from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request: Request):
    """Returns the HTML content for the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
def read_login(request: Request):
    """Returns the HTML content for the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Returns the HTML content after a successful login"""
    # Print the username and password to the logs
    print(f"Username: {username}, Password: {password}")
    return templates.TemplateResponse("login_successful.html", {"request": request})

@router.get("/logout")
def read_logout(request: Request):
    """Returns the HTML content for the logout page"""
    return templates.TemplateResponse("logout.html", {"request": request})

@router.get("/create_account")
def read_create_account(request: Request):
    """Returns the HTML content for the create account page"""
    return templates.TemplateResponse("create_account.html", {"request": request})

@router.post("/create_account")
def post_create_account(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    """Returns the HTML content after a successful account creation"""
    return templates.TemplateResponse("account_created.html", {"request": request})

@router.get("/create_message")
def read_create_message(request: Request):
    """Returns the HTML content for the create message page"""
    return templates.TemplateResponse("create_message.html", {"request": request})

@router.post("/create_message")
def post_create_message(request: Request, message: str = Form(...)):
    """Returns the HTML content after a successful message creation"""
    return templates.TemplateResponse("message_posted.html", {"request": request})

@router.get("/search")
def read_search(request: Request):
    """Returns the HTML content for the search page"""
    return templates.TemplateResponse("search.html", {"request": request})

@router.post("/search")
def post_search(request: Request, query: str = Form(...)):
    """Returns the HTML content for the search results page"""
    return templates.TemplateResponse("search_results.html", {"request": request})
