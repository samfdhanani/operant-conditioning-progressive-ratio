A massive thank you to Tala Sohrabi (@Talaa202) for teaching me and helping me write this code and to the Balsam-Simpson Lab at the New York State Psychiatric Institute for letting me borrow their Med Associate operant boxes!

# Progressive Ratio
## Task Details
In the PR task, the number of lever presses required to obtain a reward starts with 2 presses and doubles thereafter with each reward, such that the number of lever presses in sequence is 2, 4, 8, 16, 32, 64, 128, etc. Only one lever is presented in these sessions and the lever presentation (right vs left) is alternated each session. The PR task ended after two hours or three minutes without a lever press.

### Training Overview
After learning how to make a lever press, the mice were trained using a variable ratio (VR) schedule. To get the mice used to making many lever presses we trained them from a VR4 schedule to a VR20 schedule, where a reward is presented on average every 20 presses. 

## Apparatus Information
The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).

 'Ratios', 'Presses Made per Ratio','Running Rate', 'Average Running Rate for all Ratios'

## Script Outputs
- Date: date of session.
- Subject: subject number from the Med Associates data file.
- Genotype: assigns a value to the subject based on a list defined by the user.
- Sex: assigns a value to the subject based on a list defined by the user.
- Program: program name from the Med Associates data file.
- Average Latency between Lever Presses: the average number of seconds in between every lever press in the session.
- Session Time: total session time.
- Number Of Rewards: number of rewards achieved.
- Lever Press: number of lever presses made in the entire session.
- Breakpoint: the highest number of responses made in a ratio, reward or not rewarded.
- Breakpoint Info: tells the user if the breakpoint was rewarded or not rewarded.
- First Ratio: time from the start of the session to the first reward presented.
- Last Ratio: time from the last dipper turning off the end of the session.
- Ratios: list of times in between the first lever of the ratio and the last lever of the ratio. The code uses the first lever press after the first or previous dipper turns of and the last lever press before the dipper turns on, this excludes the first and last ratio.
- Presses Made per Ratio: presses made in each ratio, this excludes the first and last ratio.
- Running Rate: the rate of lever presses per second in each ratio.
- Average Running Rate for all Ratios: the average of all the running rates for each ratio excluding the first and last ratio. 
