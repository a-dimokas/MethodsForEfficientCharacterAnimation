import bpy
import bmesh

#the blender home directory is needed for the project (eg: C:\\Users\\----\\Blender)
blenderHomeDir = ""

bpy.ops.object.mode_set(mode='EDIT')
obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data)
file = open(blenderHomeDir+"\\phase2\\faces.txt", "a")

for f in bm.faces:
    for v in f.verts:
        file.write(str(v.index) + " ")
    file.write("\n")