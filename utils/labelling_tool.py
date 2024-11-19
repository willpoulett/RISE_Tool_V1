import subprocess
import pandas as pd
from PIL import Image
from IPython.display import display
import ipywidgets as widgets
from pathlib import Path
import random

def add_a_vote(col, image_id, label):
    df = pd.read_csv("labelling/personal_votes.csv", index_col = "ID")
    df.at[image_id,col] = label
    df.to_csv("labelling/personal_votes.csv")

def commit(x):
    subprocess.run(["git", "pull"])
    subprocess.run(['git', 'add', "labelling/personal_votes.csv"], check=True)
    subprocess.run(['git', 'commit', '-m', "update vote"], check=True)
    subprocess.run(["git","push"])
    return None

# Function to display the next image
def show_next_image(images, predictions, idx, shuffled_ids, random_list, img_widget, output_widget, progress_widget):
    
    if idx >= len(images):
        print("Saving...")
        #commit(None)
        print("Done")
        output_widget.clear_output()
        progress_widget.clear_output()
        with output_widget:
            display(widgets.HTML(f"""
                        <div style="text-align: center; font-size: 20px;">
                            <strong> Labelling Complete. Thank you!</strong>  
                        </div>"""))
        idx = 1

    
    new_id = shuffled_ids[idx]
    img_path = images[new_id]
    img = Image.open(Path(img_path))
    img = img.resize((256, 256))  # Resize image to 256x256
    
    random_id = random_list[new_id]
    
    img_widget.value = img_to_bytes(img)  # Update the image in the widget
    output_widget.clear_output()  # Clear previous output
    progress_widget.clear_output()

    if random_id == 1:
        with output_widget:
                display(widgets.HTML(f"""
                            <div style="text-align: center; font-size: 20px;">
                                <strong>The model has made the following prediction:</strong>  
                            </div>"""))
                    
                display(widgets.HTML(f"""
                        <div style="border: 1px solid #d3d3d3; padding: 10px; border-radius: 5px; background-color: #f9f9f9; text-align: center; font-size: 40px;"">
                            <span style="color: #0073e6;">{predictions[new_id]}</span> 
                        </div>"""))
            
    with output_widget:
        display(widgets.HTML(f"""
                        <div style="text-align: center; font-size: 20px;">
                            <strong>Please label this image</strong>  
                        </div>"""))
        
    with progress_widget:
        display(widgets.HTML(f"""
                            <div style="text-align: center; font-size: 20px;">
                                <strong>Progress:</strong>  
                            </div>"""))
        display(widgets.HTML(f"""
                            <div style="text-align: center; font-size: 20px;">
                                <strong>{idx+1}/{len(images)}</strong>  
                            </div>"""))


    def on_button_click(label):
        
        nonlocal idx # Declare as nonlocal to modify within this function
        
        new_id = shuffled_ids[idx]
        random_id = random_list[new_id]

        if random_id == 1:
            add_a_vote("user_vote_with_prediction",new_id, label)
            add_a_vote("user_vote_without_prediction",new_id, None)
        else:
            add_a_vote("user_vote_without_prediction",new_id, label)
            add_a_vote("user_vote_with_prediction",new_id, None)
        
        idx+=1
        show_next_image(images, predictions, idx, shuffled_ids, random_list, img_widget, output_widget, progress_widget)
            

    return on_button_click

# Helper function to convert PIL Image to bytes for displaying in ipywidgets
def img_to_bytes(img):
    from io import BytesIO
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def make_user_csv(id, preds):
    
    data = {
        'ID': id,
        'predictions': preds ,
        'user_vote_with_prediction': [None for i in range(len(id))],
        'user_vote_without_prediction': [None for i in range(len(id))]
        }
    
    pd.DataFrame(data).set_index('ID').to_csv("labelling/personal_votes.csv")


# Function to start the labeling process
def start_labeling(init_df, user_number):
    
    init_df = pd.read_csv(init_df)
    image_ids = init_df["ID"]
    image_paths = init_df["path"]
    predictions = init_df["prediction"]
    
    shuffled_ids = list(image_ids)
    random.shuffle(shuffled_ids)

    make_user_csv(image_ids, predictions)
    if user_number not in [0,1]:
        raise ValueError("Invalid ID_NUM, please seek help from Will")

    if user_number == 1:
         random_list = list([1 if x == 0 else 0 for x in init_df["random_number"]])
    else:
         random_list = list(init_df["random_number"])

    img_widget = widgets.Image()
    output_widget = widgets.Output(layout = widgets.Layout(height="170px"))
    
    
    buttons = [
        widgets.Button(description="Domestic Dog", layout = widgets.Layout(height="85px")),
        widgets.Button(description="Domestic Cat", layout = widgets.Layout(height="85px")),
        widgets.Button(description="Wildlife", layout = widgets.Layout(height="85px")),
    ]

    progress_widget = widgets.Output(layout = widgets.Layout(height="170px"))
    commit_button = widgets.Button(description=" Save / Commit ", layout = widgets.Layout(height="85px"), button_style = "success" )

    display(widgets.HBox([img_widget , widgets.VBox([output_widget, widgets.HBox(buttons)] ), widgets.VBox([commit_button, progress_widget])]))  # Display image and output side by side
    
    # Bind the on_button_click event to each button
    on_button_click = show_next_image(image_paths, predictions, 0, shuffled_ids, random_list, img_widget, output_widget, progress_widget)
    
    for button in buttons:
        button.on_click(lambda b: on_button_click(b.description))

    commit_button.on_click(commit)