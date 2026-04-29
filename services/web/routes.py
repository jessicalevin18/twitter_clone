from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi import Form

router = APIRouter()

@router.get("/")
def read_root(request: Request):
  return {"Hello": "World"}

@router.get("/login")
def read_login(request: Request):
  return {"message": "Please enter your username and password"}

@router.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
  return {"message": "You are logged in"}

@router.get("/logout")
def read_logout(request: Request):
  return {"message": "You are logged out"}

@router.get("/create_account")
def read_create_account(request: Request):
  return {"message": "Please enter your username and password to create an account"}

@router.post("/create_account")
def post_create_account(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
  return {"message": "Your account has been created"}

@router.get("/create_message")
def read_create_message(request: Request):
  return {"message": "Please enter your message"}

@router.post("/create_message")
def post_create_message(request: Request, message: str = Form(...)):
  return {"message": "Your message has been posted"}

@router.get("/search")
def read_search(request: Request):
  return {"message": "Please enter your search query"}

@router.post("/search")
def post_search(request: Request, query: str = Form(...)):
  return {"message": "Search results for your query"}

@router.get("/create_message")
def read_create_message(request: Request):
  return {"message": "Please enter your message"}
