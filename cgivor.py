import bpy
import os
# Get the containing folder of this file
dir_path = os.path.dirname(os.path.realpath(__file__))
# Load Config
bpy.ops.cgivor.load_config(config_path=os.path.join(dir_path, "cgivor.yaml"))
# Load Scene
bpy.ops.cgivor.init_scene()
# Run generator
bpy.ops.cgivor.run_generator()