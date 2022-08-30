# cgivor

## Installation (Linux)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install git git-lfs
# Install blender
sudo snap install blender --channel=2.9/stable --classic
sudo apt-get install -y libxxf86vm-dev libxi6 libgconf-2-4 libxfixes-dev libgl-dev libxrender-dev
wget https://bootstrap.pypa.io/get-pip.py -P ~
/snap/blender/65/2.91/python/bin/python3.7m ~/get-pip.py
export PATH=$PATH:~/.local/bin
# Fetch cgivor package
git clone https://github.com/skyler-bruggink/cgivor.git
# Use Git Large File Storage to fetch cgivor_addon.zip
cd cgivor
git lfs pull
# Install and enable addon
blender -b -P install_cgivor_addon.py
```

## Configuration
Edit the provided `cgivor.json` file and run blender with `cgivor.py` to use the configuration on the image generator. The following describes each of the parameters:
```yaml
# CGI for Visual Object Recognition Config
# True or False
white_noise_only: False
# True or False
scene_no_trees: true
# True or False
scene_no_rocks: false
# Must be less than max rocks
min_num_rocks: 3
# Must be more than min rocks
max_num_rocks: 5
# Must be more than min trees
min_num_trees: 2
# Must be more than max trees
max_num_trees: 4
# Must be more than min subjects
min_num_subjects: 6
# Must be more than max subjects
max_num_subjects: 9
# Must be any of [ground_grass, ground_water]
ground_type: "ground_grass"
# Number in range [0-3]
grass_preset: 1
# Must be any of [morning, noon, afternoon, evening, night]
time_of_day: "afternoon"
camera_distance: 10
camera_height: 10
# True or False
random_rotate_camera: true
# True or False
random_rotate_HDRI: true
# True or False
random_ground_texture: true
# True or False
random_ground_type: true
# True or False
random_grass_texture: true
# True or False
random_time_of_day: true
image_prefix: "cgivor"
# Number of images to be generated
step_count: 5
# Starting number in the image's filename
step_start: 0
```

## Run the generator in headless mode
After editing the config file, use the following command in the cgivor directory:
```bash
blender -b -P cgivor.py
```

## Installation (Windows)
1. Download and install the latest version of [Blender for Windows](https://www.blender.org/download/).
2. Download or clone the cgivor repository to a local directory.
3. Open blender and navigate to `Edit > Preferences > Add-ons`, then select `Install`. In a file dialog select the `cgivor_addon.zip` to install the add-on.
4. Click the checkbox to enable the addon (named `3D View: CGI for Visual Object Recognition`).
5. Open the configuration panel in the 3D viewport under the CGIVOR tab.

### Note 
Make sure to press `Initialize Scene` before you run the generator.