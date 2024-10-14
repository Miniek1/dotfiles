#!/bin/bash

# Define the screenshot folder
SCREENSHOT_FOLDER="/home/miniek/Pictures"

# Take a screenshot and save it
SCREENSHOT_FILE="${SCREENSHOT_FOLDER}/$(date +'%Y-%m-%d_%H-%M-%S').png"
grimblast --freeze copysave area "$SCREENSHOT_FILE"

# Send a notification with the screenshot as an icon and two buttons: Open and Delete
ACTION=$(notify-send "Screenshot Taken" \
                    "Screenshot saved to $SCREENSHOT_FILE" \
                    --hint=int:transient:1 \
                    --icon="$SCREENSHOT_FILE" \
                    --action="Open" \
                    --action="Delete")

# Handle the action based on the button clicked
if [[ $ACTION == "0" ]]; then
    # Open the screenshot (using xdg-open to open with the default image viewer)
    xdg-open "$SCREENSHOT_FILE"
elif [[ $ACTION == "1" ]]; then
    # Delete the screenshot
    rm "$SCREENSHOT_FILE"
    notify-send "Screenshot Deleted"
fi
