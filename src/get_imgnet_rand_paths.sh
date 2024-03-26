#!/bin/bash


# define a constant for number of image paths to get
NUM_IMG_PATHS=5000

# store current working dir
original_dir="$PWD"

# imagenet path
IMAGENET_PATH="eagle/datasets/ImageNet/ILSVRC/Data/CLS-LOC/train"

# change to the imagenet dir on polaris
cd $HOME

cd ..
cd ..

# find image paths given NUM_IMG_PATHS 
jpg_files=$(find "$IMAGENET_PATH" -type f -name '*.jpg' | shuf -n "$NUM_IMG_PATHS")

# create an array to store the paths
paths=()

# name of json file for storage
json_file = "imagenet_rand_$NUM_IMG_PATHS.json"

# get image path and store to paths array
for file in $jpg_files; do
    # Get the absolute path of the file
    absolute_path=$(realpath "$file")
    # Add the absolute path to the array
    paths+=("$absolute_path")
done

# switch to where image paths will be stored
cd $HOME/"$original_dir"/assets/polaris

# create a JSON file containing the paths
echo "{ \"paths\": [" > "./$json_file"
for path in "${paths[@]}"; do
    echo "  \"$path\"," >> "./$json_file"
done

# remove the trailing comma from the last entry
sed -i '$ s/,$//' "./$json_file"
echo "] }" >> "./$json_file"




