from PIL import Image
import os, re
from pathlib import Path

def get_file_key(filename):
    key = re.sub("[^0-9]", "", filename)
    if bool(re.search(r'\d', filename)):
        return int(key)

def sort_filenames(all_files):
    filenames_sorted = []
    original_filenames = {}
    for full_filename in all_files:
        filename, file_extension = os.path.splitext(full_filename)

        # Save all the files names to be sorted
        filenames_sorted.append(filename)
        # Save original full filename in a dictionary for later retrieval
        original_filenames[filename] = full_filename

    # Sort the list using key
    filenames_sorted.sort(key=get_file_key)
    filenames = []
    for key in filenames_sorted:
        filenames.append(original_filenames[key])

    return filenames

def CreateCollage(outputFolder: str, folder: str, count: int, imageName: str):
    image_list = []
    
    height = 0
    width = 0
    index = 0
    # Create an ordered list for all items in the folder
    fileList = [None] * (count)
    for filename in os.listdir(folder):
        if not filename == 'output':
            fileList[index] = filename
            index += 1
    sortedFiles = sort_filenames(fileList)

    index = 0
    # Rename the items
    for filename in sortedFiles:
        if not filename == 'output':
            img = Image.open(folder + filename)
            image_list.append(img)
    
    # Set final image size
    finalImage = Image.new("RGBA", ((round(count / 10) * img.size[0]) ,(round(count / 10) * img.size[1])))

    # Create collage
    for num in range(round(count / 10)):
        for num2 in range(round(count / 10)):
            if index < len(image_list):
                finalImage.paste(image_list[index], (width, height))
                width += img.size[0] # 1200
                index += 1
        height += img.size[1]
        width = 0      

    finalImage.save(outputFolder + imageName + '.png', 'PNG')

# Get directory
home = str(Path.home()) + '\\'

# Get folder location and image name input from user
folderLocation = str(input("Enter images file location: "))
imageName = str(input("Enter a name to give the file: "))
folder = home + folderLocation + '\\'

# Checking if the directory demo_folder 
# Exist or not.
if not os.path.exists(folder+"output\\"):
    # If the folder directory is not present 
    # Then create it.
    os.makedirs(folder+"output\\")
    outputFolder = folder+"output\\"
else:
    outputFolder = folder+"output\\"

# Get total items in folder
rangeCount = 0
for i in os.listdir(folder):
    if not i == 'output':
        rangeCount += 1

CreateCollage(outputFolder, folder, rangeCount, imageName)
