import glob

def init(file_names = ["edge_case_images","non_edge_case_images"]):

    image_paths = []
    
    for folder in file_names:
        fileList = glob.glob(f'{folder}/*')
        image_paths.extend(fileList)


    return image_paths