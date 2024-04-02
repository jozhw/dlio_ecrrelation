#!/bin/bash



# store current working dir
original_dir="$PWD"

# imagenet path
IMAGENET_PATH="eagle/datasets/ImageNet/ILSVRC/Data/CLS-LOC/train"

# change to the imagenet dir on polaris
cd $HOME

cd ..
cd ..

cd eagle/datasets/ImageNet/ILSVRC/Data/CLS-LOC/train || echo "Could not find $IMAGENET_PATH"

current_path=$(pwd)
echo "Current Path: $current_path"


# find image paths given NUM_IMG_PATHS 
jpg_files=$(find .  -type f -name '*.JPEG' )

# create an array to store the paths
paths=()

# make dated file
date=$(date +'%Y-%m-%d')

# name of json file for storage
json_file="all_imagenet_paths_on_${date}.json"

# get image path and store to paths array
for file in $jpg_files; do
    # Get the absolute path of the file
    absolute_path=$(realpath "$file")
    # Add the absolute path to the array
    paths+=("$absolute_path")
done

# switch to where image paths will be stored
cd "$original_dir"/assets/polaris/img_paths


# create a JSON file containing the paths
echo "{ \"paths\": [" > "$json_file"
for path in "${paths[@]}"; do
    echo "  \"$path\"," >> "$json_file"
done

# remove the trailing comma from the last entry
sed -i '$ s/,$//' "$json_file"
echo "] }" >> "$json_file"




