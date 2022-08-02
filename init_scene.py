import random
import bpy
import os
import math
import mathutils

linked_object_names = [
  "goose",
  "ground",
]

class CGIVOR_OT_init_scene(bpy.types.Operator):
  """Create the basic scene setup needed to render an object"""

  bl_idname = "cgivor.init_scene"
  bl_label = "Initialize Scene"
  bl_options = {"REGISTER", "UNDO"}

  collection_name: bpy.props.StringProperty(
    name="Collection Name",
    description="Name of collection of active render objects",
    default="Geese",
  )
  object_name: bpy.props.StringProperty(
    name="Object Name",
    description="Name of base render object",
    default="Goose",
  )

  def create_collection(self, col_name):
    try:
      col = bpy.data.collections[col_name]
    except KeyError:
      bpy.data.collections.new(col_name)
      col = bpy.data.collections[col_name]
      bpy.context.scene.collection.children.link(col)
    while col.objects:
      bpy.data.objects.remove(col.objects[0], do_unlink=True)
    return col

  def create_world_shader(self):

    nodeTree = bpy.context.scene.world.node_tree    
    for node in nodeTree.nodes:
        nodeTree.nodes.remove(node)

    texCoord = nodeTree.nodes.new('ShaderNodeTexCoord')
    mapping = nodeTree.nodes.new('ShaderNodeMapping')
    nodeTree.links.new(texCoord.outputs["Generated"], mapping.inputs[0])
    texEnv = nodeTree.nodes.new('ShaderNodeTexEnvironment')
    nodeTree.links.new(mapping.outputs[0], texEnv.inputs[0])

    background1 = nodeTree.nodes.new('ShaderNodeBackground')
    background1.inputs[1].default_value = 1.0
    nodeTree.links.new(texEnv.outputs[0], background1.inputs[0])

    texSky = nodeTree.nodes.new('ShaderNodeTexSky')
    texSky.sun_intensity = 0.5  # Sun Intensity
    texSky.sun_elevation = math.radians(70.0) # Sun Elevation
    texSky.air_density = 0      # Air
    texSky.dust_density = 0     # Dust
    texSky.ozone_density = 0    # Ozone

    hueSat = nodeTree.nodes.new('ShaderNodeHueSaturation')
    nodeTree.links.new(texSky.outputs[0], hueSat.inputs[4])
    background2 = nodeTree.nodes.new('ShaderNodeBackground')
    background2.inputs[1].default_value = 0.4
    nodeTree.links.new(hueSat.outputs[0], background2.inputs[0])

    mixShader = nodeTree.nodes.new('ShaderNodeMixShader')
    mixShader.inputs[0].default_value = 0.75
    nodeTree.links.new(background2.outputs[0], mixShader.inputs[1])
    nodeTree.links.new(background1.outputs[0], mixShader.inputs[2])
    output = nodeTree.nodes.new('ShaderNodeOutputWorld')
    nodeTree.links.new(mixShader.outputs[0], output.inputs[0])

  def append_object(self, file_path, name):
    bpy.ops.wm.append(
      filename=os.path.join(file_path, '\\Object\\', name)
    )

  def execute(self, context):

    for collection in bpy.data.collections:
      for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
      bpy.data.collections.remove(collection)

    bpy.ops.outliner.orphans_purge()

    col = self.create_collection(self.collection_name)
    base_col = self.create_collection("BaseObjects")
    env_col = self.create_collection("Environment")

    # Setup the camera
    camera = bpy.data.objects.get("Camera")
    if camera is None:
      camera = bpy.data.cameras.new("Camera")
    camera.lens = 60
    camera_obj = bpy.data.objects.new("Camera", camera)
    camera_obj.location = (0, 0, 5)
    camera_obj.rotation_euler = (0, 0, 0)
    context.scene.camera = camera_obj
    base_col.objects.link(camera_obj)
 
    file_path = os.path.join(bpy.utils.user_resource('SCRIPTS', path="addons"), "\\cgivor_addon\\assets\\")
    # Link into the assets blend file
    for obj in ["ground_grass", "ground_water"]:
      self.append_object(os.path.join(file_path + "environment.blend"), obj) 
      context.scene.collection.objects.unlink(bpy.data.objects.get(obj))
      base_col.objects.link(bpy.data.objects.get(obj))
      ground = base_col.objects.get(obj)
      if obj == context.scene.ground_type:
        ground.hide_render = False
        ground.hide_set(False)
      else:
        ground.hide_render = True
        ground.hide_set(True)
      
    self.append_object(os.path.join(file_path + "environment.blend"), self.object_name) 
    context.scene.collection.objects.unlink(bpy.data.objects.get(self.object_name))
    base_col.objects.link(bpy.data.objects.get(self.object_name))

    # Link rocks
    if not context.scene.scene_no_rocks:
      for r in range(1,6):
        self.append_object(os.path.join(file_path + "environment.blend"), "rock_"+str(r))
        base_col.objects.link(bpy.data.objects.get("rock_"+str(r)))
        context.scene.collection.objects.unlink(bpy.data.objects.get("rock_"+str(r)))
    # Link trees
    if not context.scene.scene_no_trees:
      for t in range(1,6):
        self.append_object(os.path.join(file_path + "environment.blend"), "tree_"+str(t))
        base_col.objects.link(bpy.data.objects.get("tree_"+str(t)))
        context.scene.collection.objects.unlink(bpy.data.objects.get("tree_"+str(t)))

    for file in os.listdir(file_path):
      try:
        bpy.data.images[file].reload()
      except KeyError:
        if file.endswith(".exr"):
          bpy.data.images.load(os.path.join(file_path, file), check_existing=False)

    self.create_world_shader()

    # Place the camera in its default position
    alpha = 2 * math.pi * random.random()
    x_pos = context.scene.camera_distance * math.cos(alpha)
    y_pos = context.scene.camera_distance * math.sin(alpha)
    loc_camera = mathutils.Vector((x_pos, y_pos, context.scene.camera_height))
    bpy.data.objects["Camera"].location = loc_camera
    direction = loc_camera - mathutils.Vector((0,0,0))
    rot_quat = direction.to_track_quat('Z', 'Y')
    bpy.data.objects["Camera"].rotation_euler = rot_quat.to_euler()
  
    context.scene.render.engine = "CYCLES"
    context.scene.render.resolution_x = 1000
    context.scene.render.resolution_y = 1000
    if bpy.context.scene.world.node_tree.nodes['Environment Texture'].image is None:
      bpy.context.scene.world.node_tree.nodes['Environment Texture'].image = bpy.data.images["kloetzle_blei_4k.exr"]

    return {"FINISHED"}