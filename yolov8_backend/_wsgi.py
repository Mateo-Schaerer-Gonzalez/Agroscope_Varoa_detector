import os
import traceback
from flask import Flask, jsonify, request
from ultralytics import YOLO
from label_studio_ml.model import LabelStudioMLBase
import os

# -----------------------------
# YOLOv8 backend class
# -----------------------------
class YOLOv8Backend(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            # Path to YOLOv8 model
            self.model_path = os.path.join(
                os.path.dirname(__file__),
                "..", "model_weights", "runs", "detect",
                "fine_tuned_varro_model9", "weights", "best.pt"
            )
            print("Model path:", self.model_path)

            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"YOLO model not found: {self.model_path}")

            # Load YOLO model
            self.model = YOLO(self.model_path)
            print("YOLO model loaded successfully!")

            # Label map
            self.label_map = {"Varroa": "varoa", "varroa": "varoa", "varoa": "varoa"}

        except Exception as e:
            print("Error initializing YOLOv8Backend:", e)
            traceback.print_exc()
            raise

    def predict(self, tasks, **kwargs):
        results = []

        for task in tasks:
            data = task.get("data", {})
            image_path = data.get("image")
            print("Received task image path:", image_path)

            if not image_path:
                results.append({"result": [], "error": "No image path in task", "model_version": "yolov8_varroa_v1"})
                continue

            try:
                # Resolve Label Studio path
                local_image_path = self.get_local_path(image_path)
                print("Resolved local image path:", local_image_path)

                if not local_image_path or not os.path.exists(local_image_path):
                    results.append({
                        "result": [],
                        "error": f"Image does not exist: {local_image_path}",
                        "model_version": "yolov8_varroa_v1"
                    })
                    continue

                # Run YOLO prediction
                pred = self.model.predict(
                    local_image_path,
                    imgsz=1024,
                    conf=0.1,
                    iou=0.5,
                    max_det=2000,
                    device="cuda:0" if kwargs.get("device") else "cpu",
                    verbose=False
                )[0]

                task_preds = []

                if pred.boxes is not None and len(pred.boxes) > 0:
                    for box in pred.boxes:
                        x_min, y_min, x_max, y_max = box.xyxy[0].cpu().numpy()
                        cls_id = int(box.cls[0].cpu().numpy())
                        yolo_label = pred.names[cls_id]
                        label = self.label_map.get(yolo_label, "varoa")
                        width = x_max - x_min
                        height = y_max - y_min

                        # Convert to Python float and clamp 0–100
                        task_preds.append({
                            "from_name": "label",
                            "to_name": "image",
                            "type": "rectanglelabels",
                            "value": {
                                "x": min(max(float(100 * x_min / pred.orig_shape[1]), 0), 100),
                                "y": min(max(float(100 * y_min / pred.orig_shape[0]), 0), 100),
                                "width": min(max(float(100 * width / pred.orig_shape[1]), 0), 100),
                                "height": min(max(float(100 * height / pred.orig_shape[0]), 0), 100),
                                "rectanglelabels": [label]
                            }
                        })

                results.append({
                    "result": task_preds,
                    "model_version": "yolov8_varroa_v1"
                })
                print(f"Detected {len(task_preds)} objects in {local_image_path}")

            except Exception as e:
                print(f"Prediction failed for {image_path}: {e}")
                traceback.print_exc()
                results.append({
                    "result": [],
                    "error": str(e),
                    "model_version": "yolov8_varroa_v1"
                })

        return results


# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

try:
    backend = YOLOv8Backend()
except Exception as e:
    print("Failed to initialize backend:", e)
    traceback.print_exc()
    backend = None

# Health endpoint
@app.route("/health")
def health():
    return jsonify({"status": "ok" if backend else "error"})

# Setup endpoint
@app.route("/setup", methods=["POST"])
def setup():
    return jsonify({
        "interfaces": ["image"],
        "label_config": """
<View>
  <Image name="image" value="$image" zoom="true"/>
  <RectangleLabels name="label" toName="image">
    <Label value="varoa" background="#FFA39E"/>
  </RectangleLabels>
</View>
"""
    })

# Predict endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.json
        print("Received payload:", payload)

        tasks = payload.get("tasks", [])
        if not tasks:
            return jsonify({"results": [], "error": "No tasks provided"})

        results = backend.predict(tasks)
        return jsonify({"results": results})

    except Exception as e:
        print("Prediction error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:9090")
    try:
        app.run(host="127.0.0.1", port=9090, debug=True)
    except Exception as e:
        print("Error running Flask server:", e)
        traceback.print_exc()
