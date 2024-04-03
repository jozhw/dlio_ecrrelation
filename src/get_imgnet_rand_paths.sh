#!/bin/bash

# Define a constant for the number of image paths to get
NUM_IMG_PATHS=100000

# Store the original working directory
original_dir="$PWD"

# ImageNet path
IMAGENET_PATH="eagle/datasets/ImageNet/ILSVRC/Data/CLS-LOC/train"

# Change to the ImageNet directory
cd "$HOME/../.." || { echo "Could not find $IMAGENET_PATH"; exit 1; }

# Print current path
current_path=$(pwd)
echo "Current Path: $current_path"

# Find image paths given NUM_IMG_PATHS
jpg_files=$(find . -type f -name '*.JPEG' | shuf -n "$NUM_IMG_PATHS")

# Use GNU Parallel to process image paths in parallel
parallel -j64 realpath {} ::: $jpg_files | \
    shuf | \
    head -n "$NUM_IMG_PATHS" | \
    parallel -j64 'echo {} >> "$original_dir/assets/polaris/img_paths/$date/$json_file"'

# Name of the JSON file for storage
json_file="imagenet_rand_$NUM_IMG_PATHS.json"

# Switch to where image paths will be stored
cd "$original_dir/assets/polaris/img_paths" || { echo "Could not switch directory"; exit 1; }

# Make dated directory
date=$(date +'%Y-%m-%d')

mkdir -p "$date" || echo "Directory $date already exists"

# Create a JSON file containing the paths
echo "{ \"paths\": [" > "$date/$json_file"

# Concatenate all the partial JSON files into the final JSON file
cat $date/* >> "$date/$json_file"

# Remove the trailing comma from the last entry
sed -i '$ s/,$//' "$date/$json_file"
echo "] }" >> "$date/$json_file"
