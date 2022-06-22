import bpy
import numpy as np
import math

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

#returns the vertices data for a single frame   
def vertexDataOfFrame(frame, totalNumOfVertices):
    #retrieve the vertex global coordinates
    file = open(blenderHomeDir+"\\vertices\\vert"+str(frame)+".txt")
    v = np.zeros((totalNumOfVertices,4))
#    v = np.zeros((totalNumOfVertices,3))
    for p,l in enumerate(file):
        tmpArr = l.split(",")
        vx = float(tmpArr[0])
        vy = float(tmpArr[1])
        vz = float(tmpArr[2])
        v[p] = np.array([vx,vy,vz,1.0])
#        v[p] = np.array([vx,vy,vz])
    file.close()
    return v

#retrieve bones spatial data
def boneDataOfFrame(n):
    file = open(blenderHomeDir+"\\bones\\bone"+str(n)+".txt")
    all_lines = file.readlines()
    ImportantBones = []
    for i in range(len(vertGroupsNames)):
        #init empty 3x4 matrix
#        ImportantBones.append(np.zeros(shape=(3,4)))
        ImportantBones.append(np.zeros(shape=(4,4)))
    cc = 0
    for i in boneIndices:
#        for j in range(3):
        for j in range(4):
            #get data from file and add it to the matrix
            getBoneData(ImportantBones[cc],j,all_lines[(i*5) + j])
        cc += 1
    file.close()
    return ImportantBones
    
    
#function to get line string from boneFile and transform it into array    
def getBoneData(matrix, lineNum, line):
    if "(((" in line:
        firstParen = line.find('(((') + 2
    else:
        firstParen = line.find('(')
    lastParen = line.find(')')
    matrix[lineNum] = [float(x) for x in line[firstParen+1:lastParen].split(",")]
    

#n is the frame from which we want to calculate the next frame's vertices data
#vert is the number of the vertex
def vertexCalculation(n,vert,vertData, boneData, file):
    #retrieve the correct vertex global coordinates
    v = vertData[vert-1]  
    #calculate the result of the matrices multiplication and the corresponding weight factor
    result = 0
    
    for i in range(len(weights[vert-1])):
        
        #old (wrong)
#        result += np.dot(v,boneData[vertexGroups[vert-1][i]]) * weights[vert-1][i]

        #working but with minor deviations
#        M = boneData[vertexGroups[vert-1][i]] @ restBones[vertexGroups[vert-1][i]]
#        result += weights[vert-1][i] * M @ v
        
        #
#        M = restBones[vertexGroups[vert-1][i]] @ boneData[vertexGroups[vert-1][i]]
#        result += weights[vert-1][i] * (M @ v)
        
        
        v_relative = restBones[vertexGroups[vert-1][i]] @ v
        result += weights[vert-1][i] * (boneData[vertexGroups[vert-1][i]] @ v_relative)
#    result = result @ v
    
    file.write(np.array2string(result, separator = ", ")[1:-1] +"\n")
    
#set mesh as active object
bpy.context.view_layer.objects.active = bpy.data.objects['Lola']
    
#get vertex groups names
vertGroupsNames = []
for vgrp in bpy.context.object.vertex_groups.items():
    vertGroupsNames.append(vgrp[0])
      
#get bones names 
bones = []
for bone in bpy.data.objects["Armature"].data.bones:
    bones.append(bone.name)
   
#get bone indices that are in vertex groups
boneIndices = []
for vertGrp in vertGroupsNames:
    boneIndices.append(bones.index(vertGrp))
   
#get weigths and vertex groups of model
weights = [] 
vertexGroups = []
weightFile = open(blenderHomeDir+"\\weights\\weights.txt")

for p,l in enumerate(weightFile):
    #finding in which vertex groups indices the vertex belongs to
    vertGroups = l[1:l.find(']')].split(',')
    for i in range(len(vertGroups)):
        vertGroups[i] = int(vertGroups[i])
    vertexGroups.append(vertGroups)
    #getting the weights for the correponding vertex groups
    weight = l[l.find(']')+4:(len(l)-2)].split(',')
    w = np.array([])
    for i in weight:
        w = np.append(w,float(i))
    weights.append(w)
weightFile.close()
    
#get rest pose bone matrices
restfile = open(blenderHomeDir+"\\bones\\restBones.txt")
all_lines = restfile.readlines()
restBones = []
for i in range(len(vertGroupsNames)):
    #init empty 3x4 matrix
#    restBones.append(np.zeros(shape=(3,4)))
    restBones.append(np.zeros(shape=(4,4)))
k = 0
for i in boneIndices:
#    for j in range(3):
    for j in range(4):
        #get data from file and add it to the matrix
        getBoneData(restBones[k],j,all_lines[(i*5) + j])
    k += 1
restfile.close()  
    
# get all actions
action_list = [action.frame_range for action in bpy.data.actions]

#find the first and last keyframe
frames = (sorted(set([item for sublist in action_list for item in sublist])))
frame_last = frames[-1]

#get total number of vertices from files
lines = sum(1 for line in open(blenderHomeDir+"\\vertices\\vert1.txt"))

verticesData = vertexDataOfFrame(1,lines)

#iterate through frames of animation
for i in range(int(frame_last)):
    
    #erase contents of files
    open(blenderHomeDir+"\\phase2\\frame"+str(i+1)+".txt", "w").close()
#    if(i>0):    
    
        #get vertex data of the i frame of all vertices
#        verticesData = vertexDataOfFrame(i,lines)
        
        #get bone data of frame i + 1
    boneData = boneDataOfFrame(i+1)
        
    file = open(blenderHomeDir+"\\phase2\\frame"+str(i+1)+".txt", "a")
        
    for j in range(lines):
        vertexCalculation(i,j+1, verticesData, boneData, file)
        
    file.close()
    