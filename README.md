# 🧑‍⚖️ Online Lawyer Booking System

A web-based platform for booking appointments with lawyers, built using **Django**, **Pillow**, **HTML**, **CSS**, **JavaScript**, and **Python**.

## 🚀 Features
- Lawyer & Client Registration/Login
- Lawyer profiles with specialization & availability
- Search & filter lawyers
- Appointment booking system
- Admin panel for user & appointment management
- Image upload using Pillow

## 💻 Tech Stack
- **Backend:** Django, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Image Handling:** Pillow

## ⚙️ How to Run
```bash
git clone https://github.com/gaddamsudeeksha/online-lawyer-booking.git
cd online-lawyer-booking
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
