# Define paths
VMF_path = 'S:/_GmodMapping/VMFs/_current/github/rp_evocity_v33x_sb_n13.vmf'

content_path = "S:/_GmodMapping/HammerContent/css-content-gmodcontent/"
upload_path = "S:/_GmodMapping/HammerContent/upload_check/"

additional_models_file = "S:/_GmodMapping/additional.txt"
use_additional_models = True

#########################################################

#########################################################
#########################################################

#########################################################

import re
import os
import shutil
import logging

###ADD SKYBOX "skyname" "mpa104" S:\Python\Conent\rp_evocity_sb_materials_1686896941\materials\skybox

material_path = f"{content_path}materials/"
sounds_path = f"{content_path}sound/"
decompiled_models_path = f"{content_path}_decompiled/"


new_model_path = upload_path
new_material_path = f"{upload_path}materials/"
new_sounds_path = f"{upload_path}sound/"

# Create the new_model_path folder if it doesn't exist
if not os.path.exists(new_model_path):
    os.makedirs(new_model_path)

# Set up logging
log_folder = new_model_path
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, 'model_copy_log.txt')
missing_models_log_file = os.path.join(log_folder, 'missing_models_log.txt')

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
missing_models_log = open(missing_models_log_file, 'w')

# Create a set to store distinct models
distinct_models = set()

existing_models = set()

model_count = 0
qc_count = 0
texture_folder_count = 0
smd_count = 0
smd_texture_count = 0


def copy_texture(texture_path):
    texture_path = texture_path.lower()
    basetexture_values = {}
    source_path = os.path.join(content_path,"materials",texture_path)
    dest_path = os.path.join(new_material_path, texture_path)
    filename = os.path.basename(os.path.splitext(texture_path)[0])

    if os.path.exists(source_path):
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        shutil.copy2(source_path, dest_path)

    vmt_path = source_path

    if os.path.exists(vmt_path):
        with open(vmt_path, 'r') as vmt_file:
            vmt_content = vmt_file.read()

        basetexture_matches = re.findall(r'\$(basetexture|bumpmap|detail|parallaxmap|basetexturetransform|detailtexturetransform|detail_alpha_mask_base_texture|lightwarptexture|blendmodulatetexture|envmapmask|selfillummask|hdrbasetexture)\d*["]?\s+"(.*?)"', vmt_content, re.IGNORECASE)
        basetexture_matches += re.findall(r'\$(basetexture|bumpmap|detail|parallaxmap|basetexturetransform|detailtexturetransform|detail_alpha_mask_base_texture|lightwarptexture|blendmodulatetexture|envmapmask|selfillummask|hdrbasetexture)\s+"?(.*?)"?$', vmt_content, re.IGNORECASE | re.MULTILINE)
        if basetexture_matches:
            basetexture_values[filename] = basetexture_matches

            for basetexture_match in basetexture_matches:
                basetexture_file = basetexture_match[1].split(".", 1)[0]
                source_texture_path = os.path.join(material_path, basetexture_file + ".vtf")
                dest_texture_path = os.path.join(new_material_path, basetexture_file + ".vtf")
                dest_dir = os.path.dirname(dest_texture_path.lower())
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                if os.path.exists(source_texture_path):
                    shutil.copy2(source_texture_path, dest_texture_path)
                else:
                    missing_vtf_message = f"Missing VTF file: '{basetexture_file}.vtf' (used in '{filename}.vmt')"
                    print(missing_vtf_message)


def copy_skybox(skybox_basename):
    src_skybox_path =  os.path.join(material_path, "skybox")
    dest_skybox_path = os.path.join(new_material_path, "skybox")
    print(skybox_basename)
    print(src_skybox_path)
    print(dest_skybox_path)
    os.makedirs(dest_skybox_path, exist_ok=True)
    files = os.listdir(src_skybox_path)
    # Iterate through the files and copy those that start with "mpa104"
    for filename in files:
        print(filename)
        if filename.startswith(skybox_basename):
            source_file = os.path.join(src_skybox_path, filename)
            destination_file = os.path.join(dest_skybox_path, filename)
            shutil.copy2(source_file, destination_file)
            print(source_file)
            print(destination_file)

def copy_map_required_files():
    with open(VMF_path, 'r') as file:
        content = file.read()

    # Find all matches in the content
    texture = re.findall(r'"(material|texture)" "(.*?)"', content, re.IGNORECASE)  # Perform a case-insensitive match
    distinct_textures = set(texture)

    for match in distinct_textures:
        copy_texture(match[1]+".vmt")

    sound = re.findall(r'"([^"]+\.wav)"', content, re.IGNORECASE)  # Perform a case-insensitive match
    distinct_sounds = set(sound)

    for match in distinct_sounds:
        copy_sound(match)

    skybox_texture = re.findall(r'"skyname"\s+"([^"]+)"', content, re.IGNORECASE)  # Perform a case-insensitive match
    distinct_skybox_textures = set(skybox_texture)

    for match in distinct_skybox_textures:
        copy_skybox(match)


