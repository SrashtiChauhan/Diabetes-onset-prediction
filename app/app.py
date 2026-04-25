from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

#load model files
try:
    model = joblib.load("../model/xgb_model.pkl")
    threshold = joblib.load("../model/threshold.pkl")
    feature_order = joblib.load("../model/feature_order.pkl")
except Exception as e:
    raise RuntimeError(f"Error loading model files: {e}")


# home route
@app.route("/")
def home():
    return jsonify({"message": "Diabetes Prediction API is running 🚀"})


# healthy check
@app.route("/health")
def health():
    return jsonify({"status": "OK"})


# prediction route
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

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
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400

    # range validation
    if not (0 <= glucose <= 300):
        return jsonify({"error": "Glucose out of range"}), 400

    if not (10 <= bmi <= 60):
        return jsonify({"error": "BMI out of range"}), 400

    if not (1 <= age <= 120):
        return jsonify({"error": "Age out of range"}), 400


    # feature engineering
    bmi_cat = 0 if bmi < 18.5 else 1 if bmi < 25 else 2 if bmi < 30 else 3
    age_group = 0 if age < 30 else 1 if age < 50 else 2
    glucose_risk = 0 if glucose < 100 else 1 if glucose < 140 else 2
    high_insulin = 1 if insulin > 150 else 0
    high_bp = 1 if bp > 80 else 0


    #  feature vector
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

    try:
        features = np.array([[input_dict[col] for col in feature_order]])
    except KeyError as e:
        return jsonify({"error": f"Feature mismatch: {e}"}), 500


    # prediction
    prob = float(model.predict_proba(features)[0][1])
    prediction = int(prob > threshold)
    label = "Diabetic" if prediction == 1 else "Not Diabetic"


    # result
    return jsonify({
        "prediction": prediction,
        "label": label,
        "probability": round(prob, 3)
    })


if __name__ == "__main__":
    app.run(debug=True)
