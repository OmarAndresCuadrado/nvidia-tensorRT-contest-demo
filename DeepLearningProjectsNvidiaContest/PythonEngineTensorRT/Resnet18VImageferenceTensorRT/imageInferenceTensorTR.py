import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import cv2
import numpy as np
import os
import time
import yaml

class TRTInference:

    def __init__(self, engine_file_path, input_shape, output_shape, class_labels_file, conf_threshold, score_threshold, nms_threshold):

        self.logger = trt.Logger(trt.Logger.WARNING)

        self.engine_file_path = engine_file_path

        self.engine = self.load_engine(self.engine_file_path)

        self.context = self.engine.create_execution_context()

        self.conf_threshold = conf_threshold

        self.score_threshold = score_threshold

        self.nms_threshold = nms_threshold

        self.input_shape = input_shape

        self.output_shape = output_shape



        with open(class_labels_file, 'r', encoding='UTF8') as class_read:
            data = yaml.safe_load(class_read)
            self.class_labels = [name for name in data['names'].values()]
        self.stream = cuda.Stream()

    def load_engine(self, engine_file_path):

        with open(engine_file_path, 'rb') as f:
            runtime = trt.Runtime(self.logger)
            engine_deserialized = runtime.deserialize_cuda_engine(f.read())
        return engine_deserialized

    def preprocess_image(self, image_path):

        img_list, img_path = [], []


        for img_original in os.listdir(image_path):
            if img_original.lower().endswith(('.jpg', '.png', '.jpeg')):
                img_full_path = os.path.join(image_path, img_original)
                img = cv2.imread(img_full_path)
                img_resized = cv2.resize(img, (self.input_shape[3], self.input_shape[2]), interpolation=cv2.INTER_AREA)
                img_np = np.array(img_resized).astype(np.float32) / 255.0
                img_np = img_np.transpose((2,0,1))
                img_np = np.expand_dims(img_np, axis=0)
                img_list.append(img_np)
                img_path.append(img_full_path)

                if len(img_list) >= 12:
                    break

        return img_list, img_path

    def inference_detection(self, image_path):

        input_list, full_img_paths = self.preprocess_image(image_path)
        total_time = 0

        for inputs, full_img_path in zip(input_list, full_img_paths):
            start = time.time()
            inputs = np.ascontiguousarray(inputs)
            outputs = np.empty(self.output_shape, dtype=np.float32)
            d_inputs = cuda.mem_alloc(1 * inputs.nbytes)
            d_outputs = cuda.mem_alloc(1 * outputs.nbytes)
            bindings = [int(d_inputs), int(d_outputs)]
            cuda.memcpy_htod_async(d_inputs, inputs, stream=self.stream)
            self.context.execute_async_v2(bindings=bindings, stream_handle=self.stream.handle)
            cuda.memcpy_dtoh_async(outputs, d_outputs, stream=self.stream)
            self.stream.synchronize()
            total_time += (time.time() - start)
            self.postprocess_recognized_image(full_img_path, outputs, total_time)

    def postprocess_recognized_image(self, image_path, yolov5_output, total_time):

        image = cv2.imread(image_path)
        detections = yolov5_output[0].shape[0]
        height, width = image.shape[:2]

        x_scale = width / self.input_shape[3]
        y_scale = height / self.input_shape[2]


        conf_threshold = self.conf_threshold
        score_threshold = self.score_threshold
        nms_threshold = self.nms_threshold

        class_ids, confidences, bboxes = [], [], []

        for i in range(detections):

            detect = yolov5_output[0][i]
            getConf = detect[4]


            if getConf > conf_threshold:
                class_score = detect[5:]
                class_idx = np.argmax(class_score)



                if class_score[class_idx] > score_threshold:
                    confidences.append(float(getConf))
                    class_ids.append(class_idx)
                    

                    cx, cy, w, h = detect[:4]
                    left = int((cx - 0.5 * w) * x_scale)
                    top = int((cy - 0.5 * h) * y_scale)
                    width = int(w * x_scale)
                    height = int(h * y_scale)
                    bboxes.append([left, top, width, height])

        indices = cv2.dnn.NMSBoxes(bboxes, confidences, conf_threshold, nms_threshold)

        for i in indices.flatten():

            box = bboxes[i]
            left, top, width, height = box

            cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 3)

            label = f"Detected: {self.class_labels[class_ids[i]]} Confidence: {confidences[i]:.2f} Time: {total_time:.2f}s"

            cv2.putText(image, label, (left, top - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        project_directory_path = os.path.dirname(os.path.realpath(__file__))
        project_directory_path_format = project_directory_path.replace('\\', '/')

        directory_path_processed_images = project_directory_path_format + '/ProcessedImages'

        parent_directory_path_one = os.path.abspath(os.path.join(project_directory_path_format, os.path.pardir)).replace('\\', '/')
        parent_directory_path_two = os.path.abspath(os.path.join(parent_directory_path_one, os.path.pardir)).replace('\\', '/')

        directory_path_angular = parent_directory_path_two + '/NvidiaContestDemo/FrontendAngular/src/assets'

        if class_ids:
            filename = f"processed-{self.class_labels[class_ids[0]]}.jpg"
        else:
            filename = "processed-no-detection.jpg"


        file_path = os.path.join(directory_path_processed_images, filename)
        file_path_angular = os.path.join(directory_path_angular, filename)
        

        cv2.imwrite(file_path, image)
        cv2.imwrite(file_path_angular, image)

def main():

    project_directory_path = os.path.dirname(os.path.realpath(__file__))
    project_directory_path_format = project_directory_path.replace('\\', '/')


    engine_file_path =  project_directory_path_format + '/Models/ImageAndVideoInference.engine'
    
    class_labels_file = project_directory_path_format + '/coco.yaml'
   
    image_path = project_directory_path_format + '/OriginalImages'

    input_shape = (1, 3, 640, 640)
    output_shape = (1, 25200, 85)

   

    conf_threshold = 0.4
    score_threshold = 0.45
    nms_threshold = 0.35

   


    inference = TRTInference(engine_file_path, input_shape, output_shape, class_labels_file, conf_threshold, score_threshold, nms_threshold)
    inference.inference_detection(image_path)

if __name__ == "__main__":
    main()
