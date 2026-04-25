from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# load files and models
model = joblib.load("../model/xgb_model.pkl")
threshold = joblib.load("../model/threshold.pkl")
feature_order = joblib.load("../model/feature_order.pkl")  # saved during training


# route
@app.route("/")
def home():
    return "Diabetes Prediction API is running 🚀"


# prediction route
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    # input validation
    required_fields = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is missing"}), 400

    try:
        pregnancies = int(data["Pregnancies"])
        glucose = float(data["Glucose"])
        bp = float(data["BloodPressure"])
        skin = float(data["SkinThickness"])
        insulin = float(data["Insulin"])
        bmi = float(data["BMI"])
        dpf = float(data["DiabetesPedigreeFunction"])
        age = int(data["Age"])
    except:
        return jsonify({"error": "Invalid data type"}), 400

    # Range validation
    if not (0 <= glucose <= 300):
        return jsonify({"error": "Glucose out of range"}), 400

    if not (10 <= bmi <= 60):
        return jsonify({"error": "BMI out of range"}), 400

    if not (1 <= age <= 120):
        return jsonify({"error": "Age out of range"}), 400


    # feature engineering

    # BMI Category
    if bmi < 18.5:
        bmi_cat = 0
    elif bmi < 25:
        bmi_cat = 1
    elif bmi < 30:
        bmi_cat = 2
    else:
        bmi_cat = 3

    # Age Group
    if age < 30:
        age_group = 0
    elif age < 50:
        age_group = 1
    else:
        age_group = 2

    # Glucose Risk
    if glucose < 100:
        glucose_risk = 0
    elif glucose < 140:
        glucose_risk = 1
    else:
        glucose_risk = 2

    # High Insulin
    high_insulin = 1 if insulin > 150 else 0

    # High BP
    high_bp = 1 if bp > 80 else 0


    # feature order
    input_dict = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": bp,
        "SkinThickness": skin,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age,
        "BMI_Category": bmi_cat,
        "Age_Group": age_group,
        "Glucose_Risk": glucose_risk,
        "High_Insulin": high_insulin,
        "High_BP": high_bp
    }

    features = np.array([[input_dict[col] for col in feature_order]])


    # prediction
    prob = model.predict_proba(features)[0][1]
    prediction = int(prob > threshold)

    result = "Diabetic" if prediction == 1 else "Not Diabetic"


    # output result
    return jsonify({
    "prediction": prediction,  
    "label": result,           
    "probability": round(float(prob), 3)
})



if __name__ == "__main__":
    app.run(debug=True)