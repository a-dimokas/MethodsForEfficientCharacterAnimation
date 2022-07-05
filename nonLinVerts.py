import numpy as np

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

outputName = None
maxFrames = None
maxBones = None
objName = None
fileName = None

vertsDebug = [1804,1862]

#get restPose vertices
restVerts = open(blenderHomeDir+"\\restPoseVerts\\"+fileName+"\\verts.txt")
restVertData = []
for pos,line in enumerate(restVerts):
    if(pos>vertsDebug[0]):
        tmpArr = line.split(",")
        vx = float(tmpArr[0])
        vy = float(tmpArr[1])
        vz = float(tmpArr[2])
        restVertData.append(np.array([vx,vy,vz,1.]))
    if(pos==vertsDebug[1]):
        break
    
#vertex groups of model
vertexGroups = []
weightFile = open(blenderHomeDir+"\\weights\\"+objName+"\\weights.txt")
for p,l in enumerate(weightFile):
    if(p>vertsDebug[0]):
    #finding in which vertex groups indices the vertex belongs to
        vertGroups = l[1:l.find(']')].split(',')
        for i in range(len(vertGroups)):
            vertGroups[i] = int(vertGroups[i])
        vertexGroups.append(vertGroups)
    if(p==vertsDebug[1]):
            break
weightFile.close()   

bonesSort = []
for i in vertexGroups:
    for j in i:
        if j not in bonesSort:
            bonesSort.append(j)
bonesSort.sort()

bones = []
for frame in range(1,maxFrames):
    bones.append([])
    file = open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\frame"+str(frame)+".txt")
    tmp = []
    for p,l in enumerate(file):
        if(p%4==3):
            bones[frame-1].append(tmp)
            tmp = []
        else:
            tmpArr = l.split(',')
            tmp.append([float(tmpArr[0]),float(tmpArr[1]),float(tmpArr[2]),float(tmpArr[3])])
        if(p==(len(bonesSort)*4)-1):
            break
    file.close()

weights = [] 
weightFile = open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\approxVertWeights.txt")
for p,l in enumerate(weightFile):
    weights.append([])
    tmp = l.split(',')
    for i in tmp:
        weights[p].append(float(i))
    
#calculate new vertices.
for frame in range(1,maxFrames):
#    verts = []
    open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\approxVerts\\frame"+str(frame)+".txt", "w").close()
    file = open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\approxVerts\\frame"+str(frame)+".txt", "a")
    for v in range(0,len(restVertData)):
        result = 0
        for i in range(len(weights[v])):
            result += weights[v][i] * (bones[frame-1][bonesSort.index(vertexGroups[v][i])] @ restVertData[v])
        file.write(np.array2string(result, separator = ", ")[1:-1] +"\n")
    #write new verts

    
    