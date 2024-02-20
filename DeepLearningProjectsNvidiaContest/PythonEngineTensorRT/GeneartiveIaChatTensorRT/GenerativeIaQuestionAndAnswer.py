import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
import tensorrt as trt
from transformers import DistilBertTokenizer
import sys
import os

def load_engine(trt_runtime, engine_path):

    with open(engine_path, 'rb') as f:
        engine_data = f.read()
       
    engine = trt_runtime.deserialize_cuda_engine(engine_data)
    return engine

def run_inference(question, context, engine):

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')

    inputs = tokenizer.encode_plus(question, context, return_tensors='pt', padding='max_length', truncation=True, max_length=128)

    input_ids = inputs['input_ids'].detach().cpu().numpy()

    attention_mask = inputs['attention_mask'].detach().cpu().numpy()

    
    context = engine.create_execution_context()

    context.active_optimization_profile = 0

    context.set_binding_shape(0, input_ids.shape)

    context.set_binding_shape(1, attention_mask.shape)


    
    d_input_ids = cuda.mem_alloc(input_ids.nbytes)

    d_attention_mask = cuda.mem_alloc(attention_mask.nbytes)


    output_start_shape = context.get_binding_shape(2)
    output_end_shape = context.get_binding_shape(3)


    if output_start_shape[0] < 0 or output_end_shape[0] < 0:
        raise ValueError("Invalid shape received from TensorRT engine")

    output_start = np.empty(output_start_shape, dtype=np.float32)
    output_end = np.empty(output_end_shape, dtype=np.float32)


    d_output_start = cuda.mem_alloc(output_start.nbytes)

    d_output_end = cuda.mem_alloc(output_end.nbytes)


    stream = cuda.Stream()


    cuda.memcpy_htod_async(d_input_ids, input_ids, stream)

    cuda.memcpy_htod_async(d_attention_mask, attention_mask, stream)


    bindings = [int(d_input_ids), int(d_attention_mask), int(d_output_start), int(d_output_end)]

    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)


    cuda.memcpy_dtoh_async(output_start, d_output_start, stream)

    cuda.memcpy_dtoh_async(output_end, d_output_end, stream)

    stream.synchronize()


    start_index = np.argmax(output_start)

    end_index = np.argmax(output_end) + 1

    answer_tokens = tokenizer.convert_ids_to_tokens(input_ids.flatten()[start_index:end_index])

    answer = tokenizer.convert_tokens_to_string(answer_tokens)


    project_directory_path = os.path.dirname(os.path.realpath(__file__))
    project_directory_path_format = project_directory_path.replace('\\', '/')
    filename = project_directory_path_format + "/Responses/chat_response.txt"
    print("filename ", filename)

    
    with open(filename, 'w') as file:
        file.write(answer)

    return answer


if __name__ == '__main__':
    context_for_the_question = sys.argv[1]
    question = sys.argv[2]
    print("context_for_the_question ", context_for_the_question)
    print("question ", question)
  
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    trt_runtime = trt.Runtime(TRT_LOGGER)
    
    engine_path = 'distilbert-base-cased-distilled-squad.trt'
    engine = load_engine(trt_runtime, engine_path)

    question = question
    context = context_for_the_question
    answer = run_inference(question, context, engine)
    print("Answer:", answer)
