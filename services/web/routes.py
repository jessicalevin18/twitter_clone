import psycopg2
import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import Cookie

# Define the router before using it
router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("PG_HOST", "pg_normalized"),
        port=os.environ.get("PG_PORT", 5432),
        database=os.environ.get("PG_DB", "postgres"),  # default postgres db name
        user=os.environ.get("PG_USER", "postgres"),
        password=os.environ.get("PG_PASSWORD", "pass"),
    )

def check_credentials(username: str, password: str) -> str:
    """
    Checks if the provided username and password are valid.

    Args:
    - username (str): The username to check.
    - password (str): The password to check.

    Returns:
    - str: The username if the credentials are valid, otherwise None.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # ✅ Parameterized — safe from SQL injection
            cursor.execute(
                "SELECT username FROM credentials WHERE username = %s AND password = %s",
                (username, password)
            )
            row = cursor.fetchone()
            return row[0] if row else None
    finally:
        conn.close()


def logged_in_user(request: Request) -> str:
    """
    Checks if the user is logged in by checking the cookies.

    Args:
    - request (Request): The current request.

    Returns:
    - str: The username if the user is logged in, otherwise None.
    """
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username is not None and password is not None:
        valid_username = check_credentials(username, password)
        if valid_username is not None:
            return valid_username
    return None

def print_debug_info(request: Request):
    #print(f"--- DEBUG: {request.method} {request.url.path} ---")
    #print(f"Query params: {dict(request.query_params)}")
    print(f"Cookies: {dict(request.cookies)}")
    #print(f"Headers: {dict(request.headers)}")

@router.get("/")
async def read_root(request: Request):
    print_debug_info(request)
    """Returns the HTML content for the home page"""
    username = logged_in_user(request)

    page = int(request.query_params.get("page", 0))
    limit = 20
    offset = page * limit

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.screen_name, t.created_at, t.text
                FROM tweets t
                JOIN users u ON t.id_users = u.id_users
                ORDER BY t.created_at DESC, t.id_tweets DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            messages = cursor.fetchall()
    finally:
        conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,
        "messages": messages,
        "page": page,
    })

@router.get("/login")
def read_login(request: Request):
    print_debug_info(request)
    """Returns the HTML content for the login page"""
    username = logged_in_user(request)
    return templates.TemplateResponse("login.html", {"request": request, "username": username})

@router.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    print_debug_info(request)
    valid_username = check_credentials(username, password)
    if valid_username is not None:
        # ✅ Redirect to homepage after successful login
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie("username", username)
        response.set_cookie("password", password)
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "username": None,
            "error": "Invalid username or password"
        })
        

@router.get("/logout")
def read_logout(request: Request):
    print_debug_info(request)
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("username")
    response.delete_cookie("password")
    return response

@router.get("/create_account")
def read_create_account(request: Request):
    """Returns the HTML content for the create account page"""
    username = logged_in_user(request)
    return templates.TemplateResponse("create_account.html", {"request": request, "username": username})

@router.post("/create_account")
def post_create_account(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    # Check passwords match
    if password != confirm_password:
        return templates.TemplateResponse("create_account.html", {
            "request": request,
            "username": None,
            "error": "Passwords do not match"
        })

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if username already exists
            # ✅ Parameterized — safe from SQL injection
            cursor.execute(
                "SELECT username FROM credentials WHERE username = %s",
                (username,)
            )
            if cursor.fetchone() is not None:
                return templates.TemplateResponse("create_account.html", {
                    "request": request,
                    "username": None,
                    "error": f"Username '{username}' already exists"
                })

            # Insert new account
            # ✅ Parameterized — safe from SQL injection
            cursor.execute(
                "INSERT INTO credentials (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
    finally:
        conn.close()

    # Log them in automatically after account creation
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("username", username)
    response.set_cookie("password", password)
    return response

@router.get("/create_message")
def read_create_message(request: Request):
    """Returns the HTML content for the create message page"""
    username = logged_in_user(request)
    return templates.TemplateResponse("create_message.html", {"request": request, "username": username})

@router.post("/create_message")
def post_create_message(request: Request, message: str = Form(...)):
    """Returns the HTML content after a successful message creation"""
    username = logged_in_user(request)
    return templates.TemplateResponse("message_posted.html", {"request": request, "username": username})

@router.get("/search")
def read_search(request: Request):
    """Returns the HTML content for the search page"""
    username = logged_in_user(request)
    return templates.TemplateResponse("search.html", {"request": request, "username": username})

@router.post("/search")
def post_search(request: Request, query: str = Form(...)):
    """Returns the HTML content for the search results page"""
    username = logged_in_user(request)
    return templates.TemplateResponse("search_results.html", {"request": request, "username": username})
