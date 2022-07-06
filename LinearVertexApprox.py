import numpy as np

maxFrames = None
maxBones = None
objName = None
fileName = None
outputName = None

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

#which verts to approx (-1,-1 for all Verts)
# vertsDebug = [1804,1862]
vertsDebug = [-1,-1]

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

for mode in ['it3_init1',#'it3_init2','it3_init3',
'it5_init1',#'it5_init2','it5_init3',
'it8_init1',#'it8_init2','it8_init3',
'it10_init1',#'it10_init2','it10_init3',
'it12_init1']:#,'it12_init2','it12_init3']:
#it() - num of iterations available
#init(1,2,3) - 
    #1 for random weights and bones
    #2 for random weights and correct bones
    #3 for correct weights and random bones

    bones = []
        #get bones approximation matrices
    for frame in range(1,maxFrames):
        bones.append([])
        file = open(blenderHomeDir+"\\approx\\"+outputName+"\\"+mode+"\\frame"+str(frame)+".txt")
#        file = open(blenderHomeDir+"\\nonLinApprox\\"+mode+"\\frame"+str(frame)+".txt")
        tmp = []
        linePos = 0
        tmptmp = []
        for p,l in enumerate(file):
            if(linePos%4==3):
                bones[frame-1].append(tmp)
                tmp = []
                linePos += 1
            else:
                tmpArr = l.split()
                if(len(tmpArr)==4):
#                print(mode, frame, p)
                    tmp.append([float(tmpArr[0]),float(tmpArr[1]),float(tmpArr[2]),float(tmpArr[3])])
                    linePos += 1
                    tmptmp = []
                else:
                    for i in tmpArr:
                        tmptmp.append(float(i))
                    if(len(tmptmp)==4):
                        tmp.append(tmptmp)
                        linePos += 1
                        tmptmp = []
                        
            if(linePos==(len(bonesSort)*4)):
                break
            
        file.close()
        
    #weights of model vertices
    weights = [] 
    weightFile = open(blenderHomeDir+"\\approxWeights\\"+outputName+"\\"+mode+"\\approxVertWeights.txt")
    for p,l in enumerate(weightFile):
        weights.append([])
        tmp = l.split(',')
        for i in tmp:
            weights[p].append(float(i))
        
    #calculate new vertices.
    for frame in range(1,maxFrames):
    #    verts = []
        open(blenderHomeDir+"\\approxVerts\\"+outputName+"\\"+mode+"\\frame"+str(frame)+".txt", "w").close()
        file = open(blenderHomeDir+"\\approxVerts\\"+outputName+"\\"+mode+"\\frame"+str(frame)+".txt", "a")
        for v in range(0,len(restVertData)):
            result = 0
            for i in range(len(weights[v])):
                result += weights[v][i] * (bones[frame-1][bonesSort.index(vertexGroups[v][i])] @ restVertData[v])
            file.write(np.array2string(result, separator = ", ")[1:-1] +"\n")
        #write new verts

    
    