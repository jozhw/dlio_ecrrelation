#!/bin/bash

# dir path
DIRECTORY="./assets"

# check if dir exists
if [ -d "$DIRECTORY" ]; then
    # delete .npz files
    find "$DIRECTORY" -type f -name "*.npz" -delete

    echo "Deleted all .npz files in $DIRECTORY"

else
    echo "Directory $DIRECTORY does not exist."

fi
