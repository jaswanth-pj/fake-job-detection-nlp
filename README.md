Fake Job Detection Using NLP and Machine Learning
Abstract

Online job portals have increasingly become a target for fraudulent activities, leading to financial and identity-related risks for job seekers. This project presents an intelligent system to detect fake job postings using Natural Language Processing (NLP) and Machine Learning techniques. The system combines statistical learning with rule-based detection to improve accuracy and reliability. User feedback is incorporated to continuously improve model performance through controlled retraining.

1. Introduction

Fake job postings are commonly used to exploit job seekers by requesting sensitive personal information, registration fees, or by offering unrealistic job guarantees. Traditional keyword-based filtering methods are insufficient to detect such scams effectively. This project addresses the problem by applying machine learning models trained on real-world job posting datasets, along with heuristic rules for identifying high-risk scam patterns.

2. Objectives

To classify job postings as Real or Fake using NLP techniques

To build a user-friendly web interface for job verification

To support image-based job detection using OCR

To implement an admin dashboard for monitoring system performance

To incorporate user feedback and enable automated model retraining

3. System Architecture

The system follows a client–server architecture:

Frontend: React.js (Vite)

Backend: Flask (REST API)

Database: SQLite

ML Engine: Scikit-learn

OCR Engine: Tesseract OCR

The frontend communicates with the backend via RESTful APIs. The backend processes text, performs prediction, stores results, and provides analytics to administrators.

4. Machine Learning Methodology
4.1 Text Preprocessing

Lowercasing

Removal of URLs and email addresses

Removal of numeric characters

Removal of special symbols

4.2 Feature Extraction

TF-IDF (Term Frequency–Inverse Document Frequency) is used to convert text into numerical vectors.

4.3 Classification Model

Logistic Regression is employed due to its efficiency, interpretability, and strong performance on text classification tasks.

4.4 Hybrid Detection Strategy

To improve reliability, the system integrates:

Machine Learning Prediction

Rule-Based Scam Detection, targeting indicators such as:

No interview required

Requests for PAN/Aadhaar/Bank details

Telegram or WhatsApp-based communication

Registration or verification fees

5. Feedback and Retraining Mechanism

Users can flag incorrect predictions. Flagged job postings are stored in the database and automatically included in retraining once a predefined threshold is reached. This controlled retraining strategy prevents overfitting while ensuring continuous model improvement.

6. Functional Modules
6.1 User Module

User registration and login

Text-based job verification

Image-based job verification using OCR

Confidence score display

Prediction history

Feedback submission

6.2 Admin Module

Admin dashboard with analytics

User and role management

Fake vs Real job statistics

Flagged post monitoring

CSV export of predictions

Retraining trigger monitoring

7. Technology Stack
Frontend

React.js (Vite)

JavaScript

CSS

Backend:

Python (Flask)

Flask-CORS

SQLite

Machine Learning

Scikit-learn

TF-IDF Vectorizer

Logistic Regression

OCR

Tesseract OCR

OpenCV

8. Project Structure
jobcheck/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── database.py
│   ├── ocr_utils.py
│   └── model/
├── frontend_react/
│   ├── src/
│   ├── public/
│   └── package.json
├── dataset/
├── scripts/
├── README.md
└── .gitignore

9. Installation and Execution
Backend
cd backend
python app.py

Frontend
cd frontend_react
npm install
npm run dev

10. Results

The system successfully identifies fraudulent job postings using a hybrid detection approach. The integration of rule-based detection significantly improves the identification of emerging scam patterns not adequately represented in training data.

11. Limitations

Performance depends on training data distribution

Advanced scams may require deeper semantic models

OCR accuracy depends on image quality.

12. Conclusion

This project demonstrates an effective approach to detecting fake job postings using NLP and machine learning. By combining statistical learning, rule-based checks, and user feedback, the system provides a robust and scalable solution to a real-world problem.

Author

Pallikonda Penchala Jaswanth 
Internship Project – Infosys Springboard

GitHub Repository
https://github.com/jaswanth-pj/fake-job-detection-nlp

