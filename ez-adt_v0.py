#Easy AD EVO Tuner Alpha
#itsB34STW4RS 2023
#Hot Mess edition wip.

from tkinter import Tk, Label, Button, Entry, StringVar, ttk, Listbox, LabelFrame, BooleanVar, Radiobutton, Frame, DISABLED, NORMAL, messagebox
import os
import yaml
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from collections import OrderedDict

def represent_dict_order(self, data):
    return self.represent_mapping('tag:yaml.org,2002:map', data.items())

yaml.add_representer(OrderedDict, represent_dict_order)

def read_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.load(f, Loader=yaml.Loader)

def dict_to_ordered_dict(d, key_order):
    ordered_dict = OrderedDict((k, d[k]) for k in key_order if k in d)
    for k, v in d.items():
        if k not in ordered_dict:
            ordered_dict[k] = v
    return ordered_dict

# Training section

training_process = None

def run_training():
    global training_process
    interrupt_button.config(state=NORMAL)
    config_path = f"configs/training/{project_name_with_time}.yaml"  # Replace this with your actual config path
    try:
        training_process = subprocess.Popen(["python", "train.py", "--config", config_path])
    except Exception as e:
        print("failed to start training.")
        print(f"Error: {e}")
    finally:
        if training_process is not None:
           training_process.wait()
           save_button.config(state=NORMAL) #re-enable the 'start button'
           interrupt_button.config(state=DISABLED)

# Function to interrupt the training script
def interrupt_training():
    global training_process
    if training_process is not None:
        answer = messagebox.askyesno("Confirmation", "Do you really want to stop training?")
        if answer:
            training_process.terminate()
            print("\nTraining has been cancelled.")
            # re-enable the 'Start Training' button here
            save_button.config(state=NORMAL)
            interrupt_button.config(state=DISABLED)

# Function to start the training in a separate thread
def start_training_thread():
    train_thread = threading.Thread(target=run_training)
    train_thread.start()
    
