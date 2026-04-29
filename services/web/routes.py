from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Form

router = APIRouter()

@router.get("/")
def read_root(request: Request):
  html_content = """
  <html>
      <head>
          <title>Home</title>
      </head>
      <body>
          <h1>Welcome to the home page</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.get("/login")
def read_login(request: Request):
  html_content = """
  <html>
      <head>
          <title>Login</title>
      </head>
      <body>
          <h1>Login page</h1>
          <form action="/login" method="post">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username" required><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password" required><br>
              <input type="submit" value="Submit">
          </form>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
  html_content = """
  <html>
      <head>
          <title>Login successful</title>
      </head>
      <body>
          <h1>Login successful</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.get("/logout")
def read_logout(request: Request):
  html_content = """
  <html>
      <head>
          <title>Logout</title>
      </head>
      <body>
          <h1>You are logged out</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.get("/create_account")
def read_create_account(request: Request):
  html_content = """
  <html>
      <head>
          <title>Create account</title>
      </head>
      <body>
          <h1>Create account page</h1>
          <form action="/create_account" method="post">
              <label for="username">Username:</label><br>
              <input type="text" id="username" name="username" required><br>
              <label for="password">Password:</label><br>
              <input type="password" id="password" name="password" required><br>
              <label for="confirm_password">Confirm password:</label><br>
              <input type="password" id="confirm_password" name="confirm_password" required><br>
              <input type="submit" value="Submit">
          </form>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.post("/create_account")
def post_create_account(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
  html_content = """
  <html>
      <head>
          <title>Account created</title>
      </head>
      <body>
          <h1>Your account has been created</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.get("/create_message")
def read_create_message(request: Request):
  html_content = """
  <html>
      <head>
          <title>Create message</title>
      </head>
      <body>
          <h1>Create message page</h1>
          <form action="/create_message" method="post">
              <label for="message">Message:</label><br>
              <input type="text" id="message" name="message" required><br>
              <input type="submit" value="Submit">
          </form>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.post("/create_message")
def post_create_message(request: Request, message: str = Form(...)):
  html_content = """
  <html>
      <head>
          <title>Message posted</title>
      </head>
      <body>
          <h1>Your message has been posted</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.get("/search")
def read_search(request: Request):
  html_content = """
  <html>
      <head>
          <title>Search</title>
      </head>
      <body>
          <h1>Search page</h1>
          <form action="/search" method="post">
              <label for="query">Query:</label><br>
              <input type="text" id="query" name="query" required><br>
              <input type="submit" value="Submit">
          </form>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)

@router.post("/search")
def post_search(request: Request, query: str = Form(...)):
  html_content = """
  <html>
      <head>
          <title>Search results</title>
      </head>
      <body>
          <h1>Search results for your query</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)
