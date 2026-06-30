# Credit_Card_Fraud_Detection_using_Machine_learning

A Machine Learning-based web application developed using **Python**, **Django**, and **Scikit-learn** to detect fraudulent credit card transactions. The system analyzes transaction details such as amount, location, category, and customer information to predict whether a transaction is fraudulent or legitimate.

---

##  Project Overview

Credit card fraud is one of the major challenges faced by financial institutions. This project uses Machine Learning algorithms to identify fraudulent transactions based on transaction features.

The application provides:

- User Registration & Login
- Admin Login
- Credit Card Transaction Prediction
- Fraud Detection using Machine Learning
- Prediction Result Storage
- User-Friendly Django Web Interface

---

##   Features

-   User Authentication (Register/Login)
-   Admin Panel
-   Credit Card Fraud Prediction
-   Random Forest Machine Learning Model
-   CSV Dataset Integration
-   SQLite Database
-   Responsive Web Interface using Bootstrap

---

##  Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Backend
- Python
- Django

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

### Database
- SQLite

---

## 📂 Project Structure

```
CreditCard/
│
├── CreditCard/          # Django Project
├── User/                # Django App
├── static/
│   ├── css/
│   ├── images/
│   └── dataset/
│       └── CreditCard.csv
├── templates/
├── db.sqlite3
├── manage.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

git clone https://github.com/your-username/CreditCard_fixed.git

### 2. Go to Project Folder

cd CreditCard_fixed

### 3. Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Linux/Mac

python3 -m venv venv
source venv/bin/activate

### 4. Install Dependencies

pip install django
pip install pandas
pip install numpy
pip install scikit-learn

Or
pip install -r requirements.txt

---

##  Run the Project

Apply migrations
python manage.py migrate

Run server
python manage.py runserver

Open
http://127.0.0.1:8000/

---

## 👩‍💻 Developed By

**Rachana H B - MCA, Presidency University, Bengaluru
