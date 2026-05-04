#!/bin/bash

# Test login with valid credentials
echo "Testing login with valid credentials"
response=$(curl -X POST -F 'username=Trump' -F 'password=12345' http://localhost:8000/login)
if echo "$response" | grep -q "Login successful"; then
    echo "Login with valid credentials: SUCCESS"
else
    echo "Login with valid credentials: FAILURE"
fi

# Test login with invalid credentials
echo "Testing login with invalid credentials"
response=$(curl -X POST -F 'username=Wrong' -F 'password=wrong' http://localhost:8000/login)
if echo "$response" | grep -q "Invalid username or password"; then
    echo "Login with invalid credentials: SUCCESS"
else
    echo "Login with invalid credentials: FAILURE"
fi

# Test cookies are set after login
echo "Testing cookies are set after login"
response=$(curl -X POST -F 'username=Trump' -F 'password=12345' http://localhost:8000/login)
cookies=$(echo "$response" | grep -oP '(?<=Set-Cookie: )[^;]+')
if [ -n "$cookies" ]; then
    echo "Cookies are set after login: SUCCESS"
else
    echo "Cookies are set after login: FAILURE"
fi

# Test logout
echo "Testing logout"
response=$(curl -X GET http://localhost:8000/logout)
if echo "$response" | grep -q "You are logged out"; then
    echo "Logout: SUCCESS"
else
    echo "Logout: FAILURE"
fi

# Test cookies are deleted after logout
echo "Testing cookies are deleted after logout"
response=$(curl -X GET http://localhost:8000/logout)
cookies=$(echo "$response" | grep -oP '(?<=Set-Cookie: )[^;]+')
if [ -z "$cookies" ] || (echo "$cookies" | grep -q "Expires=0"); then
    echo "Cookies are deleted after logout: SUCCESS"
else
    echo "Cookies are deleted after logout: FAILURE"
fi
