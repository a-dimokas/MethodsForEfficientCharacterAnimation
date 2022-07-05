import bpy
import numpy as np
from numpy import linalg as la
import math

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

frame_last =None
maxBones = None
objName = None
fileName = None
outputName = None

#(-1,-1) for all verts
# vertsDebug = [1804,1862]
vertsDebug = [-1,-1]

#swithc to linear or non linear
nonLin = True
ftol = None
iter = None

modeList=[]
if(not nonLin):
    modeList = ['it3_init1''it3_init2','it3_init3',
'it5_init1''it5_init2','it5_init3',
'it8_init1''it8_init2','it8_init3',
'it10_init1''it10_init2','it10_init3',
'it12_init1','it12_init2','it12_init3']
else:
    modeList = ['']

for mode in modeList:

    if bpy.data.actions:

        # get all actions
        action_list = [action.frame_range for action in bpy.data.actions]
        
        #find the first and last keyframe
        frames = (sorted(set([item for sublist in action_list for item in sublist])))
        frame_first = int(frames[0])
        #frame_last = int(frames[-1])#
        #assign the current frame as the first one
        current_frame = frame_first
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        Aorig = []
        Aapprox = []
        max_dist = []
        Aavg = []
        with open(blenderHomeDir+"\\globalVertices\\"+objName+"\\vert1.txt", "r") as file:
            for vertCount, line in enumerate(file):
                if(vertCount>vertsDebug[0]):
                    for i in range(3):
                        Aavg.append(0.)
                if(vertCount==vertsDebug[1]):
                    break
        file.close()
        #loop for every frame
        while current_frame<frame_last :
                  
            #get data from files
            actualData = open(blenderHomeDir+"\\globalVertices\\"+objName+"\\vert"+str(current_frame)+".txt")
            
            if(nonLin):
                estData = open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\approxVerts\\frame"+str(current_frame)+".txt")
            else:
                estData = open(blenderHomeDir+"\\approxVerts\\"+outputName+"\\"+mode+ "\\frame"+str(current_frame)+".txt")
            
            #original vertices
            AavgCC = 0
            for pos,line in enumerate(actualData):
                if(pos>vertsDebug[0]):
                    tmpArr = line.split(",")
                    for i in range(3):
                        Aorig.append(float(tmpArr[i]))
                        Aavg[(3*AavgCC)+i] += float(tmpArr[i])
                    AavgCC += 1
                if(pos==vertsDebug[1]):
                    break
            
            #approximated vertices   
            for pos,line in enumerate(estData):
                tmpArr = line.split(",")
                for i in range(3):
                    Aapprox.append(float(tmpArr[i]))
              
            #calculating max distance deviation in every frame      
            dists = []
            for i in range(pos+1):
                v_orig = [Aorig[current_frame*i*3], Aorig[current_frame*i*3 + 1], Aorig[current_frame*i*3 + 2]]
                v_approx = [Aapprox[current_frame*i*3], Aapprox[current_frame*i*3 + 1], Aapprox[current_frame*i*3 + 2]]
                dists.append(math.dist(v_orig,v_approx))
            max_dist.append(max(dists))
            
            #get next frame
            current_frame += 1
            
        
        #calculate average of og vertices in all frames
        Aavg[:] = [x / (frame_last-1) for x in Aavg]
        newAvg = []
        
        for i in range(frame_last-1):
            newAvg += Aavg
            
        
        #original - approx  (frobenius norm)
        A_orig_approx_frob = la.norm(np.array(Aorig) - np.array(Aapprox))
        
        #orig - avg (frob norm)
        A_orig_avg_frob = la.norm(np.array(Aorig) - np.array(newAvg))
        
        #Distortion percentage
        DisPer = 100 * A_orig_approx_frob / A_orig_avg_frob
        
        #ERMS
        erms = 100 * A_orig_approx_frob / math.sqrt(3*(vertCount+1)*(frame_last-1))
        
        #maximum average distance
        MaxAvgDist = sum(max_dist)/(frame_last-1)
        
        outputFilepath = ''
        if(nonLin):
            outputFilepath = blenderHomeDir+"\\metrics\\"+outputName+"\\nonLinear"+str(ftol)+"="+iter+".txt"
        else:
            outputFilepath = blenderHomeDir+"\\metrics\\"+outputName+"\\"+mode+".txt"
        with open(outputFilepath, "w") as metricOutput:
            metricOutput.write("Distortion Percentage: " + str(DisPer) + "\n")
            metricOutput.write("Root Mean Square Error: " + str(erms) + "\n")
            metricOutput.write("Maximum Average Distance: " + str(MaxAvgDist) + "\n")

        
