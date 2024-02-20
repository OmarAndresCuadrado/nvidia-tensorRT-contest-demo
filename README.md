# 🚀 Nvidia tensorRT contest demo 🚀

## OverView 👁️
**This project is designed** to leverage cutting-edge technology in artificial intelligence (AI) to provide high-performance image and video inference, as well as generative AI for text chat. At its core, the backend engine utilizes Python and integrates Nvidia's TensorRT technology, enhancing efficiency and speed to meet the demands of real-time processing.

---
## Diagram project workflow ⚒️

<p align="center">
<img src="https://github.com/OmarAndresCuadrado/nvidia-tensorRT-contest-demo/blob/master/overViewDesignDemo.png"  align="center">
</p>

---
## Demo video 📹
video in x tweter

---
#### Backend Engine
Developed in Python, the backend engine is the powerhouse of the project. It employs **Nvidia TensorRT, a high-performance deep learning inference platform**.

---
#### Frontend Interface
To ensure a user-friendly experience, the frontend is built with **Angular**. This modern framework provides a responsive and intuitive interface.

---
#### Middleware Layer
Bridging the frontend and the backend, the middleware layer is implemented using **Spring Boot with Java**. This component is crucial for orchestrating command-line commands to the **Python-based AI engine**.

## A BIT OF IA TOOLS INSIDE THIS PROJECT 🤖

This project used as pretrained models for video and image inference from pytorch Resnet18, on the other hand a pretrained model distilbert-base-uncased-distilled-squad
was use in order to create the generative IA chat bot based on Question-and-Answer system, these projects have been optimizing by using Nvidia's TensorRT technology; you can check the section (Compile section) how to compile onnx files and tensorRT engines.

Note: since the compile onnx and tensorRT engine files are a big ones and can’t add to github, you can download them from this google drive (here you can find everything related to this wonderful project)

```
https://drive.google.com/drive/u/0/folders/1ky-Om3OGPZiVl8v1hu1Zmt5jKCmlKIHM
```
---
#### Models use for video and image inference (onnx and TensorRT engine files)
**Model:** Resnet18 <br>
**onnx file:** https://drive.google.com/file/d/1T0Ci8rr4ePjWdkoe8uygXccqiWrfR02P/view?usp=drive_link <br>
**TensorRT engine file:** https://drive.google.com/file/d/16DMZ_BPcFZ1pWsekhyj8APjhG3V9VEk0/view?usp=drive_link 


#### Models use for generative IA chat bot based on Question-and-Answer system (onnx and TensorRT engine files)
**Model:** distilbert-base-uncased-distilled-squad <br>
**onnx file:** https://drive.google.com/file/d/1upBRUy5Q5o5czaRqA1y_-0NPwdS9onR7/view?usp=drive_link <br>
**TensorRT engine file:** https://drive.google.com/file/d/1zwpfNaCVdDa8kSQFlJPnnDY88kIInN20/view?usp=drive_link

## Compile section ⚙️

---
### Resnet18
1. For compiling the onnx file for resnet18 you can use the script that is located at the root of the project "exportResnetModelToOnnx.py"

2. For the tensorRT engine file, you will have to go to your tensorRT installation folder , in my case is **C:\TensorRT-8.6.1.6\bin** open a cmd shell inside the bin folder and add the onnx file generated on the step before, the run the following command

```
trtexec --onnx=[path_to_your_onnx_model] --saveEngine=[path_to_save_trt_engine_file]
```
---
### Distilbert-base-uncased-distilled-squad
1. you can download the onnx file from 
```
https://huggingface.co/philschmid/distilbert-onnx
```

2. For the tensorRT engine file, you will have to go to your tensorRT installation folder , in my case is **C:\TensorRT-8.6.1.6\bin** open a cmd shell inside the bin folder and add the onnx file generated on the step before, the run the following command

```
trtexec --onnx=distilbert-base-cased-distilled-squad.onnx --saveEngine=distilbert-base-cased-distilled-squad.trt --explicitBatch --minShapes=input_ids:1x128,attention_mask:1x128 --optShapes=input_ids:4x128,attention_mask:4x128 --maxShapes=input_ids:8x128,attention_mask:8x128 --workspace=2048 --fp16
```

## Installation Guide ⚙️

The steps could look too much but **is very straightforward environment setup I just want to make sure to make a really detail guide, so could looks extensive** (PS. as soon as I finish this guide, I test my self-following this guide successfully 🙂)

I’m going to provided **two different option for installation**, both of them are simple to reproduce


### Dependencies needed for option one and two

```
pip install transformers
pip install torch
pip install torchvision
pip install torchaudio
pip install pycuda
pip install opencv-python-headless
pip install numpy
pip install Pillow
pip install matplotlib
pip install pyyaml
pip install subprocess.run
```

---
#### Install ffmpeg 

1. clone the git repository

```
git clone https://git.ffmpeg.org/ffmpeg.git
```

2. add this to your path variables on your windows machine
```
C:\Users\USUARIO\Documents\DevTools\ffmpeg-master-latest-win64-gpl\bin\
```
**Remember to change to path to your download location**


### Dependencies needed for option one 1️⃣


