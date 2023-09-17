from PIL import Image
import os
import shutil
from tqdm import tqdm
import argparse
import time
import sys

def resize_and_save_image(input_path, output_path, target_size, max_change_factor, verbose = True):
    """
    Resize the input image based on the target size and max change factor and save it.

    Parameters:
    input_path (str): Path to the input image.
    output_path (str): Path to save the resized image.
    target_size (tuple): Target size in the format (width, height).
    max_change_factor (float): Maximum allowed change factor for image proportions.
    verbose (bool): Allow prints or not
    
    Returns:
    None
    """
    
    if verbose: tqdm.write(" ") # make a new line to indicate the change in img procesed
    tqdm.write(f"Img '{input_path}' -> '{output_path}'")
    
    # Open the image
    img = Image.open(input_path)

    # Get the current image size (width, height)
    current_size = img.size
    current_width, current_height = current_size

    # Calculate the current aspect ratio
    current_aspect_ratio = current_width / current_height

    # Calculate the target aspect ratio
    target_width, target_height = target_size
    target_aspect_ratio = target_width / target_height

    # Calculate the change factor in aspect ratio
    change_factor = abs((current_aspect_ratio - target_aspect_ratio) / target_aspect_ratio)
    
    # Check if change factor is within the max change factor
    if change_factor <= max_change_factor:
        if verbose: tqdm.write(f"No crop Needed, img reslution {current_size} px, aspect ratio {current_aspect_ratio} | target resolution {target_size} px, aspect ratio {target_aspect_ratio} | Change factor {change_factor} smaller than {max_change_factor}")
        # Resize the image to the target size
        img_resized = img.resize(target_size, resample=Image.BICUBIC)
        img_resized.save(output_path)
    else:
        # Crop needed
        if verbose: tqdm.write(f"Crop needed, Img resolution {current_size} px, aspect ratio {current_aspect_ratio} | target resolution {target_size} px, aspect ratio {target_aspect_ratio} | Change factor {change_factor} greater than {max_change_factor}")
        # Calculate new dimensions to fit within the max change factor
        if current_aspect_ratio > target_aspect_ratio:
            # Crop Horizontally 
            if verbose: tqdm.write(f"Crop Horizontally")
            
            # Calculate the new aspect ratio that respect the max_change_factor
            new_aspect_ratio = round(( max_change_factor * target_aspect_ratio ) + target_aspect_ratio, 15 ) # 1.955... Is the new aspect ratio for vertical images, with a target asp of 1.777... and a max factor change of 0.1
            new_change_factor = abs((new_aspect_ratio - target_aspect_ratio) / target_aspect_ratio)
            if verbose: tqdm.write(f"New aspect ratio {new_aspect_ratio} | New Change factor {new_change_factor}")
            
            
            # Crop the img base on the new aspect ratio
            new_width = int(current_height * new_aspect_ratio)
            left_offset = (current_width - new_width) // 2
            img_cropped = img.crop((left_offset, 0, left_offset + new_width, current_height))
            if verbose: tqdm.write(f"New Size {(new_width, current_height)} px, aspect ration {new_width / current_height} | Cropped each size by {left_offset} px")
        else:
            # Crop Vertically
            if verbose: tqdm.write(f"Crop Vertically")
            
            # Calculate the new aspect ratio that respect the max_change_factor
            new_aspect_ratio = round(( -max_change_factor * target_aspect_ratio ) + target_aspect_ratio, 15 ) # 1.5999... Is the new aspect ratio for vertical images, with a target asp of 1.777... and a max factor change of 0.1
            new_change_factor = abs((new_aspect_ratio - target_aspect_ratio) / target_aspect_ratio)
            if verbose: tqdm.write(f"New aspect ratio {new_aspect_ratio} | New Change factor {new_change_factor}")
            
            # Crop the img base on the new aspect ratio
            new_height = int(current_width / new_aspect_ratio)
            top_offset = (current_height - new_height) // 2
            img_cropped = img.crop((0, top_offset, current_width, top_offset + new_height))
            if verbose: tqdm.write(f"New Size {(current_width, new_height)} px, aspect ration {current_width / new_height} | Cropped the top and bottom by {top_offset} px")

        # Resize the cropped image to the target size
        img_resized = img_cropped.resize(target_size, resample=Image.BICUBIC)
        img_resized.save(output_path)

