#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (use sudo)." >&2
    exit 1
fi

# Create the directory if it doesn't exist
mkdir -p /opt/splicer

# Prompt for user input
read -p "Enter the Splice directory path: " splice
read -p "Enter the Final directory path: " final

# Write the config file with user inputs
cat <<EOF > /opt/splicer/config.json
{
  "splice": "$splice",
  "final": "$final"
}
EOF

# Change ownership of the config file
chown $(whoami):staff /opt/splicer/config.json

echo "Configuration file created at /opt/splicer/config.json with the following values:"
echo "Splice Directory: $splice"
echo "Final Directory: $final"
