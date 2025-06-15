import bpy
from mathutils import Vector

# Delete default objects
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# Create a simple low-poly body using cubes

def create_body():
    bpy.ops.mesh.primitive_cube_add(size=1)
    body = bpy.context.object
    body.name = 'Body'
    body.scale = (1.0, 2.5, 1.0)
    body.location = (0, 0, 1.5)
    
    # Head
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 2.2, 2.5))
    head = bpy.context.object
    head.name = 'Head'
    head.scale = (0.8, 1.0, 0.8)

    # Tail
    bpy.ops.mesh.primitive_cone_add(radius1=0.4, radius2=0.05, depth=3.0, location=(0, -2.5, 1.2))
    tail = bpy.context.object
    tail.name = 'Tail'
    tail.rotation_euler = (1.5708/4, 0, 0)

    # Legs
    for x in (-0.4, 0.4):
        bpy.ops.mesh.primitive_cube_add(size=0.4, location=(x, 0.3, 0.5))
        leg = bpy.context.object
        leg.name = f'Leg_{"L" if x<0 else "R"}1'
        leg.scale = (0.4, 0.4, 1.0)

    # Arms
    for x in (-0.3, 0.3):
        bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 1.4, 1.8))
        arm = bpy.context.object
        arm.name = f'Arm_{"L" if x<0 else "R"}'
        arm.scale = (0.2, 0.2, 0.5)

    # Join meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    return body


def create_material(obj):
    mat = bpy.data.materials.new(name='CarnotaurusSkin')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.4, 0.25, 0.1, 1)  # brownish
    obj.data.materials.append(mat)


def create_armature(obj):
    bpy.ops.object.armature_add(enter_editmode=True, location=(0,0,0))
    arm = bpy.context.object
    arm.name = 'Armature'
    arm.show_in_front = True
    amt = arm.data
    amt.edit_bones.remove(amt.edit_bones['Bone'])

    bones = {
        'root': ((0,0,0), (0,0,1)),
        'spine': ((0,0,1), (0,0,2.2)),
        'head': ((0,0,2.2), (0,2.2,2.5)),
        'tail': ((0,0,1), (0,-2.5,1.2)),
        'leg.L': ((-0.4,0.3,0.5), (-0.4,0.3,0)),
        'leg.R': ((0.4,0.3,0.5), (0.4,0.3,0)),
        'arm.L': ((-0.3,1.4,1.8), (-0.3,1.4,1.5)),
        'arm.R': ((0.3,1.4,1.8), (0.3,1.4,1.5)),
    }
    for name, (head, tail) in bones.items():
        bone = amt.edit_bones.new(name)
        bone.head = Vector(head)
        bone.tail = Vector(tail)
        if name in ['spine', 'head', 'tail']:
            bone.parent = amt.edit_bones['root'] if name=='spine' else amt.edit_bones['spine']
    bpy.ops.object.mode_set(mode='OBJECT')

    modifier = obj.modifiers.new('armature', 'ARMATURE')
    modifier.object = arm
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    return arm


def export_fbx(path):
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True)


def main():
    clear_scene()
    body = create_body()
    create_material(body)
    arm = create_armature(body)
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    body.select_set(True)
    export_fbx('AI_Generated/Prefabs/Dinosaurs/carnotaurus_model.fbx')


if __name__ == "__main__":
    main()
