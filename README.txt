# 🍷 BABYLON — Premium Restaurant & Lounge Website  
A modern, high-end restaurant website featuring an elegant pink–white aesthetic, a full reservation system, and a refined dining brand experience. Built with **Flask**, **HTML**, **CSS**, and **SQLite**, Babylon offers a premium interface that feels warm, stylish, and professional.

---

## ✨ Overview
Babylon is a premium pub & night-kitchen experience translated into a beautifully designed web application.  
The website includes a luxury-styled reservation section, rich visuals, multi-page layout, and automated email confirmations for guests.

The goal:  
**Deliver a premium, upscale, modern restaurant website that feels real and production-ready.**

---

## 🎨 Features

### 🍽 Frontend (UI/UX)
- Premium pink–white luxury theme  
- Responsive design across all devices  
- Elegant hero section, on-scroll visuals, and soft shadows  
- Multi-page structure:
  - **Home / Reservations**
  - **Menu**
  - **Gallery**
  - **Contact**
- Smooth modal popup for successful reservations  
- High-quality card layout for gallery & blogs  

### 🛎 Reservation Engine
- Accepts:
  - Name  
  - Email  
  - Phone number  
  - Number of guests  
  - Date  
  - Time  
  - 18+ Confirmation  
- Validations:
  - Phone format  
  - Email format  
  - Available hours (11:30 AM – 11:00 PM only)  
- Stores reservations into **SQLite database**  
- Auto-sends confirmation email using:
  - **SendGrid API** (recommended)  
  - Or Gmail SMTP fallback  

### 🔐 Security & Best Practices
- `.env` file to store all secrets  
- Git-safe: env/db ignored  
- Clean backend code with safe validation  

---

## 🛠 Technology Stack

### Frontend
- HTML5  
- CSS3 (custom premium styling)  
- JavaScript (fetch + modals)  
- Google Fonts (Playfair Display + Inter)

### Backend
- Python  
- Flask  
- SQLite  
- SendGrid API  
- SMTP (Gmail App Password)  
- dotenv  

---

## 📂 Project Structure

restaurant-website/
│
├── server.py # Flask backend
├── index.html # Home / Reservation page
├── menu.html # Menu
├── gallery.html # Gallery
├── contact.html # Contact page
│
├── images/ # All images
├── reservations.db # Database (ignored in Git)
├── .env # Secrets (ignored in Git)
├── .gitignore
└── README.md

---

## ⚙️ Local Setup Guide

### 1️⃣ Clone the repository
```bash
git clone https://github.com/adeeshreddi/restaurant-website.git
cd restaurant-website

2️⃣ Create a virtual environment
python -m venv venv
Activate it: venv\Scripts\activate

3️⃣ Install required packages
pip install flask python-dotenv requests


4️⃣ Create your .env file
SENDGRID_API_KEY=
EMAIL_FROM=yourgmail@gmail.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=yourgmail@gmail.com
SMTP_PASS=your_16_char_app_password

DB_FILE=reservations.db
5️⃣ Run the server
python server.py
6️⃣ Open the website
http://127.0.0.1:5000
👤 Author

Aadeesh Reddi
GitHub: @adeeshreddi