Install java 8 JDK (follow this tutorial)  <br>
Install Maven (follow this tutorial) <br>
Install Nodejs (go to its official website here and download the install) <br>
Install Angular (just run the following command once you have installed node) <br>

### 🐍 Option One only uses python IA programs from a cmd console 🐍

Before to use any python IA program, you have to change the original path and comment some lines in the IA python programs

---
#### 🖼️ For image inference IA program 🖼️


go to **{your-download-project-folder}/ DeepLearning/Resnet18VImageferenceTensorRT**

1. Comment the following lines (you can find this lines at the end of the script)

```
#directory_path_angular = 'C:/Users/USUARIO/Documents/NvidiaContestDemo/frontend/nvidia-contents/src/assets'
```
```
#file_path_angular = os.path.join(directory_path_angular, filename)
```
```
#cv2.imwrite(file_path_angular, image)
```
```
#print("File also saved for angular app at:", file_path_angular)
```

2. Setup your workspace path


On the def main(): you are going to set up in the following lines your workspace

```
directory_path = 'C:/Users/USUARIO/Documents/DeepLearning/YOLO/ProcessedImages/'
engine_file_path = 'C:/Users/USUARIO/Documents/DeepLearning/YOLO/Models/yolov5s.engine'
class_labels_file = 'C:/Users/USUARIO/Documents/DeepLearning/YOLO/coco.yaml'
image_path = 'C:/Users/USUARIO/Documents/DeepLearning/YOLO/OriginalImages'
```

Note: In my case **"C:/Users/USUARIO/Documents"** is where my project is located, so, in your case you have to change this path with your project download location


Before to run the program move some images (.jpg or .jpeg) to the **"/DeepLearning/YOLO/OriginalImages"**


3. Run the following program from the root of the project (where imageInferenceTensorTR.py is located) 

Open a cmd in the root path and type **"python imageInferenceTensorTR.py"** (without quotes)

The result images will appear in the **"/DeepLearning/YOLO/ProcessedImages"**

---
### 🎞️ For video inference IA program 🎞️

go to **{your-download-project-folder}/DeepLearning/Resnet18VideoInferenceTensorRT**

1. Comment the following lines (you can find this lines at the end of the script)

```
 #output_video_angular = 'C:/Users/USUARIO/Documents/NvidiaContestDemo/frontend/nvidia-contents/src/assets'
```
```
#out_video_path_angular = os.path.join(output_video_angular, f'{random_name}.mp4')
```
```
# command = f"ffmpeg -i {out_video_path} -c:v libx264 {out_video_path_angular}"
```
```
# try:
#     subprocess.run(command, shell=True, check=True)
#     print("Video move it successfully to angular folder!")
# except subprocess.CalledProcessError as e:
#     print("Error executing command:", e)
```

2. Setup your workspace path

On the def main(): you are going to set up in the following lines your workspace

```
engine_file_path =  'C:/Users/USUARIO/Documents/DeepLearning/YOLOVIDEO/Models/yolov5s.engine'
```
```
video_path = f'C:/Users/USUARIO/Documents/DeepLearning/YOLOVIDEO/OriginalVideo/{videoNameArgument}'
```
```
path_to_classes = 'C:/Users/USUARIO/Documents/DeepLearning/YOLOVIDEO/coco.yaml'
```

Note: In my case **"C:/Users/USUARIO/Documents"** is where my project is located, so, in your case you have to change this path with your project download location

now, before to run the program move some videos (.mp4) to the **"/DeepLearning/YOLOVIDEO/OriginalVideo"**

3. Run the following program from the root of the project (where imageInferenceTensorTR.py is located) 

Open a cmd in the root path and type 'python videoInferenceTensorTR.py  "videoName.mp4" '(the video name has to be closed between quotes)

The result images will appear in the '/DeepLearning/ YOLOVIDEO/'

---
### 💬 For generative chat bot IA program 💬

go to
**{your-download-project-folder}/DeepLearning/GeneartiveIaChatTensorRT**

1. Setup your workspace path

```
filename = f"C:/Users/USUARIO/Documents/DeepLearning/questionAnswer/Responses/chat_response.txt"
```

Note: In my case **"C:/Users/USUARIO/Documents"** is where my project is located, so, in your case you have to change this path with your project download location


2. Run the following program from the root of the project (where imageInferenceTensorTR.py is located) 


Open a cmd in the root path and type "python GenerativeIaQuestionAndAnswer.py  "Colombia is a wonderful country" "what is Colombia?" " (the program need to have two initial argument , the first one is for the context and the second one is for the question, both of them are closed by double quotes

The response will appears on the cmd at the end and inside the {your-download-project-folder}/DeepLearning/GeneartiveIaChatTensorRT/Responses/reponse.txt file

### Option Two full installation 2️⃣

if you want to use the wonderful UI running on angular and spring in order to communicate with the IA programs from python, we need to set up a couple of simple things (trust me is really fast)

todo todo todo
todo todo todo
todo todo todo

### General project Resources  📚

Here you can find

- The onnx files
- The trt engine files
- The original presentation
- The picture of the Diagram
- The datasets used on the demo 
- The python script for compiling the Resnet18

https://drive.google.com/drive/u/0/folders/1ky-Om3OGPZiVl8v1hu1Zmt5jKCmlKIHM




