from pathlib import Path

import numpy as np
from PIL import Image

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import img_to_array
except Exception as e:
    print("TensorFlow Import Error:", e)
    load_model = None
    img_to_array = None

DISEASE_CLASSES = [
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___healthy",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato___Bacterial_spot",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
]

DISEASE_INFO = {
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {"name": "Corn Gray Leaf Spot", "description": "A fungal disease that creates rectangular gray or tan lesions and reduces photosynthesis.", "treatment": "Apply a locally recommended fungicide at early symptoms, remove infected residue, and improve airflow.", "prevention": "Rotate crops, use tolerant hybrids, avoid overhead irrigation, and manage crop residue."},
    "Corn_(maize)___Common_rust_": {"name": "Corn Common Rust", "description": "Rust-colored pustules form on leaf surfaces during cool and humid weather.", "treatment": "Use a labeled fungicide if infection appears before tasseling and weather remains favorable.", "prevention": "Choose resistant varieties, monitor early, and avoid very dense planting."},
    "Corn_(maize)___healthy": {"name": "Healthy Corn Leaf", "description": "The uploaded leaf does not show disease symptoms detected by the model.", "treatment": "No disease treatment is required. Continue normal crop care.", "prevention": "Maintain balanced nutrition, timely irrigation, and regular scouting."},
    "Corn_(maize)___Northern_Leaf_Blight": {"name": "Corn Northern Leaf Blight", "description": "Long cigar-shaped lesions appear on leaves and can spread quickly in humid conditions.", "treatment": "Protect upper leaves with fungicide when disease pressure is high.", "prevention": "Use resistant hybrids, rotate crops, and remove or bury infected residue."},
    "Potato___Early_blight": {"name": "Potato Early Blight", "description": "Dark concentric leaf spots weaken the crop and reduce tuber yield.", "treatment": "Remove badly affected leaves and apply mancozeb or chlorothalonil as locally recommended.", "prevention": "Use certified seed, rotate crops, mulch soil, and avoid water stress."},
    "Potato___healthy": {"name": "Healthy Potato Leaf", "description": "The uploaded potato leaf appears healthy according to the model.", "treatment": "No immediate disease treatment is needed.", "prevention": "Keep field sanitation strong and monitor weekly for early symptoms."},
    "Potato___Late_blight": {"name": "Potato Late Blight", "description": "A destructive disease with water-soaked lesions and white growth during moist weather.", "treatment": "Destroy infected foliage safely and apply a recommended systemic fungicide urgently.", "prevention": "Plant certified seed, improve drainage, avoid overhead watering, and follow blight alerts."},
    "Tomato___Bacterial_spot": {"name": "Tomato Bacterial Spot", "description": "Small dark lesions appear on leaves and fruit, often spread by splashing water.", "treatment": "Remove infected leaves and use copper-based sprays as advised by local experts.", "prevention": "Use disease-free seed, drip irrigation, crop rotation, and avoid handling wet plants."},
    "Tomato___healthy": {"name": "Healthy Tomato Leaf", "description": "No disease symptoms were detected by the model.", "treatment": "No treatment is required.", "prevention": "Maintain staking, airflow, balanced fertilizer, and regular pest checks."},
    "Tomato___Late_blight": {"name": "Tomato Late Blight", "description": "Fast-spreading lesions and leaf collapse can occur during wet, cool weather.", "treatment": "Remove infected plant material and apply recommended fungicide quickly.", "prevention": "Use resistant varieties, avoid overhead irrigation, and remove volunteer tomato plants."},
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {"name": "Tomato Yellow Leaf Curl Virus", "description": "A whitefly-spread viral disease causing yellow curled leaves and stunted growth.", "treatment": "There is no cure. Remove infected plants and manage whiteflies immediately.", "prevention": "Use resistant varieties, insect-proof nursery netting, yellow traps, and whitefly control."},
}

class DiseasePredictor:
    def __init__(self, model_paths):
        self.model_paths = [Path(path) for path in model_paths if path]
        self.model = None
        self.error = None

    def load(self):
        if self.model is not None:
            return self.model
        if load_model is None:
            self.error = "TensorFlow is not installed. Install requirements before prediction."
            return None
        for model_path in self.model_paths:
            if model_path.exists():
                self.model = load_model(model_path, compile=False)
                self.error = None
                return self.model
        self.error = "MobileNet model file was not found. Copy mobilenet.h5 into app/ml or set MODEL_PATH."
        return None

    def predict(self, image_path):
        model = self.load()
        if model is None:
            raise RuntimeError(self.error)
        image = Image.open(image_path).convert("RGB").resize((224, 224))
        array = img_to_array(image) / 255.0
        array = np.expand_dims(array, axis=0)
        predictions = model.predict(array, verbose=0)[0]
        index = int(np.argmax(predictions))
        confidence = float(predictions[index]) * 100
        class_key = DISEASE_CLASSES[index]
        info = DISEASE_INFO[class_key]
        return {"class_key": class_key, "disease_name": info["name"], "confidence": round(confidence, 2), "description": info["description"], "treatment": info["treatment"], "prevention": info["prevention"]}
