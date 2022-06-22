import bpy
import numpy as np

#this script is to evaluate the difference between the actual and the phased animation on all 
#frames and vertices of the mesh

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""


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
    
    open(blenderHomeDir+"\\phase3Eval\\frameDiffEval.txt", "w").close()
    file = open(blenderHomeDir+"\\phase3Eval\\frameDiffEval.txt", "a")
    avg = []
    
    #loop for every frame
    while current_frame<frame_last :
              
        #get data from files
        actualData = open(blenderHomeDir+"\\globalVertices\\vert"+str(current_frame)+".txt")
        estData = open(blenderHomeDir+"\\approxVerts\\frame"+str(current_frame)+".txt")
        
        actualVertData = []
        for pos,line in enumerate(actualData):
            tmpArr = line.split(",")
            vx = float(tmpArr[0])
            vy = float(tmpArr[1])
            vz = float(tmpArr[2])
            actualVertData.append(np.array([vx,vy,vz]))
            
        estVertData = []
        for pos,line in enumerate(estData):
            tmpArr = line.split(",")
            vx = float(tmpArr[0])
            vy = float(tmpArr[1])
            vz = float(tmpArr[2])
            estVertData.append(np.array([vx,vy,vz]))
            
        
        #calculate diffs
        diffs = []
        for i in range(0,len(estVertData)):
            diffs.append(abs(actualVertData[i] - estVertData[i]))
        
        tmp = np.mean(diffs, axis=0)
        file.write("mean deviation of vertice data, frame " + str(current_frame) + ": \t" + repr(tmp.tolist()) + " \n")
        avg.append(tmp)
#        file.write("max: \t" + repr(np.amax(diffs, axis=0).tolist()) + "\t" + str(np.where(diffs == np.amax(diffs, axis=0))) + " \n")
        
        current_frame += 1
file.write("----------------------------------------------------------------------\n")
file.write("mean deviation for all frames: " + repr(np.mean(avg, axis=0).tolist()))
