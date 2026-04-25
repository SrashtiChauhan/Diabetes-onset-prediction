# 🩺 Diabetes Onset Prediction System

A Machine Learning-powered web application that predicts the likelihood of diabetes using patient health parameters.

---

## 🚀 Features

* 🔍 Diabetes prediction using **XGBoost**
* ⚙️ Feature engineering (BMI category, glucose risk, etc.)
* 🎯 Threshold tuning for improved recall
* 🌐 Flask API backend
* 🎨 Streamlit interactive UI
* 📊 Risk visualization (gauge chart)
* 📄 Downloadable patient report (PDF)
* ✅ Input validation for robust predictions

---

## 🧠 Machine Learning Details

* **Model:** XGBoost Classifier
* **Accuracy:** ~75%
* **F1 Score:** ~0.67
* **ROC-AUC:** ~0.82

### Feature Engineering

* BMI Category
* Age Group
* Glucose Risk
* High Blood Pressure
* High Insulin

---

## 📁 Project Structure

```
Diabetes-onset-prediction/
│
├── app/
│   ├── app.py        # Flask API
│   ├── ui.py         # Streamlit UI
│
├── model/
│   ├── xgb_model.pkl
│   ├── threshold.pkl
│   ├── feature_order.pkl
│
├── data/
│   └── diabetes.csv
│
├── notebook/
│   └── eda.ipynb     # Training + EDA
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/SrashtiChauhan/Diabetes-onset-prediction.git
cd Diabetes-onset-prediction
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Backend (Flask)

```bash
cd app
python app.py
```

### 4️⃣ Run Frontend (Streamlit)

```bash
streamlit run ui.py
```

---

## 🧪 Sample Input

```json
{
  "Pregnancies": 1,
  "Glucose": 95,
  "BloodPressure": 70,
  "SkinThickness": 20,
  "Insulin": 80,
  "BMI": 22,
  "DiabetesPedigreeFunction": 0.3,
  "Age": 25
}
```

---

## 📊 Output

* Prediction: **Diabetic / Not Diabetic**
* Probability score
* Risk visualization (gauge)
* Downloadable PDF report

---

## 🔐 Notes

* Model files are included for easy execution

---

## ⭐ Future Improvements

* Add authentication system
* Store patient history
* Deploy to cloud (Render / Streamlit Cloud)
* Improve model performance

---

## 🧑‍💻 Author

**Srashti Chauhan**
BTech CSE

