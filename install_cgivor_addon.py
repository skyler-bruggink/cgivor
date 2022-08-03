import bpy
import os
# Get the containing folder of this file
dir_path = os.path.dirname(os.path.realpath(__file__))

addon_file = os.path.join(dir_path, "cgivor_addon.zip")
bpy.ops.preferences.addon_install(overwrite=True, filepath=addon_file)
bpy.ops.preferences.addon_enable(module="cgivor_addon")

preferences = bpy.context.preferences
cycles_preferences = preferences.addons['cycles'].preferences
cuda_devices, opencl_devices = cycles_preferences.get_devices()

cycles_preferences.compute_device_type = "CUDA"

for device in cuda_devices:
    device.use = True
