import os
from shutil import copy2

from Sort_by_date import Test_PartA

def copy_media_files(input_folder, output_folder):
    """
    Copy image and video files from input folder and its subfolders to output folder.
    
    Parameters:
        input_folder (str): Path to the input folder.
        output_folder (str): Path to the output folder.
    """
    # List of supported image and video file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
    
    # Traverse through all subfolders and copy image and video files
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            
            # Check if the file extension is in the list of supported extensions
            if file_extension in image_extensions or file_extension in video_extensions:
                # Copy the file to the output folder
                copy2(file_path, output_folder)
                print(f"Copied {file} to {output_folder}")

if __name__ == "__main__":
    # Prompt user for input folder and output folder
    input_folder = input("Enter the path to the input folder: ")
    output_folder = input("Enter the path to the output folder: ")
    
    # Call function to copy media files
    copy_media_files(input_folder, output_folder)

    # Call function to copy media files
    Test_PartA(output_folder)