# Example PowerShell script (script.ps1)
param(
    [string]$i = 'input',
    [string]$output = "output",
    [bool]$delete_existing_output_folder = $false,
    [string]$resolution = "1920,1080",
    [float]$max_factor_change = 0.1,
    [bool]$verbose = $False
)

# Output provided parameters
Write-Host "Input: $i"
Write-Host "Output: $output"
Write-Host "Delete existing output folder: $delete_existing_output_folder"
Write-Host "Resolution: $resolution"
Write-Host "Max factor change: $max_factor_change"
Write-Host "Verbose: $verbose"
Write-Host " "

# Create and activate the virtual environment
Write-Host "Creating and activating the virtual environment..."
python -m venv .venv
.venv\Scripts\Activate.ps1
Write-Host " "

# Install the required packages
Write-Host "Installing the required packages..."
pip install -r requirements.txt
Write-Host " "

# Run the app.py with the specified input folder
Write-Host "Running the app.py with the specified input folder..."
# Construct the command to run app.py based on the provided parameters
$appCommand = "python app.py -i $i -o $output -r $resolution -f $max_factor_change"
# Add -d flag if delete_existing_output_folder is true
if ($delete_existing_output_folder) {
    $appCommand += " -d"
}
# Add -v flag if verbose is true
if ($verbose) {
    $appCommand += " -v"
}
# Run the app.py with the specified input folder and other parameters
Write-Host "$appCommand"
Invoke-Expression -Command $appCommand
Write-Host " "

# Deactivate the virtual environment
Write-Host "Deactivating the virtual environment..."
deactivate
Write-Host " "

# Deleting the virtual environment
Write-Host "Deleting the virtual environment..."
Remove-Item -Path ".venv" -Recurse -Force
Write-Host " "

Write-Host "Script execution completed."
