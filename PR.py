import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

# declaring an empty list
filelist = []
pathslist = []

datapath = os.path.normpath("filepath to cohort folder")
IDList = [1, 2, 3, 4]

# walks through the filepath, filelist contains a list of all files and pathslist contains datapaths for subfolders
for subdir, dirs, files in sorted(os.walk(datapath)):
    filelist.append(files)
    pathslist.append(subdir)

filelist.pop(0) # get rid of elements in index zero
pathslist.pop(0) # get rid of elements in index zero

# this function is used to isolate and analyze a specific folder/date from the data; run at the botton of this script
def query(pathslist, querydate): 
    folderdates = [] # stores dates from folder path
    for x in pathslist: # goes through each path in pathslist
        folderdates.append(os.path.basename(os.path.normpath(x))) # extracts the date from the filepath

    querypaths = [] # stores paths that match query dates

    for i in range(0, len(folderdates)):
        if folderdates[i] == querydate: 
            querypaths.append(pathslist[i]) # pull specific date

    return(querypaths)

# this function extracts data from each specific data file by ID 
def data_pull(datapath, ID):
    df = [] 
    progline = None
    
    for subdir, dirs, files in sorted(os.walk(datapath)): 
        for file in files:
            temp = file.split('.') # split string by '.', in this case the string is split into the sesion date (0) and Subject ID (1)
            sub = temp[1] # Subject ID
            if ID == sub:
                x = os.path.join(subdir, file) # specific file
                df = pd.read_csv(x, sep="[:\s]{1,}", skiprows=15, header=None, engine="python") # skips 15 rows to where the data actually starts
                progline = pd.read_csv(x, skiprows=12, nrows = 1, header = None, engine="python") # reads only 1 row, the program line in the 12th row
                progline = progline.values.tolist()
                progline = progline[0][0].split(" ") 
                if "_" in progline[1]:
                    progline = progline[1].split("_", 1) # splits up program name if an underscore is present
                progline = progline[1]
                df = df.drop(0,axis=1) # cleaning up the data
                df = df.stack() 
                df = df.to_frame() 
                df = df.to_numpy() # dataframe should be an array of each line containing the data, removed the row labels from the data file 
    return(df, progline)   

# this function uses event and timestamp data to output various metrics describing behavior
def data_construct(data): 

    events = np.remainder(data,10000) # use division to isolate event code
    times = data - events # subtract event code from full code

    StartTrial = times[np.where(events == 111)] # all event codes come from the MED-PC Medscript
    StartSess = times[np.where(events == 113)]
    EndSess = times[np.where(events == 114)]

    Sess_time = np.divide(np.subtract(EndSess, StartSess), 10000000)
    Sess_time = Sess_time.tolist() # turn into list
    Sess_time = Sess_time[0] # points to specific info we need

    LLever = times[np.where(events == 27)] # command for when the lever is on
    RLever = times[np.where(events == 28)]

    DipOn = times[np.where(events == 25)] # event codes for the dipper turning on and off
    DipOff = times[np.where(events == 26)]

    Lever_extensions = np.concatenate((LLever, RLever), axis = 0) # total time a lever was extended
    Lever_extensions = np.unique(Lever_extensions) # makes sure each time is only recorded once

    LLever_off = times[np.where(events == 29)]
    RLever_off = times[np.where(events == 30)]
    Lever_retractions = np.concatenate((LLever_off, RLever_off), axis = 0)
    Lever_retractions = np.unique(Lever_retractions)

    Reward = times[np.where(events == 25)]

    LPress = times[np.where(events == 1015)]
    RPress = times[np.where(events == 1016)]

    LeverPress = np.concatenate((LPress, RPress),axis=0)
    LeverPress = sorted(LeverPress) # combine lever presses into one list and keep them sorted
    LeverPress = np.unique(LeverPress) # makes sure each lever press is only recorded once

    print('Mouse - ', Full_ID)
    
    # calculating the latency array by finding the time in between lever presses until the last one when LeverPress[i+1] doesn't exist
    LA = [] # stores individual latencies

    for i in range (0, len(LeverPress)):
        p1 = np.divide(LeverPress[i], 10000000)
        try:
            p2 = np.divide(LeverPress[i+1], 10000000)
        except IndexError:
            break
        else:
            latency = p2 - p1 # next lever press - current lever press
        LA.append(latency) # add latency to LA
    
        def average_LA(LA_list):
            total = 0 # stores sum of all latencies
            for i in LA_list:
                total += i # adds latencies values to total
            return total/len(LA_list) # returns the avg by dividing the total by the number of latencies recorded
        
    average_latency = average_LA(LA)

    # calculate the number of lever presses between the last two DipOn events
    LP_for_last_reward = 2 ** len(DipOn) # number of presses required up until the last reward of the session 
   
    # calculate the number of lever presses from the last DipOff to the lever retracting
    if len(DipOff) > 0:
        last_dipoff = DipOff[-1]
        LP_to_leveroff = len([press for press in LeverPress if last_dipoff < press < Lever_retractions])
    else:
        LP_to_leveroff = 0
    # output the larger value
    breakpoint = max(LP_for_last_reward, LP_to_leveroff)


    breakpoint_info = '' # add info about breakpoint for double checking data
    if breakpoint == LP_for_last_reward: 
        breakpoint_info = 'Breakpoint Rewarded'
    else:
        if breakpoint == LP_to_leveroff:
            breakpoint_info = 'Breakpoint Not Rewarded'
    
    first_ratio = np.divide(np.subtract(DipOn[0], Lever_extensions), 10000000)
    last_ratio = np.divide(np.subtract(Lever_retractions, DipOff[-1]), 10000000)
    # calculating the latency array by finding the time in between lever presses until the last one when LeverPress[i+1] doesn't exist
    
    Ratios = []  # stores individual ratio times
    lever_presses_per_ratio = []  # stores the number of presses in each ratio
    running_rates = []  # stores the running rate for each ratio

    for i in range(len(DipOff)):
        # find the first lever press after DipOff[i]
        p1_press = next((press for press in LeverPress if press > DipOff[i]), None)
        # finds the last lever press before the next DipOn
        if i + 1 < len(DipOn):
            # get all lever presses between DipOff and the next DipOn
            presses_in_interval = [press for press in LeverPress if DipOff[i] <= press <= DipOn[i + 1]]
            
            if presses_in_interval:
                p1_press = presses_in_interval[0]  # first press after DipOff
                p2_press = presses_in_interval[-1]  # last press before DipOn

                # calculate the ratio duration in seconds using the first and last press in the interval
                p1 = np.divide(p1_press, 10000000)
                p2 = np.divide(p2_press, 10000000)
                ratio_duration = p2 - p1
                Ratios.append(ratio_duration)

                # count the number of lever presses within this interval
                lever_presses_per_ratio.append(len(presses_in_interval))

                running_rate = len(presses_in_interval) / ratio_duration
                running_rates.append(running_rate)

    avg_running_rate = np.mean(running_rates)

    return(average_latency, Sess_time, len(DipOn), len(LeverPress), breakpoint, breakpoint_info, first_ratio, last_ratio, Ratios, lever_presses_per_ratio, running_rates, avg_running_rate)

