from ultralytics import YOLO
import os
#import torch

class Detector:
    def __init__(self):
        self.model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "model_weights",
            "runs",
            "detect",
            "fine_tuned_varro_model9",
            "weights",
            "best.pt"
        )  # Path to your fine-tuned model

        
        self.model = YOLO(self.model_path, verbose=False)
        self.result = None

    def run_detection(self, image):
        # Run the model on a single image
        result = self.model(
            image,
            imgsz=1024,  #fine tuned uses 512 / 6016
            max_det=2000,
            conf=0.3,
            iou=0.5,
            save=False,
            show_labels=False,
            line_width=2,
            save_txt=False,
            save_conf=False,
            verbose=False,
            batch=1,
            exist_ok=True,
            #device="cuda"   #uncomment if you have gpu
        )

        self.result = result[0] # only for one image

    



# Train 

if __name__ == '__main__':
    if False:
        import torch
        # Check if GPU is available
        print("CUDA available:", torch.cuda.is_available())
        print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A")


        # Load a pretrained model (or your existing one)
        model = YOLO("../model_weights/best.pt") 
        

        #freeze first 100 layers of the model
        layers = list(model.model.children())

        for i, layer in enumerate(layers[:100]):
            for param in layer.parameters():
                param.requires_grad = False


        model.train(
            data="yolo_data/data.yaml",  # path to your dataset YAML
            epochs=50,
            imgsz=1024,
            batch=1,
            name="fine_tuned_varro_model",
            resume=False  # True if you're continuing from a checkpoint
        )


