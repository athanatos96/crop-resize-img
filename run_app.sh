#!/bin/bash

# Example Bash script (script.sh)
# Set default values
input="input"
output="output"
delete_existing_output_folder=false
resolution="1920,1080"
max_factor_change=0.1
verbose=false

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -i|--input)
            input="$2"
            shift
            shift
            ;;
        -o|--output)
            output="$2"
            shift
            shift
            ;;
        -d|--delete-existing-output)
            delete_existing_output_folder=true
            shift
            ;;
        -r|--resolution)
            resolution="$2"
            shift
            shift
            ;;
        -f|--max-factor-change)
            max_factor_change="$2"
            shift
            shift
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        *)
            # Unknown option
            shift
            ;;
    esac
done

# Output provided parameters
echo "Input: $input"
echo "Output: $output"
echo "Delete existing output folder: $delete_existing_output_folder"
echo "Resolution: $resolution"
echo "Max factor change: $max_factor_change"
echo "Verbose: $verbose"
echo " "

# Create and activate the virtual environment
echo "Creating and activating the virtual environment..."
python -m venv .venv
source .venv/bin/activate
echo " "

# Install the required packages
echo "Installing the required packages..."
pip install -r requirements.txt
echo " "

# Run the app.py with the specified input folder
echo "Running the app.py with the specified input folder..."
app_command="python app.py -i $input -o $output -r $resolution -f $max_factor_change"
if [ "$delete_existing_output_folder" = true ] ; then
    app_command="$app_command -d"
fi
if [ "$verbose" = true ] ; then
    app_command="$app_command -v"
fi
echo "$app_command"
$app_command
echo " "

# Deactivate the virtual environment
echo "Deactivating the virtual environment..."
deactivate
echo " "

# Deleting the virtual environment
echo "Deleting the virtual environment..."
rm -rf .venv
echo " "

echo "Script execution completed."