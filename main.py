import uvicorn
from fastapi import FastAPI, HTTPException , WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
from random import randint
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import bcrypt
from typing import Optional

app = FastAPI(title="Dhee - The learning platform")

current_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

def read_chatLogjson():
    with open(rf"{current_dir}/Data/ChatLog.json", "r", encoding="utf-8") as fl:
        return json.load(fl)

# Add this line to enable sessions
app.add_middleware(
    SessionMiddleware,
    secret_key="&[{}(=*)]!#",  # keep this secret!
    max_age=14 * 24 * 60 * 60,                         # optional: cookie lifetime in seconds (here 14 days)
    https_only=False,                                   # optional: require HTTPS for cookie
)
conf = ConnectionConfig(
    MAIL_USERNAME="abc20.d.25@gmail.com",
    MAIL_PASSWORD="rqxi nisg pfjw foda ",
    MAIL_FROM="abc20.d.25@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)
fast_mail = FastMail(conf)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

otp_store = {}

def generate_otp() -> str:
    """Generate a 4-digit numeric OTP as string."""
    return f"{randint(1000, 9999)}"

def store_otp(email: str, hashed_password: str, user_type: str = "default") -> str:
    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=5)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO otps (email, otp, expiry, hashed_password, user_type)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE 
          SET otp=excluded.otp, expiry=excluded.expiry
    ''', (email, otp, expiry, hashed_password, user_type))
    conn.commit()
    conn.close()
    return otp

def validate_otp(email: str, user_otp: str) -> Optional[dict]:
    """
    Returns a dict with 'hashed_password' and 'user_type' if OTP is valid,
    otherwise returns None.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT otp, expiry, hashed_password, user_type FROM otps WHERE email = ?', (email,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    otp, expiry_str, hashed_password, user_type = row
    expiry = datetime.fromisoformat(expiry_str)
    if datetime.now() > expiry:
        cursor.execute('DELETE FROM otps WHERE email = ?', (email,))
        conn.commit()
        conn.close()
        return None

    if otp != user_otp:
        conn.close()
        return None

    # OTP is correct and not expired → delete and return stored data
    cursor.execute('DELETE FROM otps WHERE email = ?', (email,))
    conn.commit()
    conn.close()
    return {
        "hashed_password": hashed_password,
        "user_type": user_type
    }

def create_user_with_hash(email: str, password_hash: str, user_type: Optional[str] = None) -> bool:
    """
    Insert a new user row using an already-hashed password.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password_hash) VALUES (?, ?)',
            (email, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Templates
templates = Jinja2Templates(directory="templates")

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otps (
            email TEXT PRIMARY KEY,
            otp TEXT NOT NULL,
            expiry TIMESTAMP NOT NULL,
            hashed_password TEXT NOT NULL,
            user_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    # Add custom salt (single #) to the end of password before hashing
    salted_password = password + "#"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(salted_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    # Add the same custom salt (single #) before verification
    salted_password = password + "#"
    return bcrypt.checkpw(salted_password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_by_email(email: str) -> Optional[dict]:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'id': user[0],
            'email': user[1],
            'password_hash': user[2]
        }
    return None

def create_user(email: str, password: str) -> bool:
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def home(request: Request):
    cources = read_chatLogjson()

    data = []

    for cource in cources:
        # suppose each course is a dict with "courseName"
        course_data = {
            "courseName": cource.get("courseName", "Unnamed Course"),
            "description":cource.get("description"),
            "duration":cource.get("duration")
        }
        print(course_data)
        data.append(course_data)

    # Pass context dictionary including request
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "data": data}
    )
# Routes
@app.get("/notes")
async def serve_pdf():
    file_path = "templates/notes.pdf"  # Replace with the actual path to notes.pdf
    return FileResponse(path=file_path, media_type="application/pdf", filename="notes.pdf")

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/course", response_class=HTMLResponse)
async def course_page(request: Request):
    return templates.TemplateResponse("course.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)

    if not user or not verify_password(password, user['password_hash']):
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid email or password"
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user,
        "success": f"Welcome back, {user['email']}!"
    })

@app.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if password != confirm_password:
        errors.append("Passwords do not match")

    if '@' not in email or '.' not in email:
        errors.append("Please enter a valid email address")

    if errors:
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "errors": errors,
            "email": email
        })

    if get_user_by_email(email):
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "errors": ["An account with this email already exists"],
            "email": email
        })

    # Instead of creating user immediately, generate OTP and send email
    hashed_password = hash_password(password)
    otp = store_otp(email, hashed_password)

    # Send OTP email
    message = MessageSchema(
        subject="Your Registration Verification Code",
        recipients=[email],
        body=f"""
            <h1>Registration Verification Code</h1>
            <p>Your 4-digit verification code is: <strong>{otp}</strong></p>
            <p>This code will expire in 5 minutes.</p>
        """,
        subtype="html",
    )

    try:
        await fast_mail.send_message(message)
        # Save email in session for verification step (using cookies/session middleware if set up)
        request.session['pending_verification_email'] = email

        # Redirect to OTP verification page
        return RedirectResponse(url="/verify-otp", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print("Failed to send OTP email:", e)
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "errors": ["Failed to send verification email"],
            "email": email
        })

@app.get("/verify-otp", response_class=HTMLResponse)
async def verify_otp_page(request: Request):
    return templates.TemplateResponse("verify_otp.html", {"request": request})

@app.post("/verify-otp")
async def verify_otp_submit(request: Request, otp: str = Form(...)):
    email = request.session.get("pending_verification_email")
    if not email:
        return RedirectResponse(url="/signup", status_code=status.HTTP_303_SEE_OTHER)

    # Validate OTP and simultaneously fetch hashed_password & user_type
    result = validate_otp(email, otp)
    if result is None:
        return templates.TemplateResponse("verify_otp.html", {
            "request": request,
            "error": "Invalid or expired OTP. Please try again."
        })

    # Now create the user using the stored hash
    created = create_user_with_hash(
        email,
        result["hashed_password"],
        user_type=result.get("user_type")
    )

    # Clean up session
    request.session.pop("pending_verification_email", None)

    if created:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "success": "Your account has been verified and created. Please log in."
        })
    else:
        return templates.TemplateResponse("verify_otp.html", {
            "request": request,
            "error": "Failed to create account, maybe it already exists."
        })

@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
