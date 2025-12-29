# ITMS Authentication System Setup

## Overview
This project now includes JWT-based authentication with login/logout functionality. The home page is public and full-screen, while the admin dashboard is protected and requires login.

## Architecture

### Flow:
1. **Unauthenticated Users**: See full-screen Home page and Login page
2. **Authenticated Users**: Access admin dashboard with sidebar/navbar

### Pages:
- `/` - Public Home page (full-screen, no sidebar)
- `/login` - Login page (full-screen, no sidebar)
- `/dashboard`, `/live`, `/violations`, etc. - Protected admin pages (with sidebar/navbar)

## Backend Setup

### 1. Install Required Dependencies

```powershell
cd backend
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 bcrypt==4.0.1
```

Or install all requirements:
```powershell
pip install -r requirements.txt
```

### 2. Start the Backend Server

```powershell
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### 3. Create Admin User

Make a POST request to create the initial admin user:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/create-admin" -Method Post
```

Or use the setup script:
```powershell
.\setup_auth.ps1
```

This creates:
- **Email**: `admin@traffic.com`
- **Password**: `admin123`
- **Role**: `admin`

⚠️ **Change the password after first login!**

### 4. API Documentation

Visit the Swagger UI to see all auth endpoints:
- http://127.0.0.1:8000/docs

## Frontend Setup

### 1. Install Dependencies

```powershell
cd frontend
npm install
```

### 2. Start the Development Server

```powershell
npm run dev
```

The frontend will start at `http://localhost:5173`

## Features Implemented

### Backend:
- ✅ JWT token generation and validation
- ✅ Password hashing with bcrypt
- ✅ User registration endpoint
- ✅ Login endpoint with email/password
- ✅ Get current user endpoint
- ✅ Logout endpoint
- ✅ MongoDB user collection
- ✅ Token expiration (24 hours)

### Frontend:
- ✅ AuthContext for global authentication state
- ✅ Full-screen public Home page
- ✅ Professional Login page with form validation
- ✅ Protected routes for admin dashboard
- ✅ Automatic token storage in localStorage
- ✅ Logout functionality
- ✅ User profile display in navbar
- ✅ Loading states and error handling

## API Endpoints

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "officer"
}
```

#### POST `/api/auth/login`
Login with credentials
```json
{
  "email": "admin@traffic.com",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### GET `/api/auth/me`
Get current user info (requires authentication)
```bash
Authorization: Bearer <token>
```

#### POST `/api/auth/logout`
Logout (requires authentication)

#### POST `/api/auth/create-admin`
Create initial admin user (use once and disable in production)

## Usage

### For Users:

1. **Visit the Home Page**: Navigate to `http://localhost:5173`
2. **Click Login**: Click the "Login" button in the navigation
3. **Enter Credentials**:
   - Email: `admin@traffic.com`
   - Password: `admin123`
4. **Access Dashboard**: After successful login, you'll be redirected to the admin dashboard

### For Developers:

#### Using the Auth Context:
```jsx
import { useAuth } from '../context/AuthContext'

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth()
  
  if (!isAuthenticated) {
    return <div>Please login</div>
  }
  
  return (
    <div>
      <p>Welcome {user.full_name}</p>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

#### Making Authenticated API Calls:
```jsx
const { token } = useAuth()

const response = await fetch('http://127.0.0.1:8000/api/violations', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

## Security Notes

1. **Secret Key**: Change the `SECRET_KEY` in production (use environment variable)
2. **HTTPS**: Use HTTPS in production
3. **Token Expiration**: Tokens expire after 24 hours
4. **Password Policy**: Implement strong password requirements
5. **Rate Limiting**: Add rate limiting to login endpoint
6. **Disable Create Admin**: Remove or protect the `/create-admin` endpoint in production

## MongoDB Collections

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "admin@traffic.com",
  "full_name": "System Administrator",
  "role": "admin",
  "is_active": true,
  "hashed_password": "$2b$12$...",
  "created_at": ISODate
}
```

## Troubleshooting

### Backend Issues:

**Error: Module not found 'jose'**
```powershell
pip install python-jose[cryptography]
```

**Error: Module not found 'passlib'**
```powershell
pip install passlib[bcrypt]
```

### Frontend Issues:

**Error: Cannot read property 'user' of undefined**
- Make sure components are wrapped in `<AuthProvider>`

**Login not redirecting**
- Check if backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in backend

## Next Steps

1. ✅ Add password reset functionality
2. ✅ Add email verification
3. ✅ Add role-based permissions
4. ✅ Add refresh tokens
5. ✅ Add session management
6. ✅ Add audit logging

## License
MIT
