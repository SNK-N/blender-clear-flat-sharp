bl_info = {
    "name": "Clear Flat Sharp",
    "author": "SNK",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar (N) > Flat Sharp",
    "description": "Batch-unlock the sharp edges on sides that are nearly flat",
    "category": "Mesh",
}

from math import radians, degrees

import bpy
import bmesh
from bpy.props import EnumProperty, FloatProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup


class CFS_Settings(PropertyGroup):
    threshold: FloatProperty(
        name="Threshold",
        description="隣り合う面の法線の角度差がこの値以下なら平面とみなす",
        subtype="ANGLE",
        default=radians(1.0),
        min=0.0,
        max=radians(90.0),
        soft_max=radians(30.0),
    )
    scope: EnumProperty(
        name="Scope",
        description="処理する範囲",
        items=[
            ("SELECTED", "選択中のみ", "編集モードで選択している辺／面だけを処理する"),
            ("ALL", "オブジェクト全体", "編集中のオブジェクト全体を処理する"),
        ],
        default="SELECTED",
    )


class MESH_OT_clear_flat_sharp(Operator):
    bl_idname = "mesh.clear_flat_sharp"
    bl_label = "Clear Flat Sharp"
    bl_description = "平面とみなせる辺のシャープ指定を解除する"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH" and context.edit_object is not None

    def execute(self, context):
        settings = context.scene.cfs_settings
        threshold = settings.threshold + 1e-5  # 浮動小数点のエラー対策用
        only_selected = settings.scope == "SELECTED"

        cleared = 0
        checked = 0

        for obj in context.objects_in_mode_unique_data:
            if obj.type != "MESH":
                continue

            bm = bmesh.from_edit_mesh(obj.data)
            bm.normal_update()

            for edge in bm.edges:
                if edge.smooth:
                    continue  # シャープが指定されていない場合
                if only_selected and not edge.select:
                    continue
                if len(edge.link_faces) != 2:
                    continue  # 境界辺や非多様体は対象外

                checked += 1
                f1, f2 = edge.link_faces
                if f1.normal.angle(f2.normal, 0.0) <= threshold:
                    edge.smooth = True
                    cleared += 1

            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

        self.report(
            {"INFO"},
            f"{cleared} 本のシャープを解除しました（対象 {checked} 本 / 角度 {degrees(settings.threshold):.2f}°）",
        )
        return {"FINISHED"}


class VIEW3D_PT_clear_flat_sharp(Panel):
    bl_label = "Clear Flat Sharp"
    bl_idname = "VIEW3D_PT_clear_flat_sharp"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Flat Sharp"

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.cfs_settings

        layout.prop(settings, "threshold")
        layout.prop(settings, "scope", expand=True)
        layout.operator(MESH_OT_clear_flat_sharp.bl_idname, icon="MOD_SMOOTH")


classes = (
    CFS_Settings,
    MESH_OT_clear_flat_sharp,
    VIEW3D_PT_clear_flat_sharp,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cfs_settings = PointerProperty(type=CFS_Settings)


def unregister():
    del bpy.types.Scene.cfs_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
