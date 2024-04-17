import os
import subprocess
import json
from datetime import datetime
from shutil import move
from PIL import Image
from PIL.ExifTags import TAGS

def extract_image_exif(image_path):
    """
    Extracts EXIF metadata from an image file and adjusts the DateTimeOriginal by subtracting 5 hours and 30 minutes.
    
    Parameters:
        image_path (str): The path to the image file.
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            return exif_data
    except Exception as e:
        return None

def extract_video_creation_date(file_path):
    """
    Extracts the creation date from a video file and prints it.
    
    Parameters:
        file_path (str): The path to the video file.
    """
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        metadata = json.loads(result.stdout)
        if 'format' in metadata:
            creation_time = metadata['format'].get('tags', {}).get('creation_time')
            if creation_time:
                return creation_time
    return None

def create_year_subfolder(root_folder, year):
    """
    Creates a subfolder within the root folder based on the specified year.
    
    Parameters:
        root_folder (str): The root folder path.
        year (int): The year value.
    """
    year_folder = os.path.join(root_folder, f"M-{year}")
    os.makedirs(year_folder, exist_ok=True)
    return year_folder

def move_file_to_camera_or_digital(file_path):
    """
    Moves the file to 'Camera' folder if it contains EXIF metadata or 'Digital' folder otherwise.
    
    Parameters:
        file_path (str): The path to the file to be moved.
    """
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        metadata = extract_image_exif(file_path)
        if metadata:
            date_original = metadata.get(36867)
            if date_original:
                year = datetime.strptime(date_original, "%Y:%m:%d %H:%M:%S").year
                year_folder = create_year_subfolder(os.path.join(os.path.dirname(file_path), "Camera"), year)
                move(file_path, os.path.join(year_folder, os.path.basename(file_path)))
            else:
                move(file_path, os.path.join(os.path.dirname(file_path), "Digital", os.path.basename(file_path)))
        else:
            move(file_path, os.path.join(os.path.dirname(file_path), "Digital", os.path.basename(file_path)))
    elif file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
        creation_time = extract_video_creation_date(file_path)
        if creation_time:
            year = datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ").year
            year_folder = create_year_subfolder(os.path.join(os.path.dirname(file_path), "Camera"), year)
            move(file_path, os.path.join(year_folder, os.path.basename(file_path)))
        else:
            move(file_path, os.path.join(os.path.dirname(file_path), "Digital", os.path.basename(file_path)))
    else:
        print("Unsupported file format:", file_path)

def sort_files_by_creation_date(folder_path):
    """
    Sorts the files in each folder based on their creation date and time extracted from metadata.
    
    Parameters:
        folder_path (str): The path to the folder containing the image and video files.
    """
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            files_in_folder = [os.path.join(root, dir, file) for file in files]
            files_in_folder.sort(key=lambda x: os.path.getctime(x))
            for file_path in files_in_folder:
                print(f"Sorted: {file_path}")

def Test_PartA(folder_path):
    # Create 'Camera' and 'Digital' folders if they don't exist
    camera_folder = os.path.join(folder_path, "Camera")
    digital_folder = os.path.join(folder_path, "Digital")
    os.makedirs(camera_folder, exist_ok=True)
    os.makedirs(digital_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        move_file_to_camera_or_digital(file_path)
    
    # Sort files by creation date
    sort_files_by_creation_date(folder_path)


# if __name__ == "__main__":
#     folder_path = input("Enter the folder path containing the image and video files: ")
    
#     # Create 'Camera' and 'Digital' folders if they don't exist
#     camera_folder = os.path.join(folder_path, "Camera")
#     digital_folder = os.path.join(folder_path, "Digital")
#     os.makedirs(camera_folder, exist_ok=True)
#     os.makedirs(digital_folder, exist_ok=True)
    
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         move_file_to_camera_or_digital(file_path)
    
#     # Sort files by creation date
#     sort_files_by_creation_date(folder_path)

