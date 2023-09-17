# Your Project Name

This project includes scripts to help with image processing. It contains PowerShell and shell scripts to automate image resizing and cropping.

## PowerShell Script (script.ps1)

This PowerShell script helps in resizing and cropping images. It provides various options to customize the image processing.

### Usage

Run the PowerShell script `script.ps1` with the following optional arguments:

- `-i, --input`: Path to the input folder containing images. (default: "input")

- `-o, --output`: Path to the output folder. (default: "output")

- `-d, --delete-existing-output`: Delete the existing output folder. (flag, default: false)

- `-r, --resolution`: Target resolution in the format 'width,height'. (default: "1920,1080")

- `-f, --max-factor-change`: Maximum allowed change factor for image proportions. (default: 0.1)

- `-v, --verbose`: Enable verbose mode. (flag, default: true)

**Example:**

```powershell
.\script.ps1 -i "path/to/input" -o "path/to/output" -d -r "1280,720" -f 0.2 -v
```

## Shell Script (script.sh)
This Bash script provides similar functionality to the PowerShell script for image processing, tailored for Linux environments.

### Usage
Run the shell script `script.sh` with the following optional arguments:

- `-i, --input`: Path to the input folder containing images. (default: "input")

- `-o, --output`: Path to the output folder. (default: "output")

- `-d, --delete-existing-output`: Delete the existing output folder. (flag, default: false)

- `-r, --resolution`: Target resolution in the format 'width,height'. (default: "1920,1080")

- `-f, --max-factor-change`: Maximum allowed change factor for image proportions. (default: 0.1)

- `-v, --verbose`: Enable verbose mode. (flag, default: true)

**Example:**

```console
user@machine:~$ ./script.sh -i "path/to/input" -o "path/to/output" -d -r "1280,720" -f 0.2 -v
```