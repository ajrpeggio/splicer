#!/bin/bash

# Create the directory if it doesn't exist
splicer="${HOME}/.splicer"
mkdir -p ${splicer}
config="${splicer}/config.json"

# Prompt for user input
read -p "Enter the Splice directory path: " splice
read -p "Enter the Final directory path: " final

# Write the config file with user inputs
cat <<EOF > ${config}
{
  "splice": "$splice",
  "final": "$final"
}
EOF

# Change ownership of the config file
chown $(whoami):staff ${config}

echo "Configuration file created at ${config} with the following values:"
echo "Splice Directory: $splice"
echo "Final Directory: $final"
