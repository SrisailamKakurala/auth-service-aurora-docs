Great! Let's test all the authentication APIs using Thunder Client. I'll provide you with the complete test cases for each endpoint.

## API Testing Guide for Thunder Client

### 1. **Health Check** (GET)
**URL:** `http://127.0.0.1:8000/health`
**Method:** GET
**Expected Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. **User Registration** (POST)
**URL:** `http://127.0.0.1:8000/auth/register`
**Method:** POST
**Headers:**
```
Content-Type: application/json
```
**Body (JSON):**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpassword123"
}
```
**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 3. **User Login** (POST)
**URL:** `http://127.0.0.1:8000/auth/login`
**Method:** POST
**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```
**Body (Form Data):**
```
username=testuser
password=testpassword123
```
**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 4. **Get Current User** (GET) - Protected Route
**URL:** `http://127.0.0.1:8000/auth/me`
**Method:** GET
**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```
**Expected Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "testuser",
  "email": "test@example.com"
}
```

---

### 5. **Logout** (POST) - Protected Route
**URL:** `http://127.0.0.1:8000/auth/logout`
**Method:** POST
**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```
**Expected Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

## Step-by-Step Testing Process:

### Step 1: Start Your Server
```bash
uvicorn app.main:app --reload
```

### Step 2: Test Health Check
- Create a new request in Thunder Client
- Set method to GET
- URL: `http://127.0.0.1:8000/health`
- Send request

### Step 3: Test Registration
- Create new request, method POST
- URL: `http://127.0.0.1:8000/auth/register`
- Set Content-Type header to `application/json`
- Add JSON body with user details
- **Save the access_token from response!**

### Step 4: Test Login
- Create new request, method POST
- URL: `http://127.0.0.1:8000/auth/login`
- Set Content-Type header to `application/x-www-form-urlencoded`
- Add form data (username, password)
- **Save the access_token from response!**

### Step 5: Test Protected Routes
- For `/auth/me` and `/auth/logout`:
- Add Authorization header: `Bearer YOUR_TOKEN`
- Replace `YOUR_TOKEN` with the actual token from login/register

## Common Error Responses:

### Registration Errors:
```json
{
  "detail": "Username or email already registered"
}
```

### Login Errors:
```json
{
  "detail": "Incorrect username or password"
}
```

### Authorization Errors:
```json
{
  "detail": "Invalid or expired token"
}
```

## Thunder Client Tips:

1. **Save Environment Variables**: Create an environment variable for your token
   - Name: `auth_token`
   - Value: Your actual token
   - Use: `{{auth_token}}` in Authorization header

2. **Create a Collection**: Group all auth requests in one collection

3. **Test Flow**: Register → Login → Get User Info → Logout

Let me know what responses you get for each endpoint, and I'll help troubleshoot any issues!