# assigns a genotype to the subjects
def genotype(sub): 
    g_type = None
    if sub == 1 or sub == 2:
        g_type = 'WT'
    elif sub == 3 or sub == 4:
        g_type = 'Het'
    return g_type
# assigns a label for sex to the subject
def sex(sub): 
    s_type = None
    if sub == 1 or sub == 3:
        s_type = 'M'
    if sub == 2 or sub == 4:
        s_type = 'F'
    return s_type

# uncomment the line below to analyze one specific day in the data, date must match folder name
# pathslist = query(pathslist, '6-14-22')

df_ind = 0 # index variable, add one everytime we run through a subject

# comment the line below when running the script for one day only 
PR_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'Program', 'Average Latency between Lever Presses', 'Session Time', 'Number Of Rewards', 'Lever Press', 'Breakpoint', 'Breakpoint Info', 'First Ratio', 'Last Ratio', 'Ratios', 'Presses Made per Ratio','Running Rate', 'Average Running Rate for all Ratios'])

def new_func(session_type, ID, progline):
        sess_type = session_type(progline, ID)
        return sess_type
def get_genotype(ID): # defines a function using ID and stores the genotype labels in g_type 
    g_type = genotype(ID)
    return g_type
def get_sex(ID): # defines a function using ID and stores the sex labels in s_type
    s_type = sex(ID)
    return s_type

for dirs in pathslist:

    date = os.path.basename(os.path.normpath(dirs))
    # uncomment the line below to analyze one specific day in the data
    # PR_df = pd.DataFrame(columns = ['Date', 'Subject', 'Program', 'Average Latency between Lever Presses', 'Session Time', 'Number Of Rewards', 'Lever Press', 'Breakpoint', 'Breakpoint Info', 'First Ratio', 'Last Ratio', 'Ratios', 'Presses Made per Ratio', 'Running Rate', 'Average Running Rate for all Ratios'])
    csv_name = ".csv"
    
    for ID in IDList: # run through ID list one by one, add 'Subject' to this to prevent confusion
        Full_ID = "Subject " + str(ID)
        data, progline = data_pull(dirs, Full_ID) # calling datapull and putting it through dirs
        if len(data) == 0:
            continue
        average_latency, Sess_time, num_Rewards, num_LeverPress, breakpoint, breakpoint_info, first_ratio, last_ratio, Ratios, lever_presses_per_ratio, running_rates, avg_running_rate = data_construct(data) 
        g_type = get_genotype(ID)
        s_type = get_sex(ID)
        #sess_type = session_type(date, ID)

        PR_df.loc[df_ind] = [date, Full_ID, g_type, s_type, progline, average_latency, Sess_time, num_Rewards, num_LeverPress, breakpoint, breakpoint_info, first_ratio, last_ratio, Ratios, lever_presses_per_ratio, running_rates, avg_running_rate] 
        df_ind += 1 # location zero is populated with variables above, add one each time for it to be sequential

    # uncomment the line below to analyze one specific day in the data
    # DRL_df.to_csv(dirs + csv_name)

# comment the line below to analyze one specific day in the data
PR_df.to_csv(datapath + "_DATE.csv")