def save_yaml():
    global project_name_with_time
    try:

        # Fetch the selected folder name from the dropdown
        selected_folder = folder_var.get()
        folder_path = os.path.join('data/', selected_folder)  # Construct the full path

        video_dir = folder_path

        # List video files
        video_extensions = [".mp4", ".avi", ".mkv", ".flv"]
        video_files = [f for f in os.listdir(video_dir) if any(f.endswith(ext) for ext in video_extensions)]

        # List all video files in the 'data/' directory
        video_files = [os.path.abspath(os.path.join(video_dir, f)) for f in os.listdir(video_dir) if any(f.endswith(ext) for ext in video_extensions)]

        # Update yaml_content with these video paths
        yaml_content['train_data']['video_path'] = video_files

        # Read caption.txt
        try:
            with open(os.path.join(folder_path, 'caption.txt'), 'r') as f:
                captions = [line.strip() for line in f.readlines() if line.strip()]

            if not captions:
                raise ValueError("Caption file is empty. Please populate it with text.")

            yaml_content['train_data']['prompt'] = captions
        except FileNotFoundError:
            raise FileNotFoundError("caption.txt not found. Please create it and try again.")

        # Update the editable fields before saving
    #    prompts = [entry.get() for entry in prompt_entries]
    #    yaml_content['train_data']['prompt'] = prompts
        yaml_content['train_data']['n_sample_frames'] = int(n_sample_frames_entry.get())
        yaml_content['train_data']['width'] = int(train_width_entry.get())
        yaml_content['train_data']['height'] = int(train_height_entry.get())
        yaml_content['train_data']['sample_start_idx'] = int(sample_start_idx_entry.get())
        yaml_content['train_data']['sample_frame_rate'] = int(sample_frame_rate_entry.get())
        
        # Fetch the chosen motion module file from the Combobox
        selected_motion_module_file = motion_module_var.get()

        # Construct the full path for the chosen motion module file
        motion_module_path = Path('models/Motion_Module/') / selected_motion_module_file

        # Standardize the directory path to use forward slashes
        standardized_motion_module_path = str(motion_module_path).replace('\\', '/')

        # Update yaml_content with the new motion_module path
        yaml_content['motion_module'] = standardized_motion_module_path

        selected_motion_module_version = str(motion_module_version_var.get())

        # Update model version
        yaml_content['motion_module_version'] = selected_motion_module_version

        # Update the boolean value in the YAML content
        yaml_content['train_whole_module'] = train_whole_module_var.get()

        key_order = ['video_path', 'prompt', 'n_sample_frames', 'width', 'height', 'sample_start_idx', 'sample_frame_rate']
        ordered_train_data = dict_to_ordered_dict(yaml_content['train_data'], key_order)
        yaml_content['train_data'] = ordered_train_data

        # Copy existing 'validation_data' entries
        existing_validation_data = yaml_content.get('validation_data', {}).copy()

        # Read validate.txt for validation_data
        try:
            with open(os.path.join(folder_path, 'validate.txt'), 'r') as f:
                validate_prompts = [line.strip() for line in f.readlines() if line.strip()]  # Remove empty lines and strip others
            existing_validation_data['prompts'] = validate_prompts  # Update the prompts in the existing_validation_data
        except FileNotFoundError:
            print("validate.txt not found in the selected folder.")  # Handle the case where the file does not exist, if needed

        # Update with new parameters from the validation_data_frame
        existing_validation_data['video_length'] = int(video_length_entry.get())
        existing_validation_data['width'] = int(val_width_entry.get())
        existing_validation_data['height'] = int(val_height_entry.get())
        existing_validation_data['num_inference_steps'] = int(num_inference_steps.get())
        existing_validation_data['temporal_context'] = int(temporal_context_entry.get())

        # Reorder and save back into yaml_content
        key_order_validation = ['prompts', 'video_length', 'width', 'height', 'num_inference_steps', 'temporal_context']
        ordered_validation_data = dict_to_ordered_dict(existing_validation_data, key_order_validation)

        # Add any keys that might not be in key_order_validation but are in existing_validation_data
        for k, v in existing_validation_data.items():
            if k not in ordered_validation_data:
                ordered_validation_data[k] = v

        # Finally update yaml_content['validation_data'] with ordered_validation_data
        yaml_content['validation_data'] = ordered_validation_data


        try:
            yaml_content['learning_rate'] = str(learning_rate_entry.get())
            yaml_content['checkpointing_steps'] = int(checkpointing_steps_entry.get())
            yaml_content['max_train_steps'] = int(max_train_steps_entry.get())
            yaml_content['validation_steps'] = int(validation_steps_entry.get())
        except ValueError:
            print("Error: Please enter valid numerical values for the training parameters.")



        # Fetch the project name from the Entry widget
        project_name = project_name_entry.get()

        # Get the current time in YYYYMMDD_HHMM format
        current_time = datetime.now().strftime("%Y%m%d_%H%M")

        # If the project name is empty, use a default name
        if not project_name:
            project_name = f"training"
        
        # Append the current time to the project name
        project_name_with_time = f"{project_name}_{current_time}"

        # Create the output path for the YAML configuration
        output_path = Path('configs') / 'training' / f"{project_name_with_time}.yaml"

        # Create a new directory inside 'models/Motion_Module/' with the project name
        new_output_dir = Path(f'models/Motion_Module/{project_name_with_time}')
        new_output_dir.mkdir(parents=True, exist_ok=True)

        # Standardize the directory path to use forward slashes
        standardized_output_dir = str(new_output_dir).replace('\\', '/')

        # Update yaml_content with the new output_dir
        yaml_content['output_dir'] = str(standardized_output_dir)



        # Key order for the entire YAML content
        key_order_yaml_content = ['train_data', 'validation_data', 'learning_rate', 'checkpointing_steps', 'max_train_steps', 'validation_steps', 'train_whole_module', 'motion_module']

        # Create an ordered dictionary for the entire YAML content
        ordered_yaml_content = dict_to_ordered_dict(yaml_content, key_order_yaml_content)

        with open(output_path, 'w') as f:
            yaml.dump(ordered_yaml_content, f, default_flow_style=False)
        
        # Disable start button
        save_button.config(state=DISABLED)
        
        # Start the training after saving the YAML
        thread = threading.Thread(target=run_training)
        thread.start()

    except FileNotFoundError:
        print("caption.txt not found. Please create it and try again.")
        messagebox.showwarning('Error', "caption.txt not found. Please create it and try again.")
    except ValueError as e:
        print(str(e))
        messagebox.showwarning('Error', str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messagebox.showwarning('Error', f"An unexpected error occurred: {e}")

        

# Initialize Tkinter root
root = Tk()
root.title("AD-Evo-Tuner Alpha")
root.configure(bg='black')
root.geometry("370x590")
root.minsize(width=370, height=590)
root.maxsize(width=370, height=590)


yaml_filepath = Path('configs') / 'training' / 'default' / 'default.yaml'
yaml_content = read_yaml(yaml_filepath)
train_whole_module_var = BooleanVar()

#MasterFrame
master_frame = Frame(root, padx=10, pady=10)
master_frame.grid(row=0, column=0, sticky='nsew')

# Create a LabelFrame
info_frame = LabelFrame(master_frame, text="Project Settings", padx=5, pady=5)  # padx and pady are internal paddings
info_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')  # External paddings

# Project Name
project_name_label = Label(info_frame, text="Project Name:")
project_name_label.grid(row=0, column=0, sticky='w')  # Set to row 0, column 0 inside the info_frame
project_name_entry = Entry(info_frame)
project_name_entry.grid(row=0, column=1)  # Set to row 0, column 1 inside the info_frame

#Motion Module
motion_module_var = StringVar()
motion_module_label = Label(info_frame, text="Motion Module:")
motion_module_label.grid(row=1, column=0, sticky='w')

# Get a list of .ckpt and .pth files
model_files = [f for f in os.listdir('models/Motion_Module') if f.endswith(('.ckpt', '.pth'))]

# Find the index of the first .ckpt file
first_ckpt_index = next((i for i, filename in enumerate(model_files) if filename.endswith('.ckpt')), None)

# Create and populate the Combobox
motion_module_dropdown = ttk.Combobox(info_frame, textvariable=motion_module_var)
motion_module_dropdown['values'] = model_files
motion_module_dropdown.grid(row=1, column=1)

# Set the first .ckpt file as the default value
if first_ckpt_index is not None:
    motion_module_dropdown.current(first_ckpt_index)


#Model Version
motion_module_version_var = StringVar()
motion_module_version_label = Label(info_frame, text="Module Version:")
motion_module_version_label.grid(row=2, column=0, sticky='w')

model_versions = ['V1', 'V2']

# Create and populate the Combobox
motion_module_version_dropdown = ttk.Combobox(info_frame, textvariable=motion_module_version_var)
motion_module_version_dropdown['values'] = model_versions
motion_module_version_dropdown.grid(row=2, column=1)

motion_module_version_dropdown.current(0)


# Get a list of folders in the data/ directory
folder_names = [f for f in os.listdir('data/') if os.path.isdir(os.path.join('data/', f))]

# Folder Dropdown
folder_var = StringVar()
folder_label = Label(info_frame, text="Dataset:")
folder_label.grid(row=3, column=0, sticky='w')

folder_dropdown = ttk.Combobox(info_frame, textvariable=folder_var)
folder_dropdown['values'] = folder_names
folder_dropdown.grid(row=3, column=1)

# Set the default value for the dropdown
if "default" in folder_names:
    folder_dropdown.current(folder_names.index("default"))
else:
    folder_var.set("None")  # You can set it to any default value or leave it empty



# Train Data Frame
train_data_frame = LabelFrame(master_frame, text="Train Data")
train_data_frame.grid(row=4, columnspan=2, padx=10, pady=10, sticky='nsew')  # Adjust row and columnspan according to your layout

# n_sample_frames
n_sample_frames_label = Label(train_data_frame, text="n_sample_frames:")
n_sample_frames_label.grid(row=0, column=0, sticky='w')
n_sample_frames_entry = Entry(train_data_frame)
n_sample_frames_entry.grid(row=0, column=1)
n_sample_frames_entry.insert(0, yaml_content.get('train_data', {}).get('n_sample_frames', '16'))

# Width
width_label = Label(train_data_frame, text="Width:")
width_label.grid(row=1, column=0, sticky='w')
train_width_entry = Entry(train_data_frame)
train_width_entry.grid(row=1, column=1)
train_width_entry.insert(0, yaml_content.get('train_data', {}).get('width', '512'))

# Height
height_label = Label(train_data_frame, text="Height:")
height_label.grid(row=2, column=0, sticky='w')
train_height_entry = Entry(train_data_frame)
train_height_entry.grid(row=2, column=1)
train_height_entry.insert(0, yaml_content.get('train_data', {}).get('height', '512'))

# Sample Start Index
sample_start_idx_label = Label(train_data_frame, text="Sample Start Index:")
sample_start_idx_label.grid(row=3, column=0, sticky='w')
sample_start_idx_entry = Entry(train_data_frame)
sample_start_idx_entry.grid(row=3, column=1)
sample_start_idx_entry.insert(0, yaml_content.get('train_data', {}).get('sample_start_idx', '0'))

# Sample Frame Rate
sample_frame_rate_label = Label(train_data_frame, text="Sample Frame Rate:")
sample_frame_rate_label.grid(row=4, column=0, sticky='w')
sample_frame_rate_entry = Entry(train_data_frame)
sample_frame_rate_entry.grid(row=4, column=1)
sample_frame_rate_entry.insert(0, yaml_content.get('train_data', {}).get('sample_frame_rate', '1'))

#Validation_Data Frame
validation_data_frame = LabelFrame(master_frame, text="Validation Data")
validation_data_frame.grid(row=6, columnspan=2, padx=10, pady=10, sticky='nsew')

#video length
video_length_label = Label(validation_data_frame, text="Video Length:")
video_length_label.grid(row=1, column=0, sticky='w')
video_length_entry = Entry(validation_data_frame)
video_length_entry.grid(row=1, column=1)
video_length_entry.insert(0, yaml_content.get('validation_data', {}).get('video_length', '16'))

# Width
width_label = Label(validation_data_frame, text="Width:")
width_label.grid(row=2, column=0, sticky='w')
val_width_entry = Entry(validation_data_frame)
val_width_entry.grid(row=2, column=1)
val_width_entry.insert(0, yaml_content.get('validation_data', {}).get('width', '512'))

# Height
height_label = Label(validation_data_frame, text="Height:")
height_label.grid(row=3, column=0, sticky='w')
val_height_entry = Entry(validation_data_frame)
val_height_entry.grid(row=3, column=1)
val_height_entry.insert(0, yaml_content.get('validation_data', {}).get('height', '512'))

# Number of Inference Steps
num_inference_steps = Label(validation_data_frame, text="Infer Steps:")
num_inference_steps.grid(row=4, column=0, sticky='w')
num_inference_steps = Entry(validation_data_frame)
num_inference_steps.grid(row=4, column=1)
num_inference_steps.insert(0, yaml_content.get('validation_data', {}).get('num_inference_steps', '20'))

#Temporal_Context
temporal_context_label = Label(validation_data_frame, text="Temporal Context:")
temporal_context_label.grid(row=5, column=0, sticky='w')
temporal_context_entry = Entry(validation_data_frame)
temporal_context_entry.grid(row=5, column=1)
temporal_context_entry.insert(0, yaml_content.get('validation_data', {}).get('temporal_context', '64'))

#Training Steps Frame
training_steps_frame = LabelFrame(master_frame, text="Training Steps")
training_steps_frame.grid(row=7, columnspan=2, padx=10, pady=10, sticky='nsew')

#Learning Rate
learning_rate_label = Label(training_steps_frame, text="Learning Rate:")
learning_rate_label.grid(row=0, column=0, sticky='w')
learning_rate_entry = Entry(training_steps_frame)
learning_rate_entry.grid(row=0, column=1)
learning_rate_entry.insert(0, yaml_content.get('learning_rate', '3.0e-05'))

#Checkpoint steps
checkpointing_steps_label = Label(training_steps_frame, text="Checkpoint Steps:")
checkpointing_steps_label.grid(row=1, column=0, sticky='w')
checkpointing_steps_entry = Entry(training_steps_frame)
checkpointing_steps_entry.grid(row=1, column=1)
checkpointing_steps_entry.insert(0, yaml_content.get('checkpointing_steps', '100'))

#Training Steps
max_train_steps_label = Label(training_steps_frame, text="Training Steps:")
max_train_steps_label.grid(row=2, column=0, sticky='w')
max_train_steps_entry = Entry(training_steps_frame)
max_train_steps_entry.grid(row=2, column=1)
max_train_steps_entry.insert(0, yaml_content.get('max_train_steps', '1000'))

#Validationg Steps
validation_steps_label = Label(training_steps_frame, text="Validate Steps:")
validation_steps_label.grid(row=3, column=0, sticky='w')
validation_steps_entry = Entry(training_steps_frame)
validation_steps_entry.grid(row=3, column=1)
validation_steps_entry.insert(0, yaml_content.get('validation_steps', '10000'))

# Create a label to describe the radio buttons
radio_label = Label(training_steps_frame, text="Train Whole Module:")
radio_label.grid(row=4, column=0, sticky='w')

# Create radio buttons
rb_true = Radiobutton(training_steps_frame, text="True", variable=train_whole_module_var, value=True)
rb_false = Radiobutton(training_steps_frame, text="False", variable=train_whole_module_var, value=False)

# Set the default value, if needed
train_whole_module_var.set(yaml_content.get('train_whole_module', False))

# Place the radio buttons in the grid
rb_true.grid(row=4, column=1)
rb_false.grid(row=4, column=2)


# Video Files Listbox
#video_files_listbox = Listbox(root, height=10, width=50)
#video_files_listbox.grid(row=0, column=2, rowspan=10)


#for video in video_files:
#    video_files_listbox.insert("end", video)

# Dynamic Prompts based on the number of video files
#prompt_entries = []
#next_row = 5  # Assuming the last widget in `train_data_frame` was at row 4
#for idx, video in enumerate(video_files):
#    prompt_label = Label(train_data_frame, text=f"Prompt for {video}:")
#    prompt_label.grid(row=next_row, column=0, sticky='w')
#    prompt_entry = Entry(train_data_frame, width=75)
#    prompt_entry.grid(row=next_row, column=1)
#    prompt_entries.append(prompt_entry)

next_row = 9
next_row += 1  # Increment the row index for the next set of widgets

# Save Button
save_button = Button(master_frame, text="Start Training", command=save_yaml)
save_button.grid(row=next_row, column=1)  # Placing it after all the prompt entry fields

# Interupt Button
interrupt_button = Button(master_frame, text="Stop Training", command=interrupt_training, state=DISABLED)
interrupt_button.grid(row=next_row, column=0)

root.mainloop()
