import bpy
import os

bpy.ops.preferences.addon_enable(module="cgivor_addon")
bpy.ops.preferences.addon_enable(module="cycles")

# Get the containing folder of this file
dir_path = os.path.dirname(os.path.realpath(__file__))
# Load Config
bpy.ops.cgivor.load_config(config_path=os.path.join(dir_path, "cgivor.json"))
# Load Scene
bpy.ops.cgivor.init_scene()
# Run generator
bpy.ops.cgivor.run_generator()
