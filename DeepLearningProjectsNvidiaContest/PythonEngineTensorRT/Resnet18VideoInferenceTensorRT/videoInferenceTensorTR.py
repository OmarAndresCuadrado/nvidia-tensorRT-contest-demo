import tensorrt as trt
import pycuda.autoinit
import pycuda.driver as cuda
import cv2
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import yaml
import time
import random
import string
import subprocess
import sys

class YOLOv5TensorRT:
    def __init__(self, engine_file_path, input_shape, output_shape, classes_label_file, conf_threshold, score_threshold, nms_threshold):
        self.logger = trt.Logger(trt.Logger.WARNING)

        self.engine_file_path = engine_file_path

        self.input_shape = input_shape

        self.output_shape = output_shape

        self.classes_label_file = classes_label_file

        self.conf_threshold = conf_threshold

        self.score_threshold = score_threshold

        self.nms_threshold = nms_threshold

        self.engine = self.load_engine()

        self.context = self.engine.create_execution_context()

        self.class_labels = self.load_class_labels()

        self.stream = cuda.Stream()

    def load_engine(self):
        with open(self.engine_file_path, 'rb') as f, trt.Runtime(self.logger) as runtime:
            return runtime.deserialize_cuda_engine(f.read())

    def load_class_labels(self):

        with open(self.classes_label_file, 'r', encoding='UTF8') as file:
            data = yaml.safe_load(file)

            return [name for name in data['names'].values()]

    def preprocess_video(self, video_path):
        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            print("Error: Unable to open video file:", video_path)
            return
        
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            img_resized = cv2.resize(frame, (self.input_shape[2], self.input_shape[3]), interpolation=cv2.INTER_AREA)
            self.resized_frame_h, self.resized_frame_w = img_resized.shape[:2]

            self.org_frame_h, self.org_frame_w = frame.shape[:2]

            img_np = np.array(img_resized, dtype=np.float32) / 255.0
            img_np = np.transpose(img_np, (2, 0, 1))


            yield img_np, frame

        video.release()

    def inference_detection(self, video_path):
        total_time = 0
        num_frames = 0
        output_frames = []

        for inputs, frame in self.preprocess_video(video_path):
            num_frames += 1
            start_time = time.time()


            inputs_host = np.ascontiguousarray(inputs, dtype=np.float32)
            outputs_host = np.empty(self.output_shape, dtype=np.float32)
            inputs_device = cuda.mem_alloc(inputs_host.nbytes)
            outputs_device = cuda.mem_alloc(outputs_host.nbytes)


            cuda.memcpy_htod_async(inputs_device, inputs_host, self.stream)
            self.context.execute_async_v2([int(inputs_device), int(outputs_device)], self.stream.handle)
            cuda.memcpy_dtoh_async(outputs_host, outputs_device, self.stream)


            self.stream.synchronize()

            inference_time = time.time() - start_time
            total_time += inference_time

            fps = num_frames / total_time
            self.postprocessing_recognized_frames(frame, outputs_host, fps)
            output_frames.append(frame)


            inputs_device.free()
            outputs_device.free()

        self.save_result_video(output_frames)

    def postprocessing_recognized_frames(self, frame, yolov5_output, fps):

        detections = yolov5_output[0].shape[0]

        x_scale = self.org_frame_w / self.resized_frame_w

        y_scale = self.org_frame_h / self.resized_frame_h

        bboxes = []

        confidences = []

        class_ids = []

        for i in range(detections):
            detect = yolov5_output[0][i]
            getConf = detect[4]

            if getConf < self.conf_threshold:
                continue

            class_score = detect[5:]

            class_idx = np.argmax(class_score)

            if class_score[class_idx] <= self.score_threshold:
                continue

            confidences.append(getConf)
            class_ids.append(class_idx)

            cx, cy, w, h = detect[:4]

            left = int((cx - w / 2) * x_scale)

            top = int((cy - h / 2) * y_scale)

            width = int(w * x_scale)

            height = int(h * y_scale)

            bboxes.append([left, top, width, height])

        indices_nonmax = cv2.dnn.NMSBoxes(bboxes, confidences, self.conf_threshold, self.nms_threshold)

        for i in indices_nonmax.flatten():
            box = bboxes[i]
            left, top, width, height = box

            label = f"{self.class_labels[class_ids[i]]}:{confidences[i]:.2f}, FPS: {fps:.2f}"

            cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 3)
            cv2.putText(frame, label, (left, top - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Detection.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def save_result_video(self, frames):

        project_directory_path = os.path.dirname(os.path.realpath(__file__))

        project_directory_path_format = project_directory_path.replace('\\', '/')


        parent_directory_path_one = os.path.abspath(os.path.join(project_directory_path_format, os.path.pardir)).replace('\\', '/')
        parent_directory_path_two = os.path.abspath(os.path.join(parent_directory_path_one, os.path.pardir)).replace('\\', '/')

        output_video_angular = parent_directory_path_two + '/NvidiaContestDemo/FrontendAngular/src/assets'
        print("output_video_angular ", output_video_angular)

        random_name = ''.join(random.choices(string.ascii_lowercase, k=6))

        output_video_path = project_directory_path_format
        print("output_video_project ", output_video_path)

        if not os.path.exists(output_video_path):
            os.makedirs(output_video_path)

        out_video_path = os.path.join(output_video_path, f'{random_name}.mp4')

        out_video_path_angular = os.path.join(output_video_angular, f'{random_name}.mp4')

        frame_shape = frames[0].shape[1::-1]
        out_video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 25.0, frame_shape)

        for frame in frames:
            out_video.write(frame)

        out_video.release()

        command = f"ffmpeg -i {out_video_path} -c:v libx264 {out_video_path_angular}"

        try:
            subprocess.run(command, shell=True, check=True)
            print("Video move it successfully to angular folder!")
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)

def main():
    videoNameArgument = sys.argv[1]

    project_directory_path = os.path.dirname(os.path.realpath(__file__))

    project_directory_path_format = project_directory_path.replace('\\', '/')


    engine_file_path =  project_directory_path_format + '/Models/ImageAndVideoInference.engine'
    
    path_to_classes = project_directory_path_format + '/coco.yaml'
   
    video_path = project_directory_path_format + '/OriginalVideo/'

    video_path_name = video_path + videoNameArgument

    input_shape = (1, 3, 640, 640)

    output_shape = (1, 25200, 85)
    
    inference = YOLOv5TensorRT(engine_file_path, input_shape, output_shape,  path_to_classes, 0.4, 0.45, 0.35)
    
    inference.inference_detection(video_path_name)
    
    
if __name__=="__main__":
    main()

