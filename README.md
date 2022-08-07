# Position-Based Visual Servo 

<p align="center">
  <img src="https://user-images.githubusercontent.com/40195016/183271876-c494e9b1-2fe8-4bbf-8176-5026367c5b4f.gif" width="350"/>
  <img src="https://user-images.githubusercontent.com/40195016/183271879-a6de2253-161a-4a3e-b4c3-0b018fec77e6.gif" width="350"/>
</p>

## Description
An implementation of the Position-Based Visual Servo (PBVS) in Python 3.10 with OpenCV 4.6.0. The main reference paper is [Visual servo control, Part I: Basic approaches](https://hal.inria.fr/inria-00350283/file/2006_ieee_ram_chaumette.pdf)
by F. Chaumette and S. Hutchinson.

The purpose of visual servoing is to have control over the end-effector relative to the goal. For this, image features of the target are extracted, and preprocessed to
eventually localize the target by its position.

<p align="center">
  <img src="https://user-images.githubusercontent.com/40195016/183269196-bf263fed-dda7-4ca2-b6c0-dab45b7c4d84.svg" width="700"/>
</p>

<p align="center">
  Fig.1. Position-based visual servo.
</p>

### ArUco Marker
The target used as goal is a [fiducial marker](https://en.wikipedia.org/wiki/Fiducial_marker) known as ArUco marker, more concise information can be found in [Automatic generation and detection of highly reliable fiducial markers
under occlusion](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiXuceWuLP5AhUcL0QIHXQ4BosQgAMoAHoECAEQAg&url=https%3A%2F%2Fscholar.google.com.mx%2Fscholar_url%3Furl%3Dhttps%3A%2F%2Fcode.ihub.org.cn%2Fprojects%2F641%2Frepository%2Frevisions%2Fmaster%2Fentry%2Freaded%2FAutomatic%252520generation%252520and%252520detection%252520of%252520highly%252520reliable%252520fiducial%252520markersnunder%252520occlusion.pdf%26hl%3Des%26sa%3DX%26ei%3DsQLvYqiwC8KjywSbu76AAg%26scisig%3DAAGBfm201CMNLnD07tNRdlkyyUG_rd1aJg%26oi%3Dscholarr&usg=AOvVaw0gk6onTq5VDi690-8xUhiS)
by S. Garrido-Jurado, R. Muñoz-Salinas, F. J. Madrid-Cuevas, and M. J. Marín-Jiménez.

The main reason for using this fiducial marker is because of the ease with which the pose of the camera can be estimated. Also, OpenCV offers a complete submodule dedicated exclusively for [detecting ArUco markers](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html).

There exists a convenient platform to easily generate [online ArUco markers](https://chev.me/arucogen/). The **configuration that this project uses is:**

- _Dictionary:_ **4x4 (50, 100, 250, 1000)**.
- _Marker ID:_ **0 and 1**.
- _Marker size, mm:_ **100**.

However, I don't really use the _Marker ID_ parameter so that it can be any of the allowed ID's (0, 1, 2, 3...). Another recommendation is to crop around the ArUco in such a way 
that some white space is left, this will help for the better detection of the ArUco. Additionally, I recommend sticking it on a hard surface which will prevent
that the ArUco bends, and it also helps for a better dectection. A piece of cardboard will be enough. Leaving a kind of cardboard piece at the end in order to
have a better grip of the ArUco helped a lot. Otherwise, it's difficult not to occlude the ArUco.

### Graphical User Interface
Essentially, the Graphical User Interface (GUI) works as a guide for whoever is running the program and wants to reach the final position with the help of a minimal but sufficient text indicator.
This text let the user know what are the steps to follow to reach the goal position, and they are displayed sequentially.

<p align="center">
  <img src="https://user-images.githubusercontent.com/40195016/183271464-a03748d7-0f23-4dfc-9dbb-5fb0c51e670e.gif" width="350"/>
  <img src="https://user-images.githubusercontent.com/40195016/183271632-1594060f-06ca-4d46-abcb-5c886dc73f18.gif" width="350"/>
</p>

At the moment of showing the information, different windows are displayed. The top-left window is the current position in $x, y$ and $z$ the bottom-left window is the current
orientation in the Euler angles $\phi, \theta$ and $\psi$. The top-middle window is the desired position $x_d, y_d$ and $z_d$ and the bottom-middle window is the desired
orientation $\phi_d, \theta_d$ and $\psi_d$. Finally, the top-right window is the error in the position $x_e, y_e$ and $z_e$ and the bottom-right window is the error in the 
orientation $\phi_e, \theta_e$ and $\psi_e$.

### Charts
I have decided to add some charts as a reference using the well-known ```matplotlib.pyplot``` library, this to have a tracking of the position and orientation as well
as their position and orientation error of the camera with respect to the ArUco marker.

<p align="center">
  <img src="https://user-images.githubusercontent.com/40195016/183272642-4edb555b-d6d7-46b7-a4b3-ea5e5968bf25.gif" width="344"/>
  <img src="https://user-images.githubusercontent.com/40195016/183272643-8541d757-7fac-4038-a843-e3176396c1b9.gif" width="350"/>
</p>

<p align="center">
  Fig.2. Left: Position and orientation. Right: Position and orientation error.
</p>

The charts are displayed in real-time which is something to consider before using it since it may consume a lot of the processor to draw the charts and therefore make
the program to run slow or even the computer. The recommendation is to run the charts only when it is really necessary.  


## Usage 
```
usage: PBVS.py [-h] [-sc | --show_charts | --no-show_charts] [-sg | --show_gui | --no-show_gui]

Implements the Position-Based Visual Servo.

options:
  -h, --help            show this help message and exit
  -sc, --show_charts, --no-show_charts
                        Shows the charts of position and orientationin real time
  -sg, --show_gui, --no-show_gui
                        Shows the gui to reach the desired pose of the ArUco marker (default: True)
```

To save the current pose of the ArUco marker relative to the camera the key ```q``` can be pressed. This will save the pose into a ```.npy``` file in the ```/bin``` directory.

## Examples
To show the charts in real-time

```python3 PBVS.py --show_charts```

To not show the GUI

```python3 PBVS.py --no-show_gui```

## License
MIT License

Copyright (c) [2022] [Angelo Espinoza]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
