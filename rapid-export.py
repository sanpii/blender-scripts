# Render video markers as images

import bpy

scene = bpy.context.scene

filepath = scene.render.filepath
frame_range = scene.frame_start, scene.frame_end

markers = scene.timeline_markers[:]
markers.sort(key=lambda m: m.frame)

for i in range(len(markers)):
    scene.frame_start = scene.frame_end = markers[i].frame
    scene.frame_set(scene.frame_start)
    scene.render.filepath = filepath + markers[i].name
    bpy.ops.render.render(write_still=True)

scene.render.filepath = filepath
scene.frame_start, scene.frame_end = frame_range
