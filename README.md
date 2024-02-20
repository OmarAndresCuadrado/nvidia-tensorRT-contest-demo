# 🚀 Nvidia tensorRT contest demo 🚀

---
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

The steps could look too much but **is very straightforward environment setup I just want to make sure to make a really detail guide** (PS. as soon as I finish this guide, I test my self-following this guide successfully 🙂)

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
**this program is important to have a correct behaivor for the program to move some file to other folders**

---
### Dependencies needed for option two 

Install java 8 JDK follow this tutorial >> https://www.youtube.com/watch?v=ClcHrcNXP9g  <br>
Install Maven follow this tutorial >> https://www.youtube.com/watch?v=YTvlb6eny_0 <br>
Install Nodejs (go to its official website here and download the install) https://nodejs.org/dist/v21.6.2/node-v21.6.2-x64.msi   <br>
Install Angular (just run the following command once you have installed node) **npm install -g @angular/cli** <br>

### 1️⃣ Option One only uses 🐍python🐍 IA programs from a cmd console 1️⃣

---
#### 🖼️ For image inference IA program 🖼️

**project root** :  **/DeepLearningProjectsNvidiaContest/PythonEngineTensorRT/Resnet18VideoInferenceTensorRT**

1. Add some images (.jpg or .jpeg) to the **"/OriginalImages"** you can use the ones provided in the folder **DataSetImagesDemo**

2. Run the following command from the root of the project (where **imageInferenceTensorTR.py** is located) 

Open a cmd in the root path and type **"python imageInferenceTensorTR.py"** (without quotes)

The result images will appear in the **"/ProcessedImages"**

---
### 🎞️ For video inference IA program 🎞️

** project root ** :  **/DeepLearningProjectsNvidiaContest/PythonEngineTensorRT/Resnet18VImageferenceTensorRT**

1. Add some video (.mp4) to run the program  to the **"/OriginalVideo"**

2. Run the following program from the root of the project (where **imageInferenceTensorTR.py is** located) 

Open a cmd in the root path and type **python videoInferenceTensorTR.py  "videoName.mp4"** (the video name has to be closed between quotes)

The result video will appear in the **root of the project**

---
### 💬 For generative chat bot IA program 💬

go to
**/GeneartiveIaChatTensorRT**

1. Run the following program from the root of the project (where **imageInferenceTensorTR.py** is located) 

Open a cmd in the root path and type **"python GenerativeIaQuestionAndAnswer.py  "Colombia is a wonderful country" "what is Colombia?"** (the program need to have two initial argument , the first one is for the context and the second one is for the question, both of them are closed by double quotes

The response will appears on the cmd at the end and inside the **/Responses/reponse.txt** file
---
### Option Two full installation 2️⃣

If you want to use the wonderful UI running on angular and spring in order to communicate with the IA programs from python, we need to set up a couple of simple things (trust me is really fast)

In order to run successfully the entire application you will need to install the following tools
** go to (Dependencies needed for option two ) you can find the links there **

- Java 8 JDK 
- Maven
- Nodejs 
- Angular

1. Compile and run Frontend
	- Go to the Angular project folder **/NvidiaContestDemo/FrontendAngular**
	- Open a cmd bash
	- Run the command **npm install**
	- Run the angular project **ng serve**
	
2. Compile and run Backend
	- Go to the Spring project folder **/SpringJavaMiddelWare/demo-for-nvidia-contest-4090**
	- Open a cmd bash
	- Run the command **mvn clean install**
	- Run the spring project **mvn spring-boot:run**

3. Go to your favorite browser and go to angular host **http://localhost:4200/**
---
## 🖥️ Computer Specifications 🖥️

CPU: AMD Ryzen 7 7800X3D 8-Core Processo
GPU: NVIDIA GeForce RTX 4070 Ti
RAM: 32 3200 hz

## General project Resources  📚

#### Here you can find

- The onnx files
- The trt engine files
- The original presentation
- The picture of the Diagram
- The datasets used on the demo 
- The python script for compiling the Resnet18

https://drive.google.com/drive/u/0/folders/1ky-Om3OGPZiVl8v1hu1Zmt5jKCmlKIHM




