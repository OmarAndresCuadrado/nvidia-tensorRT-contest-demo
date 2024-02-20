import torch
import torchvision

model = torchvision.models.resnet18(pretrained=True)

resnet18_image = torch.rand(1, 3, 224, 224)

torch.onnx.export(model, resnet18_image,  "/tensorfl_vision/Resnet18/resnet18.onnx")