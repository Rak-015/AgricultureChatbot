# AGRI-BOT - AI Powered Agriculture Assistant

AGRI-BOT is a complete Flask and MySQL localhost project for academic submission. It provides plant disease detection using the supplied MobileNet model, an agriculture chatbot, crop recommendation, soil fertility prediction, treatment suggestions, and a professional dashboard.

## Features

- Responsive farmer-friendly UI based on the supplied agriculture robot reference image
- MobileNet disease detection for corn, potato, and tomato leaves
- Disease name, confidence, description, treatment, and prevention output
- Agriculture chatbot with chat history stored in MySQL
- Soil fertility prediction from pH, EC, OC, OM, N, P, K, Zn, Fe, Cu, Mn, Sand, Silt, Clay, CaCO3, and CEC
- Crop recommendation from N, P, K, temperature, humidity, pH, and rainfall
- Dashboard cards for predictions, chats, crop recommendations, and soil predictions
- MySQL schema and one-click database initializer from the dashboard

## Folder Structure

~~~text
agri-bot/
  app/
    ml/agriculture.py
    ml/disease.py
    ml/mobilenet.h5
    static/css/style.css
    static/images/agri-bot-hero.jpeg
    static/js/app.js
    static/uploads/
    templates/index.html
    __init__.py
    db.py
    routes.py
  database/schema.sql
  config.py
  run.py
  requirements.txt
  .env.example
~~~

## Setup in Visual Studio Code

Important: Use Python 3.10 or Python 3.11 for this project. TensorFlow does not support Python 3.14 yet.


1. Open the agri-bot folder in VS Code.
2. Create and activate a virtual environment:

~~~bash
python -m venv venv
venv\Scripts\activate
~~~

3. Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

4. Copy `.env.example` to `.env` and update your MySQL password.
5. Make sure MySQL Server is running.
6. Start the app:

~~~bash
python run.py
~~~

7. Open `http://127.0.0.1:5000`.
8. Click `Initialize DB` once from the dashboard to create the MySQL tables.

## Model Integration

The app expects the trained MobileNet model at `app/ml/mobilenet.h5`. No retraining is required. If the file is missing, copy the supplied `mobilenet.h5` into `app/ml/` or set `MODEL_PATH` in `.env`.

## Supported Disease Classes

1. Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot
2. Corn_(maize)___Common_rust_
3. Corn_(maize)___healthy
4. Corn_(maize)___Northern_Leaf_Blight
5. Potato___Early_blight
6. Potato___healthy
7. Potato___Late_blight
8. Tomato___Bacterial_spot
9. Tomato___healthy
10. Tomato___Late_blight
11. Tomato___Tomato_Yellow_Leaf_Curl_Virus

## Notes

- The project runs on localhost.
- The chatbot is local and does not need an external API key.
- Database failures are handled gracefully, but MySQL should be initialized before the final demo for persistent dashboard counts.
