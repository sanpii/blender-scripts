bl_info = {
    "name": "My Pie Menus",
    "author": "Sanpi",
    "version": (1, 0, 0),
    "blender": (2, 75, 0),
    "description": "My Pie Menus",
    "category": "User Interface",
}

import bpy
from bpy.types import Menu, Operator

class ModeEdit(Operator):
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context, type):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type=type)

        return {"FINISHED"}

class ModeVertex(ModeEdit):
    bl_idname = "mode.vertex"
    bl_label = "Vertex"

    def execute(self, context):
        return super().execute(context, "VERT")

class ModeFace(ModeEdit):
    bl_idname = "mode.face"
    bl_label = "Face"

    def execute(self, context):
        return super().execute(context, "FACE")

class ModeEdge(ModeEdit):
    bl_idname = "mode.edge"
    bl_label = "Edge"

    def execute(self, context):
        return super().execute(context, "EDGE")

class ModeSwitch(Operator):
    bl_idname = "mode.switch"
    bl_label = "Edit / Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}

class MainMenu(Menu):
    bl_label = ""

    def draw(self, context):
        pie = self.layout.menu_pie()

        pie.operator("mode.vertex", icon="VERTEXSEL")
        pie.operator("mode.face", icon='FACESEL')
        pie.operator("mode.edge", icon='EDGESEL')
        pie.operator("mode.switch", icon="OBJECT_DATAMODE")

addon_keymaps = []

def register():
    bpy.utils.register_module(__name__)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = 'MainMenu'
        addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

if __name__ == "__main__":
    register()
    bpy.ops.wm.call_menu_pie(name="MainMenu")
