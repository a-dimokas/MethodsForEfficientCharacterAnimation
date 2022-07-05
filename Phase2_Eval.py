import bpy
import numpy as np
#modify this number to any vertex number
vertNum = None

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

#this script is to evaluate the difference between the actual and the phased animation on a single vertex in every frame
open(blenderHomeDir+"\\phase2\\eval.txt", "w").close()
file = open(blenderHomeDir+"\\phase2\\eval.txt", "a")
file.write("Differences in results for vert" + str(vertNum) + ": \n")

if bpy.data.actions:

    # get all actions
    action_list = [action.frame_range for action in bpy.data.actions]
    
    #find the first and last keyframe
    frames = (sorted(set([item for sublist in action_list for item in sublist])))
    frame_first = int(frames[0])
    frame_last = int(frames[-1])
    #assign the current frame as the first one
    current_frame = frame_first
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #loop for every frame
    while current_frame<frame_last-1 :
        
        #get data from files
        actualData = open(blenderHomeDir+"\\globalVertices\\vert"+str(current_frame)+".txt")
        estData = open(blenderHomeDir+"\\phase2\\frame"+str(current_frame)+".txt")
        
        actualVertData = []
        for pos,line in enumerate(actualData):
            if pos == vertNum-1 :
                tmpArr = line.split(",")
                vx = float(tmpArr[0])
                vy = float(tmpArr[1])
                vz = float(tmpArr[2])
                actualVertData = np.array([vx,vy,vz])
                break
            
        estVertData = []
        for pos,line in enumerate(estData):
            if pos == vertNum-1 :
                tmpArr = line.split(",")
                vx = float(tmpArr[0])
                vy = float(tmpArr[1])
                vz = float(tmpArr[2])
                estVertData = np.array([vx,vy,vz])
                break
        
        #calculate diffs
        diffs = abs(actualVertData - estVertData)
        file.write("frame - " + str(current_frame) + ", Differences: " + np.array2string(diffs, separator=", ") + "\n")
        
        current_frame += 1
