# 📚 Dhee: AI Tutor  

**Dhee** is a lightweight AI-powered tutoring platform designed to help students learn through interactive tests, courses, and AI-guided assistance.  
It provides features like **user authentication, test generation, dashboard for courses, and structured study material** – all in one place.  

---

##  Features

-  **User Authentication**  
  - Signup, Login, and OTP Verification  
  - Passwords are securely hashed before storage  

-  **Courses & Notes**  
  - View course material and downloadable notes (PDF)  

-  **Test Generation**  
  - Pulls random questions from `question_bank.json`  
  - Interactive test interface with instant results  

-  **Dashboard**  
  - Overview of learning progress and available courses  

-  **UI/UX**  
  - Clean login/signup pages  
  - Centralized dashboard  
  - Gruvbox-material inspired dark mode color scheme  

---

##  Project Structure

```
.
├── assets/                  # Project-related assets (images, icons, etc.)
├── Data/
│   └── ChatLog.json         # Stores AI chat history
├── main.py                  # Core application logic
├── run.py                   # Entry point to run the server
├── requirements.txt         # Python dependencies
├── users.db                 # SQLite database (user data)
├── static/                  # Static files: CSS and JSON question bank
│   ├── color.css
│   ├── login.css
│   └── question_bank.json
├── style.css                # Main stylesheet
└── templates/               # Frontend HTML templates
    ├── course.html
    ├── dashboard.html
    ├── index.html           # Landing page
    ├── login.html
    ├── signup.html
    ├── test.html
    ├── notes.pdf            # Example PDF study note
    └── verify_otp.html
```

---

##  Installation & Setup

1. **Clone the repository**
   ```
   git clone https://github.com/epignosko/dhee.git
   cd dhee
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```
   python run.py
   ```

5. **Open in browser**  
   Navigate to: `http://127.0.0.1:5000`

---

##  Tech Stack

- **Backend:** Python (FastAPI)  
- **Database:** SQLite 
- **Frontend:** HTML, CSS, JavaScript  
- **AI/Logic:** Question generation, chat logging, and assistance  

---

##  Future Plans

- AI-powered tutor chatbot for personalized learning  
- Admin panel for creating and managing courses  
- Support for timed exams and leaderboards  
- Export results/reports in PDF or Excel  

---

##  Author

**Dhee** – built with love ❤️ to make learning interactive.  
Maintained by Syncergy (Gurmukh Singh, Rumani Sood, Jaspreet Singh, Sukhman Arora).  
