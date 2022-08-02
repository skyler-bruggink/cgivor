# cgivor

## Installation (Linux)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip subversion git git-lfs
# Install blender
sudo apt install blender
# Fetch cgivor package
git clone https://github.com/skyler-bruggink/cgivor.git
# Use Git Large File Storage to fetch cgivor_addon.zip
cd cgivor
git lfs pull
# Install and enable addon
blender -b -P install_cgivor_addon.py
```

## Configuration
Edit the provided `cgivor.yaml` file and run blender with `cgivor.py` to use the configuration on the image generator.

## Run the generator
After editing the config file, use the following command in the cgivor directory:
```bash
blender -b -P cgivor.py
```
