from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, render_template, request
from werkzeug.utils import secure_filename

from .db import count_rows, execute, init_database
from .ml.agriculture import chatbot_reply, predict_soil, recommend_crop
from .ml.disease import DiseasePredictor

main = Blueprint("main", __name__)
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

@main.route("/")
def index():
    stats = {"predictions": count_rows("disease_predictions"), "chats": count_rows("chat_history"), "crops": count_rows("crop_recommendations"), "soil": count_rows("soil_predictions")}
    recent = execute("SELECT disease_name, confidence, created_at FROM disease_predictions ORDER BY id DESC LIMIT 4", fetchall=True) or []
    return render_template("index.html", stats=stats, recent_predictions=recent)

@main.route("/api/init-db", methods=["POST"])
def init_db_route():
    ok, message = init_database()
    return jsonify({"ok": ok, "message": message}), 200 if ok else 500

@main.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please type a farming question."}), 400
    reply = chatbot_reply(message)
    execute("INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)", (message, reply))
    return jsonify({"reply": reply})

@main.route("/api/disease", methods=["POST"])
def disease():
    file = request.files.get("leaf_image")
    if not file or not file.filename:
        return jsonify({"error": "Please upload a leaf image."}), 400
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"error": "Only PNG, JPG, JPEG, and WEBP images are allowed."}), 400
    filename = f"{uuid4().hex}_{secure_filename(file.filename)}"
    upload_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    file.save(upload_path)
    predictor = DiseasePredictor([current_app.config["MODEL_PATH"], current_app.config["FALLBACK_MODEL_PATH"]])
    try:
        result = predictor.predict(upload_path)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    image_url = f"/static/uploads/{filename}"
    execute("""INSERT INTO disease_predictions (image_path, disease_name, confidence, description_text, treatment, prevention) VALUES (%s, %s, %s, %s, %s, %s)""", (image_url, result["disease_name"], result["confidence"], result["description"], result["treatment"], result["prevention"]))
    result["image_url"] = image_url
    return jsonify(result)

@main.route("/api/soil", methods=["POST"])
def soil():
    keys = ["ph", "ec", "oc", "om", "n", "p", "k", "zn", "fe", "cu", "mn", "sand", "silt", "clay", "caco3", "cec"]
    try:
        values = {key: float(request.form[key]) for key in keys}
    except Exception:
        return jsonify({"error": "Please enter all soil values correctly."}), 400
    result = predict_soil(values)
    execute("""INSERT INTO soil_predictions (ph, ec, oc, om, n, p, k_value, zn, fe, cu, mn, sand, silt, clay, caco3, cec, result, fertilizer, suggestions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (values["ph"], values["ec"], values["oc"], values["om"], values["n"], values["p"], values["k"], values["zn"], values["fe"], values["cu"], values["mn"], values["sand"], values["silt"], values["clay"], values["caco3"], values["cec"], result["status"], result["fertilizer"], "; ".join(result["suggestions"])))
    return jsonify(result)

@main.route("/api/crop", methods=["POST"])
def crop():
    keys = ["n", "p", "k", "temperature", "humidity", "ph", "rainfall"]
    try:
        values = {key: float(request.form[key]) for key in keys}
    except Exception:
        return jsonify({"error": "Please enter all crop values correctly."}), 400
    result = recommend_crop(values)
    execute("""INSERT INTO crop_recommendations (n, p, k_value, temperature, humidity, ph, rainfall, crop_name, reason_text, tips) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (values["n"], values["p"], values["k"], values["temperature"], values["humidity"], values["ph"], values["rainfall"], result["crop"], result["reason"], result["tips"]))
    return jsonify(result)
