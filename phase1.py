import bpy
import bmesh
import numpy as np

#declare object name and variables
objName = None
meshName = None
fileName = None
frame_last = None

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

#save verts global coords
def vertsGlobal(obj, depgraph, current_frame):
    vertFile = open(blenderHomeDir + "\\globalVertices\\"+fileName+"\\vert"+str(current_frame)+".txt", "w")
        #get mesh from object 
    mesh = bmesh.new()
    mesh.from_object(obj, depgraph)
        #iterate through each vertex and write save the coords
    for i, v in enumerate(mesh.verts):
        tmp = obj.matrix_world @ v.co
#           tmp = v.co
        vertFile.write(str(tmp[0]) + ', ' + str(tmp[1]) + ', ' + str(tmp[2]) + '\n')
    vertFile.close()

#saves bones' global matrices to the dictionary
def boneWorldMatrices(parent, dict, armature):
    #parent has at least 1 child
    if len(parent.children) != 0 :
        #iterate the children of parent
        for c in parent.children:
            tmp1 = armature.matrix_world @ c.matrix @ dict[parent.name]
            tmp2 = parent.matrix @ c.matrix
            for i in range(3):
                tmp2[i][3] = tmp1[i][3]
            dict[c.name] = tmp2
            
            #recursion for each children to check for grandchildren etc
            boneWorldMatrices(c, dict, armature)
        

#dependency graph
depgraph = bpy.context.evaluated_depsgraph_get()

#check if there are actions to be executed
if bpy.data.actions:

    # get all actions
    action_list = [action.frame_range for action in bpy.data.actions]
    
    #find the first and last keyframe
    frames = (sorted(set([item for sublist in action_list for item in sublist])))
    frame_first = 1
    #assign the current frame as the first one
    current_frame = frame_first
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #get list of pose bones
    arma = bpy.data.objects[objName]
    boneList = arma.pose.bones
    
    #save rest bones in file
    restBoneFile = open(blenderHomeDir + "\\bones\\"+fileName+"\\restBones.txt", "w")
    for i in arma.data.bones:
        restBoneFile.write(i.name + ', ' + repr(i.matrix_local.inverted()) + '\n\n')
        
    restBoneFile.close()
    
    #iterate through animation frames
    while current_frame<frame_last + 1:
                
        obj = bpy.data.objects[meshName]
        
        vertsGlobal(obj, depgraph, current_frame)
        
        #open file to store vertex coords to
        vertFile = open(blenderHomeDir + "\\vertices\\"+fileName+"\\vert"+str(current_frame)+".txt", "w")
        
        #iterate and save vertices in localspace vert file
        for v in obj.data.vertices:
            vertFile.write(str(v.co[0]) + ', ' + str(v.co[1]) + ', ' + str(v.co[2]) + '\n')
            
        vertFile.close()
            
        #switch to pose mode for handling armature's bone data  
        obj = bpy.data.objects[objName]
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='POSE')
        
        #here we store the bones' data  
        boneFile = open(blenderHomeDir + "\\bones\\"+fileName+"\\bone"+str(current_frame)+".txt", "w")
        
        #dictionary in the form: { boneName: boneWorldMatrix, ... }
        #to save world space matrices and names for children and parents of the bone hierarchy
        boneDict = {}
        
        #save global bone transformation matrices
        for i in boneList:
            boneDict[i.name] = arma.convert_space(pose_bone=i, matrix=i.matrix, from_space='POSE', to_space='WORLD')
            boneFile.write(i.name + ', ' + repr(boneDict[i.name]) + '\n\n')
        
        boneFile.close()
        
        #switch back to object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #increment frame counter and jump to the scene's next frame
        current_frame += 1
        bpy.context.scene.frame_set(current_frame)
        

#reset the current keyframe to 0
bpy.data.scenes["Scene"].frame_current = 0


#         #here we can store the bones' hierarchy  
#boneFile = open("C:\\Users\\30693\\sxoli\\diploma\\Blender\\boneHier\\boneHierarchy.txt", "w")
#for i in arma.matrix_world:
#    tmpString = ''
#    for j in i:
#        tmpString += str(j) + ", "
#    boneFile.write(tmpString[0:len(tmpString)-2] + "\n")
#bpy.ops.object.mode_set(mode='POSE')        
#for i in boneList:
#    if len(i.children) > 0:
#        childrens = []
#        for c in i.children:
#            childrens.append(c.name)
#        boneFile.write(i.name + ', ' + ", ".join(childrens) + '\n')
#    else:
#        boneFile.write(i.name + ', leafNode' + '\n')
#boneFile.close()
#bpy.ops.object.mode_set(mode='OBJECT')

 
#initialize objects for vertex Groups and weights extraction
obj = bpy.data.meshes[meshName]
curr_obj = bpy.data.objects[meshName]
bpy.context.view_layer.objects.active = curr_obj
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')  

#vlist = vertexGroups list
#wlist = weights list
vlist = []
wlist = []

#get appropriate matching indices of vertexGroups and pose Bones
vg_indices = []
boneNames = []
for i in arma.data.bones:
    boneNames.append(i.name)

for i in curr_obj.vertex_groups:
    if(i.name in boneNames):
        vg_indices.append(boneNames.index(i.name))
        

#initialize arrays for vertices groups and coressponding weights  
for v in obj.vertices:
    vlist.append([])
    wlist.append([])

#iterate each vertex group to find which vertices are affected by it
for vg_index in vg_indices:
    #find vertices that belong to vg_index vertex group 
    vs = [ v for v in obj.vertices if vg_indices.index(vg_index) in [ vg.group for vg in v.groups ] ]
    
    #fill the arrays 
    for i in vs:
        vlist[i.index].append(vg_index)
        wlist[i.index].append(obj.vertices[i.index].groups[len(vlist[i.index])-1].weight)
    
#coefficiency of weights    
for i in range(len(wlist)):
    sumW = sum(wlist[i])
    for j in range(len(wlist[i])):
        wlist[i][j] = wlist[i][j] / sumW
    
#save data to weight file
weightFile = open("C:\\Users\\30693\\sxoli\\diploma\\Blender\\weights\\"+fileName+"\\weights.txt", "w+")
for i in range(len(vlist)):
    weightFile.write(str(vlist[i]) + ", " + str(wlist[i]) + '\n')
    
weightFile.close()
    
bpy.ops.object.mode_set(mode='OBJECT')