def resize_images_in_folder(input_folder, output_folder=None, resolution = (1920, 1080), max_change_factor = 0.1, delete_existing_output_folder = False, verbose = True):
    """
    Resize and save images in the input folder.

    Parameters:
    input_folder (str): Path to the input folder containing images.
    output_folder (str): Path to the output folder. If None, a subfolder named 'output' will be created.
    delete_existing_output_folder (bool): Whether to delete the existing output folder if it already exists.
    resolution (tuple): Target resolution in the format (width, height).
    max_change_factor (float): Maximum allowed change factor for image proportions.
    verbose (bool): Allow prints or not
    
    Returns:
    None
    """
    if not os.path.isdir(input_folder):
        print(f"Not a valid input folder, {input_folder}")
        sys.exit(-1)        
    # Set default output folder
    if output_folder is None:
        output_folder = os.path.join(input_folder, 'output')

    # Delete the output folder if it exists
    if delete_existing_output_folder and os.path.exists(output_folder):
        if verbose: print(f"Deleting existing output folder: {output_folder}")
        shutil.rmtree(output_folder)
        
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the input folder
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for file in tqdm(files, desc="Processing images"):
        input_path = os.path.join(input_folder, file)
        _, ext = os.path.splitext(file)

        # Check if the file is an image (has a valid extension)
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            output_file = os.path.splitext(file)[0] + '_resize_and_cropped' + ext
            output_path = os.path.join(output_folder, output_file)

            # Call the resize_and_save_image function
            resize_and_save_image(input_path, output_path, resolution, max_change_factor, verbose)

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Resize and crop images in a folder")
    optional = parser._action_groups.pop() # Edited this line
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", type=str, required=True, help="Path to the input folder containing images")
    optional.add_argument("-o", "--output", type=str, help="Path to the output folder")
    optional.add_argument("-d", "--delete_existing_output_folder", action="store_true", default = False, help="Delete existing output folder if already exist")
    optional.add_argument("-r", "--resolution", type=str, default = '1920,1080', help="Target resolution in the format 'width,height'")
    optional.add_argument("-f", "--max_factor_change", type=float, default = 0.1, help="Maximum allowed change factor for image proportions")
    optional.add_argument("-v", "--verbose", action="store_true", default = False, help="Verbose mode")
    parser._action_groups.append(optional) # added this line
    
    # Parse arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(-1)

    # Convert resolution to tuple if provided
    if args.resolution:
        args.resolution = tuple(map(int, args.resolution.split(',')))
    
    #f'{args.input}/output/' if args.output else args.output
    print("-"*100)
    print(f"input: {args.input}, type {type(args.input)}")
    print(f"output: {f'{args.input}/output/' if args.output is None else args.output}, type {type('')}")
    print(f"delete_existing_output_folder: {args.delete_existing_output_folder}, type {type(args.delete_existing_output_folder)}")
    print(f"resolution: {args.resolution}, type {type(args.resolution)}")
    print(f"max_factor_change: {args.max_factor_change}, type {type(args.max_factor_change)}")
    print(f"verbose: {args.verbose}, type {type(args.verbose)}")
    print("-"*100)
    
    # Measure execution time
    start_time = time.time()

    # Call the resize_images_in_folder function
    resize_images_in_folder(input_folder = args.input, 
                            output_folder = args.output, 
                            delete_existing_output_folder = args.delete_existing_output_folder, 
                            resolution = args.resolution, 
                            max_change_factor = args.max_factor_change, 
                            verbose = args.verbose)

    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time

    if args.verbose:
        print(f"\nTotal execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()