def copy_sound(sound):
    # Construct the full path to the model directory
    source_dir = os.path.join(sounds_path, os.path.dirname(sound))
    # Get the base name (file name without extension) of the model
    sound_base_name = os.path.basename(sound).split('.')[0]

    if os.path.exists(source_dir):
        try:
            # Loop through the files in the source directory
            for root, _, files in os.walk(source_dir):
                for file in files:
                    # Check if the file name matches the base name of the model
                    if file.startswith(sound_base_name):
                        source_path = os.path.join(root, file)
                        relative_path = os.path.relpath(source_path, sounds_path)
                        destination_path = os.path.join(new_sounds_path, relative_path)

                        # Ensure the destination directory exists
                        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                        shutil.copy(source_path, destination_path)
                        #print(f"File '{file}' copied successfully.")

        except Exception as e:
            logging.error(f"Error copying files for Sound '{sound}': {str(e)}")
    else:
        missing_models_log.write(f"Sound directory '{sound}' does not exist.\n")



# Open the VMF file and search for models using regex
with open(VMF_path, 'r', encoding='utf-8') as vmf_file:
    vmf_content = vmf_file.read()
    # Use a case-insensitive regex pattern to find models
    model_pattern = re.compile(r'"model" "(.*?)"', re.IGNORECASE)
    matches = model_pattern.findall(vmf_content)
    # Add the distinct models from the VMF file to the set
    distinct_models.update(matches)

# Read additional models from the additional_models_file
if use_additional_models:
    if os.path.exists(additional_models_file):
        with open(additional_models_file, 'r', encoding='utf-8') as additional_models_file:
            additional_models = additional_models_file.readlines()
            # Remove empty lines and lines starting with #
            additional_models = [model.strip() for model in additional_models if model.strip() and not model.strip().startswith('#')]
            # Add additional models to the set
            distinct_models.update(model.lower() for model in additional_models)

# Copy the files matching the model names while preserving the folder structure
for model in distinct_models:
    # Construct the full path to the model directory
    source_dir = os.path.join(content_path, os.path.dirname(model))
    # Get the base name (file name without extension) of the model
    model_base_name = os.path.basename(model).split('.')[0]

    if os.path.exists(source_dir):
        try:
            # Loop through the files in the source directory
            for root, _, files in os.walk(source_dir):
                for file in files:
                    # Check if the file name matches the base name of the model
                    if file.startswith(model_base_name):
                        source_path = os.path.join(root, file)
                        relative_path = os.path.relpath(source_path, content_path)
                        destination_path = os.path.join(new_model_path, relative_path)

                        # Ensure the destination directory exists
                        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                        shutil.copy(source_path, destination_path)
                        #print(f"File '{file}' copied successfully.")
                        existing_models.add(model)

        except Exception as e:
            logging.error(f"Error copying files for model '{model}': {str(e)}")
    else:
        missing_models_log.write(f"Model directory '{source_dir}' does not exist.\n")
    

for model in existing_models:
    model_count += 1
    model_base_name = os.path.basename(model).split('.')[0]
    qc_path = os.path.join(decompiled_models_path, os.path.dirname(model), model_base_name)
    #print (qc_path)
    #print (model_base_name)
    full_qc_path = os.path.join(qc_path, model_base_name + ".qc")
    if os.path.isfile(full_qc_path):
        qc_count += 1
        smdfile_matchs = set()
        with open(full_qc_path, 'r', encoding='utf-8') as qc_file:
            qc_content = qc_file.read()
            cdmaterials_match = re.search(r'\$cdmaterials\s+"(.*?)"', qc_content, re.IGNORECASE)
            if cdmaterials_match:
                cdmaterials_path = cdmaterials_match.group(1)
                #print(f"Model '{model}' - $cdmaterials: {cdmaterials_path}")
                texture_folder_count += 1
            smdfile_matches = [match.group(1) for match in re.finditer(r'studio\s+"(.*?)"', qc_content, re.IGNORECASE)]

            # Extract the content of the "skinfamilies" texture group block
            texturegroup_skinfamilies = re.search(r'\$texturegroup "skinfamilies"(.+?)\$', qc_content, re.DOTALL)

            if texturegroup_skinfamilies:
                block_content = texturegroup_skinfamilies.group(1)
            
                # Extract the names from within the block
                matches = re.findall(r'"(.*?)"', block_content)
                for match in matches:
                    texutre_path=os.path.join(cdmaterials_path,match+".vmt")
                    copy_texture(texutre_path)

            for smdfile_match in smdfile_matches:
                #print(smdfile_match)
                smd_count +=1
                smd_file = smdfile_match
                full_smd_path = os.path.join(decompiled_models_path, qc_path, smd_file)
                with open(full_smd_path, 'r', encoding='utf-8') as smd_content:
                    lines = smd_content.read().split('\n')  # Split the text into lines
                    start_index = None
                    textures_of_smd = set()

                    # Find the index of the line containing "triangles"
                    for i, line in enumerate(lines):
                        if "triangles" in line:
                            start_index = i
                            
                    if start_index is not None:
                        # Extract every fourth line after the line containing "triangles"
                        for i in range(start_index + 1, len(lines), 4):
                            texture = lines[i]
                            if not (texture == "end"):
                                if not texture in textures_of_smd:
                                    textures_of_smd.add(texture)
                                    #print(texture)
                                    smd_texture_count += 1
                                    texutre_path=os.path.join(cdmaterials_path,texture+".vmt")
                                    copy_texture(texutre_path)

    
#print (existing_models)

copy_map_required_files()

print (f"Models: {model_count}")
print (f"QC Files: {qc_count}")
print (f"Texture Folders: {texture_folder_count}")
print (f"SMD Count: {smd_count}")
print (f"SMD Texture Count: {smd_texture_count}")
#print (f"VMT Count: {vmt_count}")
#print (f"VTF Count: {vtf_count}")

missing_models_log.close()
print("Copy process completed. Check 'logs' folder in 'upload_textures' for log files.")