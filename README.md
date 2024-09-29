# Map-Content-Purger

This repository contains a Python script designed to help manage and optimize Garry's Mod map content by removing unused materials and assets from map files, ultimately minimizing upload overhead.

## Purpose 

The goal of this script is to:
 
- **Reduce map content size** : By removing unused materials, models, and sounds, it minimizes the overall content that needs to be uploaded to the server.
 
- **Optimize server upload** : Only required assets are gathered and prepared for upload to the workshop.
 
- **Simplify map management** : Organizes map content and ensures that no unnecessary files are included in the final package.

## Decompiling Models Using Crowbar 
In order to handle all the models referenced in your map (including their textures), you need to **decompile the models**  using **Crowbar** .
### Steps to Decompile Models: 
 
1. **Download and Install Crowbar** : 
  - Download Crowbar from the official Crowbar tool page on Steam: [Crowbar Tool](https://steamcommunity.com/groups/CrowbarTool) .
 
2. **Set Up Crowbar** : 
  - Open Crowbar and go to the **Decompile**  tab.
 
  - Set the path where the decompiled model files will be saved (e.g., `.qc`, `.smd` files).
 
3. **Decompile the Models** :
  - Select models folder you wish to decompile.

  - Select "Folder for each model"

  - Output to Sbufolder
 
  - Click **Decompile**  to extract all model data.
 
4. **Place Decompiled Models** : 
  - Move the decompiled models to the following directory (as specified in the script):

```javascript
C:/GModMapping/Content/_decompiled_models/
```
 
  - Ensure that the `.qc`, `.smd`, and associated texture files are in the appropriate folders within this directory.

## How to Use the Script 

The script is designed to extract all the necessary assets (textures, models, sounds) required for the map and copy them to a designated upload folder, leaving out unused files.

### Configuration 
 
- **VMF_path** : Set the path to your `.vmf` file (the map file you're working on).
Example:

```python
VMF_path = 'C:/GModMapping/Maps/my_map.vmf'
```
 
- **content_path** : Set the base path to where your Garry's Mod content is stored. This includes folders for textures, models, and sounds.
Example:

```python
content_path = "C:/GModMapping/Content/"
```
 
- **upload_path** : Set the path where the script will copy all the required content for the final upload (textures, models, sounds).
Example:

```python
upload_path = "C:/GModMapping/Upload/"
```
 
- **decompiled_models_path** : Set the path where your decompiled models from Crowbar are located (as described in the decompiling section).
Example:

```python
decompiled_models_path = "C:/GModMapping/Content/_decompiled_models/"
```

### Running the Script 
 
1. **Prepare the VMF file** :
Ensure that the VMF file for your map is in the specified `VMF_path`.
 
2. **Prepare Content Folders** :
Make sure that all your materials, models, and sounds are organized in the directories specified in `content_path`. Decompiled models should be in the `_decompiled_models` folder within `content_path`.
 
3. **Run the Script** :
Execute the Python script in your environment. It will:
  - Parse the VMF file to find all used models, textures, sounds, and skyboxes.
 
  - Copy the required files from your content folders to the `upload_path`.

  - Log any missing models or materials that it cannot find.
 
4. **Review Logs** :
The script generates log files that track:
  - Successfully copied assets.

  - Missing models, textures, or sounds.

  - Errors encountered during the copy process.

Check the logs to verify the copy process was successful.

### Output Structure 
After running the script, the folder specified in `upload_path` will contain only the necessary files, organized as follows:

```markdown
Upload/
    ├── models/
    ├── materials/
    └── sounds/
```

This structure can be used directly for uploading content to your Garry's Mod server.

### Removing Unused Content 

The script helps you identify and exclude unused materials and models from the upload process, minimizing the size of the final package and optimizing server performance.

## Disclaimer 
This script is provided **as-is** , and **no support**  is offered for any issues, bugs, or inquiries. Use this tool at your own risk. The script is intended to assist in reducing the size of map content for DarkRP servers by removing unused materials, models, and sounds.
