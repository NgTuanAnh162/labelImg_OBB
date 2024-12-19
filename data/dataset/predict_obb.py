from ultralytics import YOLO

# Load a model
model = YOLO("last.pt")  # load a custom model

# Predict with the model
results = model(r"D:\labelImg_OBB\data\dataset\test", save=True)  # predict on an image