# Dokumentation

## Introdution
This Programm will detect diffrent shapes and patterns from either an input photo or an livestream from a conected camera.
Ther are also extensions implemented, enabling the program to give an audio output of the detected shapes, as well as an user-interface for better handling.
It is modular structured and consist out of the main.py, the image_prozessing.py, the shapespeaker.py, the log_data.py and the gui.py.

## Getting started
The program is working with a virtual enviroment, so in order to get started, its recomended to run the file setup_local_env.py, this file will install all required libarys into a newly created folder .venv. Afterwards the program will run smoothly thrue the detections process.

## Interation
### General Interation
The User can interact only thrue the main.py. 

The User has to choose a media to shape recognition via --image and --camera, this has to be added behind the execution path.
Examples:
    \Git\SW_Eng_Projet_object_detection\src\main.py --image
    \Git\SW_Eng_Projet_object_detection\src\main.py --camera
    The opening window will show the detected shapes imidiatly.

When opening the shape detection using images, the User can interact with the programm via three buttons allowing the user to either close the application, speak the detected shapes or continue to the next Image.

When opening the shape detection using the camera, the programm will detect potential shapes in realtime. The User can close the application and speak detected shapes.

### Loging
The Program will log the detected shapes automatically and safe it into the logs folder.

Ther will be exactly one logs-file per executed main.

Additionaly the sounds will be safed into the sounds folder. Only the last sounds-file will be safed, the next exectuion will overwrite the file.

### Image detection
The program will detect the images from the folder images. So in order to use the program the user has to safe the images into the folder. 

### Camera detection
The Programm will use per default the camera device 0, for laptos usaly the webcam. 
If the user wishes to use a diffrent camera insteat the webcam has to be deactivated (settings).

If ther is no camera activated or connected the programm will abort and demand a camera.

