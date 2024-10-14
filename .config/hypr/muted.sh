#!/bin/bash

# Get the default source name
default_source=$(pactl info | grep "Default Source" | awk '{print $3}')

# Toggle the microphone mute status
pactl set-source-mute "$default_source" toggle

# Get the mute status of the default source
mute_status=$(pactl list sources | grep -A 15 "$default_source" | grep "Mute:" | head -n 1 | awk '{print $2}')

# Check if the microphone is muted or not and send a notification
if [[ $mute_status == "yes" ]]; then
    notify-send "Microphone Muted"
elif [[ $mute_status == "no" ]]; then
    notify-send "Microphone Unmuted"
else
    notify-send "Error: Unable to get mute status"
fi
