import bpy
import time
from bpy.types import Mesh, Curve
import bmesh

bl_info = {
    "name": "BlenderCity",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Densyakun",
    "version": (0, 0, 1, 'alpha'),
    "location": "3Dビュー > オブジェクト",
    "support": "TESTING",
}


class BCObjMenu(bpy.types.Menu):
    bl_idname = "city.menu"
    bl_label = "BlenderCity"
    bl_description = ""

    def draw(self, context):
        self.layout.operator(EdgeA.bl_idname)


class EdgeA(bpy.types.Operator):
    bl_idname = "city.edgea"
    bl_label = "辺をカーブにしてベベルを付ける"
    bl_options = {'REGISTER', 'UNDO'}

    bevel = bpy.props.StringProperty(name="ベベル", description="")

    def execute(self, context):
        objs = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objs:
            bpy.data.objects[obj.name].select_set(True)
            context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode='EDIT')
            me = obj.data
            if type(me) is Mesh:
                bm = bmesh.from_edit_mesh(me)
                a = len(bm.faces)

                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()

                bmesh.update_edit_mesh(me)
                bpy.ops.object.mode_set(mode='OBJECT')

                if not a:
                    bpy.ops.object.convert(target='CURVE')
                    if type(context.object.data) is Curve and self.bevel:
                        context.object.data.bevel_object = bpy.data.objects[self.bevel]
            else:
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.data.objects[obj.name].select_set(False)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.menu(BCObjMenu.bl_idname)


def register():
    bpy.utils.register_class(EdgeA)
    bpy.utils.register_class(BCObjMenu)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(EdgeA)
    bpy.utils.unregister_class(BCObjMenu)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
