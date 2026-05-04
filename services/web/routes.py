# existing code...
@router.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Returns the HTML content after a login attempt"""
    # Print the username and password to the logs
    print(f"Username: {username}, Password: {password}")
    # Check the credentials
    valid_username = check_credentials(username, password)
    if valid_username is not None:
        # Credentials are valid, set cookies and return the success page
        response = templates.TemplateResponse("login_successful.html", {"request": request, "username": valid_username})
        response.set_cookie("username", username)
        response.set_cookie("password", password)
        return response
    else:
        # Credentials are invalid, return an error page
        return templates.TemplateResponse("login.html", {"request": request, "username": None, "error": "Invalid username or password"})
