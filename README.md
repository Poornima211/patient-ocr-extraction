# Patient Assessment OCR Extraction

## Overview
This project automates the extraction of patient assessment data from scanned forms (JPEG/PDF) using OCR and stores the structured data in an SQLite database.

## Features
- Extracts handwritten and printed text using **Tesseract OCR**
- Preprocesses images (grayscale, thresholding) for improved accuracy
- Parses extracted text into structured **JSON format**
- Stores patient details and form data in an **SQLite database**

## Setup Instructions
### Prerequisites
- Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Install required Python packages:
  ```sh
  pip install pytesseract pdf2image opencv-python sqlalchemy pillow
  ```

### Usage
1. Run the script:
   ```sh
   python ocr_extraction.py
   ```
2. Enter the path of a scanned **JPEG/PDF** form when prompted.
3. The extracted data will be stored in the `patients.db` database.

## Database Schema
- `patients` table stores patient name & date of birth.
- `forms_data` table stores the structured JSON form data.

## Example JSON Output
```json
{
  "patient_name": "John Doe",
  "dob": "01/05/1988",
  "date": "02/06/2025",
  "injection": "Yes",
  "exercise_therapy": "No",
  "difficulty_ratings": { "bending": 3, "putting_on_shoes": 1, "sleeping": 2 },
  "pain_symptoms": { "pain": 2, "numbness": 5, "tingling": 6 },
  "medical_assistant_data": { "blood_pressure": "120/80", "hr": 80, "weight": 67 }
}
```

## License
MIT License.
