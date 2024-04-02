#!/bin/bash


# define a constant for number of image paths to get
NUM_IMG_PATHS=200

# store current working dir
original_dir="$PWD"


# find image paths given NUM_IMG_PATHS 
jpg_files=$(find ./assets/local/uncompressed_imgs  -type f -name '*.jpg' | shuf -n "$NUM_IMG_PATHS")

# create an array to store the paths
paths=()

# name of json file for storage
json_file="local_rand_$NUM_IMG_PATHS.json"

# get image path and store to paths array
for file in $jpg_files; do
    # Get the absolute path of the file
    absolute_path=$(realpath "$file")
    # Add the absolute path to the array
    paths+=("$absolute_path")
done

# switch to where image paths will be stored
cd "$original_dir"/assets/local/img_paths

# make dated directory
date=$(date +'%Y-%m-%d')

mkdir "$date" || echo "Directory $date already exits"

# create a JSON file containing the paths
echo "{ \"paths\": [" > "$date/$json_file"
for path in "${paths[@]}"; do
    echo "  \"$path\"," >> "$date/$json_file"
done

# remove the trailing comma from the last entry using ex
ex -sc '$s/,$//' -cx "$date/$json_file"
echo "] }" >> "$date/$json_file"




