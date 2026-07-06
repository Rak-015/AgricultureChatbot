from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from groq import Groq
client = Groq(api_key=GROQ_API_KEY)


CHAT_KNOWLEDGE = {
    "soil": "For healthy soil, test pH and nutrients first. Most crops prefer pH 6.0 to 7.5, good organic matter, proper drainage, and balanced NPK fertilizer.",
    "fertilizer": "Use fertilizer based on soil test results. Nitrogen supports leaves, phosphorus improves roots and flowering, and potassium improves stress tolerance.",
    "irrigation": "Irrigate early morning or evening. Prefer drip irrigation, avoid waterlogging, and increase care during flowering and fruit formation.",
    "pest": "Use integrated pest management: field scouting, traps, clean cultivation, biological control, and chemical sprays only when needed.",
    "disease": "Remove infected leaves, improve airflow, avoid overhead irrigation, rotate crops, and use resistant varieties. Treat early when symptoms appear.",
    "season": "Choose crop timing based on rainfall, temperature, soil moisture, and market demand. Prepare seed, fertilizer, and irrigation before sowing.",
    "crop": "Crop choice depends on NPK, pH, rainfall, temperature, soil texture, water availability, and local market conditions.",
}

CROP_RULES = [
    ("Rice", lambda d: d["rainfall"] >= 180 and d["humidity"] >= 70 and 5.0 <= d["ph"] <= 7.5, "High rainfall and humidity suit paddy cultivation."),
    ("Maize", lambda d: 18 <= d["temperature"] <= 32 and 5.5 <= d["ph"] <= 7.5 and d["n"] >= 40, "Temperature, nitrogen, and pH support maize growth."),
    ("Cotton", lambda d: d["temperature"] >= 24 and d["rainfall"] < 120 and 6.0 <= d["ph"] <= 8.0, "Warm weather and moderate rainfall are suitable for cotton."),
    ("Tomato", lambda d: 18 <= d["temperature"] <= 30 and 55 <= d["humidity"] <= 85 and 5.5 <= d["ph"] <= 7.5, "Balanced pH and moderate humidity support tomato."),
    ("Potato", lambda d: 12 <= d["temperature"] <= 25 and 5.0 <= d["ph"] <= 6.8, "Cool conditions and slightly acidic soil are suitable for potato."),
    ("Wheat", lambda d: 10 <= d["temperature"] <= 25 and d["rainfall"] < 120 and 6.0 <= d["ph"] <= 7.8, "Cool season temperature and moderate water suit wheat."),
    ("Sugarcane", lambda d: d["temperature"] >= 22 and d["rainfall"] >= 100 and d["k"] >= 40, "Warm climate, moisture, and potassium favor sugarcane."),
    ("Groundnut", lambda d: 20 <= d["temperature"] <= 32 and 5.8 <= d["ph"] <= 7.2 and d["rainfall"] < 120, "Light soil, warm weather, and moderate rainfall suit groundnut."),
]

def chatbot_reply(message):
    try:
        response = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[
            {"role": "system",
             "content": (
                 "You are an expert agricultural assistant. Provide concise, practical, and actionable advice to farmers based on their queries."
                 "Answer only agriculture-related questions. If the question is unrelated, politely decline to answer."
                 "Reply in plain text without markdown, asterisks, or special symbols"
             ),
            },
            {
                "role":"user",
                "content": message,
            },
        ],
        temperature=0.3,
        max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error in generating response: {str(e)}"

        
def recommend_crop(values):
    for crop, rule, reason in CROP_RULES:
        if rule(values):
            return {"crop": crop, "reason": reason, "tips": crop_tips(crop)}
    return {"crop": "Millet", "reason": "The entered values are mixed; millet is hardy and adapts well to many local conditions.", "tips": crop_tips("Millet")}

def crop_tips(crop):
    tips = {"Rice": "Maintain standing water only when needed, transplant healthy seedlings, and monitor stem borer.", "Maize": "Use proper spacing, apply nitrogen in splits, and control weeds during early growth.", "Cotton": "Monitor pests, avoid excess nitrogen, and ensure drainage during heavy rain.", "Tomato": "Stake plants, use drip irrigation, mulch, and monitor whiteflies and blight.", "Potato": "Use disease-free seed tubers, ridge properly, and protect against late blight.", "Wheat": "Sow on time, irrigate at crown root and grain filling stages, and control weeds early.", "Sugarcane": "Use healthy setts, maintain moisture, and apply potassium for cane strength.", "Groundnut": "Use well-drained soil, apply gypsum at pegging, and avoid waterlogging.", "Millet": "Sow on time, keep spacing uniform, and add organic matter for better establishment."}
    return tips.get(crop, "Follow local agronomy recommendations and monitor regularly.")

def predict_soil(values):
    score = 0
    score += 2 if 6.0 <= values["ph"] <= 7.8 else -1
    score += 1 if values["ec"] <= 1.0 else -1
    score += 2 if values["oc"] >= 0.5 or values["om"] >= 1.0 else -1
    score += 1 if values["n"] >= 280 else -1
    score += 1 if values["p"] >= 10 else -1
    score += 1 if values["k"] >= 110 else -1
    score += 1 if values["cec"] >= 10 else -1
    score += 1 if 20 <= values["clay"] <= 45 else 0
    status = "Fertile" if score >= 5 else "Non-Fertile"
    suggestions = []
    if values["ph"] < 6.0: suggestions.append("Apply agricultural lime gradually to correct acidic soil.")
    elif values["ph"] > 7.8: suggestions.append("Add compost and gypsum where locally recommended to manage alkalinity.")
    if values["oc"] < 0.5 and values["om"] < 1.0: suggestions.append("Increase organic matter using compost, farmyard manure, green manure, or residue.")
    if values["n"] < 280: suggestions.append("Apply nitrogen in split doses using urea or organic nitrogen sources.")
    if values["p"] < 10: suggestions.append("Use phosphorus fertilizer such as DAP or SSP based on soil test advice.")
    if values["k"] < 110: suggestions.append("Apply potash fertilizer and recycle crop residues where possible.")
    if values["zn"] < 0.6: suggestions.append("Apply zinc sulphate for zinc deficiency.")
    if not suggestions: suggestions.append("Maintain fertility with balanced fertilizer, compost, and regular soil testing.")
    fertilizer = "Balanced NPK with compost" if status == "Fertile" else "Soil-test based NPK, compost/FYM, and required micronutrients"
    return {"status": status, "fertilizer": fertilizer, "suggestions": suggestions}
