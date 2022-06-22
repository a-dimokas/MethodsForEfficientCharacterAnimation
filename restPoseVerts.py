#script to get the rest pose vertices and save them on txt

objName = 'Armature'
meshName = "Tops"
fileobjName = 'Maria'
frame_last = 78

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

import bpy, bmesh
obj = bpy.context.active_object

if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data)
    vertices = bm.verts

else:
    vertices = obj.data.vertices

verts = [obj.matrix_world @ vert.co for vert in vertices] 

# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]

vertFile = open(blenderHomeDir+"\\restPoseVerts\\"+fileobjName+"\\verts.txt", "w+")

for v in plain_verts:
    vertFile.write(str(v[0]) + ", " + str(v[1]) + ", " + str(v[2]) + "\n")
