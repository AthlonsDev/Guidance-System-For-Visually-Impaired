import tensorrt as trt
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
import cv2

# Load the TensorRT engine from file
def load_engine(engine_file_path):
    with open(engine_file_path, "rb") as f, trt.Runtime(trt.Logger(trt.Logger.INFO)) as runtime:
        return runtime.deserialize_cuda_engine(f.read())
    
# Create a runtime context for this engine
def create_context(engine):
    return engine.create_execution_context()

# Allocate memory for the input and output buffers
def allocate_buffers(engine, context):
    inputs, outputs, bindings = [], [], []
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        # Allocate device memory
        device_memory = cuda.mem_alloc(size * dtype.itemsize)
        bindings.append(int(device_memory))
        # Append to the appropriate list
        if engine.binding_is_input(binding):
            inputs.append(device_memory)
        else:
            outputs.append(device_memory)
    return inputs, outputs, bindings

# Do inference
def do_inference(context, bindings, inputs, outputs, stream, batch_size=1):
    # Transfer input data to the GPU
    cuda.memcpy_htod(inputs[0], np.ascontiguousarray(inputs[0].host))
    # Run inference
    context.execute(batch_size=batch_size, bindings=bindings)
    # Transfer predictions back from the GPU
    cuda.memcpy_dtoh(outputs[0].host, outputs[0])

#convert trt file to engine
def trt_to_engine(trt_file_path, engine_file_path):
    trt_path = trt_file_path
    with trt.Builder(trt.Logger(trt.Logger.INFO)) as builder, builder.create_network() as network, trt.UffParser() as parser:
        builder.max_workspace_size = 1 << 30
        builder.max_batch_size = 1
        builder.fp16_mode = True
        # Parse the Uff model to populate the network, then set the outputs
        parser.register_input("input", (3, 416, 416))
        parser.register_output("output")
        parser.parse(trt_path, network)
        # Build and serialize the engine
        with builder.build_cuda_engine(network) as engine:
            with open(engine_file_path, "wb") as f:
                f.write(engine.serialize())


# Load the engine from file
engine = load_engine("yolov4.engine")
# Create a runtime context
context = create_context(engine)
# Allocate memory for the input and output buffers
inputs, outputs, bindings = allocate_buffers(engine, context)
# Load the image
img = cv2.imread("dog.jpg")
# Preprocess the image
img = cv2.resize(img, (416, 416))
img = img.transpose((2, 0, 1))
img = img.ravel()
# Set the input data
inputs[0].host = img
# Do inference
do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=0)
# Print the output
print(outputs[0].host)