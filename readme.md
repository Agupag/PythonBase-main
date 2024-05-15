This is a project stub for creating our drone base station in python. The thought would be to use a laptop as the base station, which would give us an integrated input system, the option to use a graphical interface easily (Tkinter), and get us in a language that's a little more friendly for the lion's share of our work.

Plan: Create two queues. One to go in to the comm thread, and one to come out of it. When the comm thread gets something the main thread needs to deal with, it passes it using the appropriate queue.  When the main thread gets something the comm thread needs to do, it passes it using the appropriate queue. 

On the main thread, we use the after with a brief delay to let it check the queue every...half second?
On teh comm thread, we include a check every time through the loop. 

Current Packets List: 
From Drone: 
1. HND|(index if known, -1 if not)|drone name --- introduces this drone to the base station. Base station adds it to the known list. 

Desired Packets List: 
1. UPD|index|name|... (an option to provide needed telemetry data to the base station)
2. EMG|index|name|... (an option to provide emergency communication for action)




