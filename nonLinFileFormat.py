outputName = 'Lola2'
maxFrames = 137-1
maxBones = 4
objName = 'Armature'
fileName = 'Lola'

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

vertsDebug = [1804,1862]
ftol = "5e-06"

def getVertexGroups():
    weightFile = open(blenderHomeDir+"\\weights\\"+fileName+"\\weights.txt")
    vertexGroups = []
    for p,l in enumerate(weightFile):
        if(p>vertsDebug[0]):
            vertGroups = l[1:l.find(']')].split(',')
            for i in range(len(vertGroups)):
                vertGroups[i] = int(vertGroups[i])
            vertexGroups.append(vertGroups)  
        if(p==vertsDebug[1]):
            break
    weightFile.close()
    return vertexGroups

vertexGroups = getVertexGroups()
    
test = 0
boneList = []
for i in vertexGroups:
    for j in i:
        if j not in boneList:
            boneList.append(j)
boneList.sort()


file = open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\output"+ftol+".txt")
all_lines = file.readlines()
lineCc = 0
weights = []
for i in vertexGroups:
    if(len(i)>1):
        tmp = []
        for j in i:
            tmp.append(all_lines[lineCc][:-2])
            lineCc += 1
        weights.append(tmp)
    else:
        weights.append([1.])

bones = []
for frame in range(maxFrames):
    bones.append([])
    for b in boneList:
        for i in range(12):
            bones[frame].append(float(all_lines[lineCc][:-2]))
            lineCc += 1


with open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\approxVertWeights.txt", "w") as weightOutput:
    vv = 0
    for line in weights:
        tmpString = ""
        for i in range(len(vertexGroups[vv])):
            tmpString += str(line[i]) + ", "
        weightOutput.write(tmpString[:-2] + "\n")
        vv += 1
            
    for frame in range(1,maxFrames):
        with open(blenderHomeDir+"\\nonLinApprox\\"+outputName+"\\frame"+str(frame)+".txt", "w") as boneOutput:
            for b in range(len(boneList)):
                for i in range(3):
                    boneOutput.write(str(bones[frame-1][(12*b)+4*i:(12*b)+(4*i)+4])[1:-1] + "\n")
                boneOutput.write("\n")
            