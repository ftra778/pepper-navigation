# Pepper Motion Mimicking

This project aims to project human motions to the Pepper robot using a simple webcam setup and Python

## Description

Human-robot interaction is a topic that has been around for a long time, and recent technological advances in social robots will serve as an important role in our society. We aim to decrease the interactivity boundary between humans and robots through human motion mimicking to create meaningful motions on robots. This repository presents a human motion mimicking system which utilizes equipment commonly available and easily accessible. The performance of this system is evaluated on the SoftBank Robotics Pepper and NAO social robots. This system achieves mimicking of natural and recognisable human motions and proves motion mimicking can be achieved on lower processing power devices and with minimal cost.

## Getting Started

### Dependencies

* Linux 20.04 or Newer
* Anaconda
* Python 2.7.x & Python 3.8.x
* [NAOqi Python SDK & Choregraphe](https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares)

### Installing

* Clone the GitHub repo
```
git clone git@github.com:UoA-CARES/pepper-motion-mimicking.git
```
* Create conda environments using the .yml files found in the "Environments" folder (May require editing the .yml file with different file paths if necessary)

### Video Recording

* The person being recorded must remain in the same spot for the video i.e: no walking
* Do not use legs for motions
* Videos need to be moved to the "videos/pose-videos/" folder

## Using Program
### Executing simulation program

* Create a new Choregraphe project
* Create two new Python boxes in the environment (Separate Pepper and NAO)
* Copy + Paste the contents of both Python box files into their respective box
* Link the onStart and onStopped inputs/outputs to one of the boxes depending on the robot
* Click the "Play" button or press F5 on your keyboard to run the simulation

### Executing real program

* Open two different terminals and activate each environment
* Using the "pepper38" environment, run the following line to run a video through MediaPipe, where --name is the name of the video (without extension name i.e: do not enter .mp4)
```
python pose_capture.py --name video_name
```

* Using the "pepper27" environment, run the following line once after activating environment
```
export PYTHONPATH=${PYTHONPATH}:/path/to/NAOqiSDK/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
```
* To apply motions to Pepper, run the following line where --pepper is a boolean that indicates you want to connect to Pepper (CAUTION - Setting this to True or False will act as if the argument is True, so if you do not wish to connect to Pepper, then do not use the argument at all), --pepper_ip is the ip address of Pepper, --pepper_port is the specific port number, and --pepper_name is the name of the gesture to execute
* To apply motions to NAO, run the following line where --nao is a boolean that indicates you want to connect to NAO (CAUTION - Setting this to True or False will act as if the argument is True, so if you do not wish to connect to NAO, then do not use the argument at all), --nao_ip is the ip address of NAO, --nao_port is the specific port number, and --nao_name is the name of the gesture to execute
```
python apply_motion.py --pepper bool --pepper_ip ip_addr --pepper_port port_no --pepper_name gesture_name --nao bool --nao ip ip_addr --nao port port_no --nao name gesture_name
```

## Notes

* It is highly recommended that any new motion is tested in the simulator before applied to the robot for safety.
* When recording videos, it is recommended that any baggy clothes are removed i.e: jackets, jumpers. They make it more difficult to track limbs.
* When recording videos for motions, there may be some sections at the start and end of the video that can reduce the quality of the motion severely i.e: flopping of arms, clicking record, looking at screen etc.. It is highly recommended that you either trim the start and/or end of the video, manually edit the .csv file, or have someone else record for you.
* Some motions, especially ones reliant on depth data, may not translate well to the robot. This is usually rectified by recording the video in a more 'robotic' fashion.
* When simulating, the robots can be interchanged between Pepper and NAO under "Edit > Preferences > Virtual Robot".


## Authors

[Finn Tracey](ftra778@aucklanduni.ac.nz) & Cale Ying

## Version History
* 0.3
    * Added NAO functionality

* 0.2
    * Added Python box codes for both Pepper and NAO (NAO is WIP) Choregraphe

* 0.1
    * Initial Release