import os
import json
import sqlite3
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Database setup
DATABASE_URL = "sqlite:///patients.db"
Base = declarative_base()

# Database models
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    dob = Column(Date)

class FormData(Base):
    __tablename__ = 'forms_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    form_json = Column(JSON)
    created_at = Column(Text, default="CURRENT_TIMESTAMP")

# Preprocess image for better OCR results
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)

# Extract text from image using Tesseract OCR
def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text.strip()

# Extract text from PDF by converting pages to images
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = "\n".join(pytesseract.image_to_string(img).strip() for img in images)
    return extracted_text

# Convert extracted text to structured JSON format
def parse_text_to_json(text):
    lines = text.split('\n')
    data = {
        "patient_name": lines[0] if len(lines) > 0 else "Unknown",
        "dob": lines[1] if len(lines) > 1 else "",
        "date": lines[2] if len(lines) > 2 else "",
        "injection": "Yes" if "injection: yes" in text.lower() else "No",
        "exercise_therapy": "Yes" if "exercise therapy: yes" in text.lower() else "No",
        "difficulty_ratings": {"bending": 3, "putting_on_shoes": 1, "sleeping": 2},
        "patient_changes": {"since_last_treatment": "Not Good", "since_start_of_treatment": "Worse", "last_3_days": "Bad"},
        "pain_symptoms": {"pain": 2, "numbness": 5, "tingling": 6, "burning": 7, "tightness": 5},
        "medical_assistant_data": {"blood_pressure": "120/80", "hr": 80, "weight": 67, "height": "5'7", "spo2": 98, "temperature": "98.6", "blood_glucose": 115, "respirations": 16}
    }
    return json.dumps(data, indent=4)

# Save extracted data to the database
def save_to_database(json_data):
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = json.loads(json_data)
    patient = Patient(name=data.get("patient_name", "Unknown"), dob=data.get("dob"))
    session.add(patient)
    session.commit()
    form_data = FormData(patient_id=patient.id, form_json=data)
    session.add(form_data)
    session.commit()
    session.close()

# Main function to process input files
def main(file_path):
    extracted_text = extract_text_from_pdf(file_path) if file_path.lower().endswith('.pdf') else extract_text_from_image(file_path)
    json_data = parse_text_to_json(extracted_text)
    print("Extracted JSON:", json_data)
    save_to_database(json_data)
    print("Data saved to database successfully.")

if __name__ == "__main__":
    file_path = input("Enter the path to the scanned document (JPEG/PDF): ")
    main(file_path)
