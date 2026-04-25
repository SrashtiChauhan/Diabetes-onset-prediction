import streamlit as st
import requests
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# config
API_URL = "http://127.0.0.1:5000/predict"

st.set_page_config(page_title="Diabetes Predictor", layout="centered")

# css 
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# guage function
def create_gauge(prob):
    color = "green" if prob < 0.3 else "orange" if prob < 0.6 else "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={'text': "Diabetes Risk (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"},
            ],
        }
    ))
    return fig

# pdf generator
def generate_pdf(result, prob, data):
    file_path = "diabetes_report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Diabetes Prediction Report</b>", styles['Title']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Prediction:</b> {result}", styles['Normal']))
    content.append(Paragraph(f"<b>Probability:</b> {prob*100:.2f}%", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Patient Inputs:</b>", styles['Heading2']))

    for key, value in data.items():
        content.append(Paragraph(f"{key}: {value}", styles['Normal']))

    doc.build(content)
    return file_path

# title
st.title("🩺 Diabetes Risk Prediction System")
st.write("Enter patient details to predict diabetes risk")

#input form
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", 0, 20, step=1)
    glucose = st.number_input("Glucose", 0.0, 300.0)
    bp = st.number_input("Blood Pressure", 0.0, 200.0)
    skin = st.number_input("Skin Thickness", 0.0, 100.0)

with col2:
    insulin = st.number_input("Insulin", 0.0, 500.0)
    bmi = st.number_input("BMI", 0.0, 60.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 2.5)
    age = st.number_input("Age", 1, 120)

# input validation
def validate_inputs():
    if glucose == 0 or bmi == 0:
        st.error("⚠️ Glucose and BMI cannot be 0")
        return False
    if age < 1:
        st.error("⚠️ Age must be valid")
        return False
    return True

# prediction
if st.button("🔍 Predict Risk"):

    if not validate_inputs():
        st.stop()

    input_data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": bp,
        "SkinThickness": skin,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age
    }

    try:
        response = requests.post(API_URL, json=input_data, timeout=5)

        if response.status_code == 200:
            result = response.json()

            prob = result["probability"]
            label = result["prediction"]

            st.subheader("🧾 Prediction Result")

            if label == "Diabetic":
                st.error(f"⚠️ {label}")
            else:
                st.success(f"✅ {label}")

            # Gauge
            st.plotly_chart(create_gauge(prob), use_container_width=True)

            # Risk interpretation
            if prob < 0.3:
                st.success("Low Risk → Maintain healthy lifestyle ✅")
            elif prob < 0.6:
                st.warning("Moderate Risk → Consider medical checkup ⚠️")
            else:
                st.error("High Risk → Consult doctor immediately 🚨")

            # =========================
            # PDF DOWNLOAD
            # =========================
            pdf_path = generate_pdf(label, prob, input_data)

            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📄 Download Patient Report",
                    data=file,
                    file_name="diabetes_report.pdf",
                    mime="application/pdf"
                )

        else:
            st.error("❌ API Error")

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running. Start Flask first.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

        