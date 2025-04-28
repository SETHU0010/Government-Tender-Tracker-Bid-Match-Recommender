# Government Tender Tracker & Bid-Match Recommender

## 🚀 Objective
Develop a **Streamlit** web application that:
- Aggregates tender notices from **Central (CPPP, GeM)** and **State e-procurement** portals.
- Matches tenders to a company's capability profile.
- Displays recommendations through an intuitive dashboard.
- (Optional) Sends real-time tender alerts via **SMS** (Twilio) or **Email** (Gmail SMTP).

---

## 📌 Problem Statement
Organizations often miss tender opportunities due to:
- Time-consuming manual monitoring of multiple portals.
- Difficulty matching tenders with internal capabilities.

This project automates:
- Tender fetching and parsing.
- Intelligent matching using text similarity (TF-IDF and Cosine Similarity).
- Real-time tender recommendation and notifications.

---

## 🛠️ Tech Stack
- **Backend**: Python (requests, BeautifulSoup, pdfplumber, scikit-learn)
- **Frontend**: Streamlit
- **Notifications**: Twilio SMS / Gmail SMTP (optional)
- **Others**: OAuth2 (for Gmail integration)

---

## 🏗️ Architecture

```plaintext
Tender Portals (CPPP, GeM, State)
    ↓
Fetch Tender Data (requests, BeautifulSoup)
    ↓
Extract Information (pdfplumber, text parsing)
    ↓
Company Profile Upload (PDF/Text)
    ↓
Profile Matching (TF-IDF + Cosine Similarity)
    ↓
Streamlit Dashboard (View Matches, Search, Upload)
    ↓
(Optional) Notifications (Twilio SMS / Gmail Email)
