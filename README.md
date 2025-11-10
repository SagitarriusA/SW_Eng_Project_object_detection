# SW_Eng_Project_object_detection
This is a semester project for the Software Engineering course at the University of Applied Sciences of the Grisons, as part of the Engineering program with a specialization in Mobile Robotics.


# Dokumentation
## Introdution
This program detects different geometric shapes and colors, either from images stored in a local folder or from a livestreamed camera.
Additionally, the program includes extensions that provide audio feedback for detected shapes and colors, as well as a graphical user interface (GUI) for improved usability.
The project consists of the following main files:
main.py, customized_datatypes.py, image_processing.py, load_sources.py, shapespeaker.py, log_data.py, and gui.py.


## Getting started
The program runs within a virtual environment.
To set it up, execute setup_local_env.py. This script installs all required libraries into a newly created .venv folder.
Once the setup is complete, the program will run smoothly through the detection process.


## Interaction
### General Interaction
To run the entire program, execute main.py.

To recognize images from the data folder, use the --image argument. To use the camera for recognition, use the --camera argument in the console.

Examples:
    \Git\SW_Eng_Projet_object_detection\src\main.py --image
    \Git\SW_Eng_Projet_object_detection\src\main.py --camera
When launched, the window will display the detected shapes immediately.

Object detection on images:
When running object detection on images, the program provides three buttons allowing you to:
-Close the application
-Play the audio description of detected shapes
-Continue to the next image

Object detection on camera:
When using the camera, the program detects shapes in real time.
The user can close the application or play the detected shapes’ audio output.

### Logging
The program automatically logs all detected shapes and saves them in the logs folder.
Each execution of main.py generates exactly one log file.
Additionally, audio files are saved in the sounds folder.
Only the most recent audio file is kept—each new execution overwrites the previous one.

### Object detection on images
The program processes images from the images folder.
To use this feature, ensure that your images are saved in this directory before running the program. 

### Object detection on camera
By default, the program uses camera device 0, which is typically the laptop’s built-in webcam.
To use a different camera, you may disable the default webcam in your system settings.
If no active or connected camera is detected, the program will terminate and prompt the user to connect one.

