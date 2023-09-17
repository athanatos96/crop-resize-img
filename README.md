# Your Project Name

This project includes scripts to help with image processing. It contains PowerShell and shell scripts to automate image resizing and cropping.

It resizes all input images to the desire resolution. If a given image don’t have the same aspect ratio, it will change the aspect ratio up to the max-factor-change, if the change in the aspect ratio needs to be bigger than the max allowed one, it will crop the image to an allowed aspect ratio that don’t break the max-factor-change.

## Functionality

This repository provides scripts for automating image resizing and cropping. The scripts are available in both PowerShell and Bash (for Windows and Linux, respectively). The image processing scripts offer the following capabilities:

- **Resizing Images:** The scripts allow you to resize images to a target resolution, specified as width and height.

- **Cropping Images:** If the original image proportions vary significantly from the target resolution, the scripts will trim or cut the image to meet an specified proportions, that don't break the max-factor-change

- **Customization:** You can customize the target resolution and the maximum allowed change factor for image proportions.

**For example:**
The target resolution is `1920 x 1080`, this result in an aspect ratio of `1.777...`
- Img size is `8000 x 4571` -> Aspect ratio `~1.75` -> Change in aspect ratio needed `~0.0155` -> which is `< than` the max-factor-change of 0.1. -> `No crop` -> Only resize to `1920 x 1080`
- Img Size is `8000 x 3000` -> Aspect ratio `~2.66` -> Change in aspect ratio needed  `0.5`    -> which is `> than` the max-factor-change of 0.1. -> `Crop` to `5866 x 3000`, New aspect ratio `1.95`, New change in aspect ratio needed `0.1` -> Then resize to `1920 x 1080`
- Img Size is `1024 x 1024` -> Aspect ratio  `1.00` -> Change in aspect ratio needed `~0.4374` -> which is `> than` the max-factor-change of 0.1. -> `Crop` to `1024 x  640`, New aspect ratio `1.6`, New change in aspect ratio needed `0.1` -> Then resize to `1920 x 1080`

The aspect ratio boundaries (max and min) that are allowed without a crop, can be defined using the formula:

```math
(\pm \&nbsp; \text{{max\_change\_factor}} \times \frac{{\text{{target\_width}}}}{{\text{{target\_height}}}}) + \frac{{\text{{target\_width}}}}{{\text{{target\_height}}}} = \text{{Aspect ratio boundaries}}
```

Here:
- \(+\) indicates the upper boundary for aspect ratio.
- \(-\) indicates the lower boundary for aspect ratio.

### Going into the rabbit hole of the aspect ratios and max-factor-change
_This section goes in depth  explaining the aspect ratio and how to choose the best one_

Here's an example of a table illustrating the impact on the upper and lower limits of the max change factor for various values of the max change factor, with a target resolution of 1920x1080:
| Max Change Factor | Lower Bound Aspect Ratio    | Upper Bound Aspect Ratio |
|-------------------|-----------------------------|--------------------------|
| 0                 |  1.7778 ( 1920/1080)        | 1.7778 (1920/1080)       |
| 0.05              |  1.6889 ( 1920/1137)        | 1.8667 (2016/1080)       |
| 0.1               |  1.6000 ( 1920/1200)        | 1.9556 (2112/1080)       |
| 0.2               |  1.4222 ( 1920/1350)        | 2.1333 (2304/1080)       |
| 0.5               |  0.8889 ( 1920/2160)        | 2.6667 (2880/1080)       |
| 1.0               |  0.0000 ( 1920/&infin;)     | 3.5556 (3840/1080)       |
| 2.0               | -1.7778 ( 1920/-1080)       | 5.3333 (5760/1080)       |
| &infin;           | -&infin;( 1920/0)           | &infin;(&infin;/1080)    |

How can it be that the lower bound aspect ratio goes to 0 and negative. This means that the lower aspect ratio disappears, when it gets to 0, meaning that all restrictions of on the height disappear.

As an image height increase, the aspect ratio will tend to 0, but it will never reach it, so with a `Max change factor >=1.0` will result in no cropping for arbitrarily large heights. We can see that if the factor is 2, the height has wrap around infinity into the negative numbers, which means that any height is allowed.

We see no such behavior for the upper bound. As the factor increases so does the upper bound, but not as fast. In fact, if we want the width to grow to infinity without a crop the factor will need to be infinity.

This means that there is an imbalance. As the code filters more exclusively the horizontal images than the vertical ones. For a factor of >=1, there will be no vertical crop and there will be horizontal crop, at an aspect ratio of 1.9556

This is because all the vertical aspect ratios are mapped from `0-1` and all the horizontal aspect ratios are mapped from `1-&infin;`. 

I will need to change the code to reflect this imbalance in the ratios, but as long as you don’t have a really weird shape image, and a big Max Change Factor, no problems will happen (It will take time to change this and it works good enough for my needs, but if you want to change it I will recommend 2 different max factors, one for horizontal and one for vertical images, that way you can map the aspect ratios as you want). `I will recommend a Max Change Factor of <=0.2`


## PowerShell Script (script.ps1)

This PowerShell script helps in resizing and cropping images. It provides various options to customize the image processing.

### Usage

Run the PowerShell script `script.ps1` with the following optional arguments:

- `-i`: Path to the input folder containing images. (default: "input")

- `-o, --output`: Path to the output folder. (default: "output")

- `-d, --delete_existing_output`: Delete the existing output folder. (flag, default: false)

- `-r, --resolution`: Target resolution in the format 'width,height'. (default: "1920,1080")

- `-m, --max_factor_change`: Maximum allowed change factor for image proportions. (default: 0.1)

- `-v, --verbose`: Enable verbose mode. (flag, default: false)

**Example:**

<!-- .\run_app.ps1 -i "path/to/input" -o "path/to/output" -d -r "1280,720" -f 0.2 -v -->
```powershell
.\run_app.ps1 -i "path/to/input" -o "path/to/output" -d $True -r "1280,720" -m 0.2 -v $True
```

## Shell Script (script.sh)

This Bash script provides similar functionality to the PowerShell script for image processing, tailored for Linux environments.

_The shell script hasn't been tested_

### Usage
Run the shell script `script.sh` with the following optional arguments:

- `-i, --input`: Path to the input folder containing images. (default: "input")

- `-o, --output`: Path to the output folder. (default: "output")

- `-d, --delete-existing-output`: Delete the existing output folder. (flag, default: false)

- `-r, --resolution`: Target resolution in the format 'width,height'. (default: "1920,1080")

- `-f, --max-factor-change`: Maximum allowed change factor for image proportions. (default: 0.1)

- `-v, --verbose`: Enable verbose mode. (flag, default: false)

**Example:**

```console
user@machine:~$ ./run_app.sh -i "path/to/input" -o "path/to/output" -d -r "1280,720" -f 0.2 -v
```
