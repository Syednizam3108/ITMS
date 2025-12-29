# 🚀 START HERE - Run Your ITMS Application

## Prerequisites Check
- ✅ Python 3.10+ installed
- ✅ Node.js installed
- ✅ MongoDB running (local or Atlas)
- ✅ All dependencies installed in backend (pip install -r requirements.txt)
- ✅ All dependencies installed in frontend (npm install)

## Step-by-Step Instructions

### 1️⃣ Start Backend (Terminal 1)

Open PowerShell in project root:

```powershell
cd backend
uvicorn main:app --reload
```

✅ **Success**: You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

🌐 **Test**: Open http://127.0.0.1:8000/docs in browser

---

### 2️⃣ Create Admin User (Terminal 1 or 2)

**IMPORTANT**: Do this only ONCE, after backend is running

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/create-admin" -Method Post
```

✅ **Success**: You should see:
```json
{
  "message": "Admin user created successfully",
  "email": "admin@traffic.com",
  "password": "admin123"
}
```

⚠️ **If you get an error**: Backend might not be running or admin already exists

---

### 3️⃣ Start Frontend (Terminal 2)

Open a NEW PowerShell terminal:

```powershell
cd frontend
npm run dev
```

✅ **Success**: You should see:
```
  VITE ready in XXX ms
  ➜  Local:   http://localhost:5173/
```

---

### 4️⃣ Open Application

🌐 Open your browser to: **http://localhost:5173**

You should see the **full-screen Home page** with:
- ITMS header
- "Get Started" buttons
- Feature cards
- No sidebar (public page)

---

### 5️⃣ Login

1. Click the **"Login"** button in the top-right corner
2. You'll see the login page
3. Enter credentials:
   - **Email**: `admin@traffic.com`
   - **Password**: `admin123`
4. Click **"Sign In"**

✅ **Success**: You'll be redirected to `/dashboard` with sidebar and navbar visible

---

## 🎯 What You Should See

### Before Login:
- ✅ Home page at `/` (full-screen, no sidebar)
- ✅ Login page at `/login` (full-screen, no sidebar)

### After Login:
- ✅ Dashboard at `/dashboard` (with sidebar + navbar)
- ✅ Your name in top-right corner
- ✅ Logout button
- ✅ Can navigate to Live Feed, Violations, Analytics, etc.

---

## 🔍 Verify Everything Works

### Test Checklist:

**Backend:**
- [ ] Backend running at http://127.0.0.1:8000
- [ ] Can see Swagger docs at http://127.0.0.1:8000/docs
- [ ] Admin user created successfully

**Frontend:**
- [ ] Home page loads (public, no sidebar)
- [ ] Can click Login button
- [ ] Login page loads
- [ ] Can submit login form
- [ ] After login, see dashboard with sidebar
- [ ] Can see user info in navbar
- [ ] Can click Logout and return to home

---

## 🐛 Common Issues & Solutions

### Issue: "Unable to connect to the remote server"
**Solution**: Backend is not running. Start it with: `uvicorn main:app --reload`

### Issue: "Admin user already exists"
**Solution**: That's fine! It means you already created it. Just login.

### Issue: Login form shows error
**Solution**: 
1. Check backend is running
2. Check you created the admin user
3. Check credentials are correct

### Issue: After login, I see a blank page
**Solution**: 
1. Check browser console for errors
2. Clear browser cache and localStorage
3. Restart frontend dev server

### Issue: MongoDB connection error
**Solution**: Make sure MongoDB is running (local or Atlas connection string in .env)

---

## 📱 Demo Credentials

**Email**: `admin@traffic.com`  
**Password**: `admin123`

⚠️ **Security Note**: Change this password in production!

---

## 🎉 You're All Set!

If you've followed all steps and everything works:
- ✅ You have a working authentication system
- ✅ Public home page is accessible
- ✅ Protected admin dashboard requires login
- ✅ JWT tokens are working
- ✅ You can logout and login again

**Enjoy your Intelligent Traffic Management System!** 🚦

---

## 📚 Additional Resources

- **Full Documentation**: See `AUTHENTICATION_SETUP.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **API Docs**: http://127.0.0.1:8000/docs

## 💡 Need Help?

If something doesn't work:
1. Check all terminals for error messages
2. Make sure MongoDB is running
3. Clear browser cache and localStorage
4. Restart both backend and frontend
5. Check the troubleshooting section in AUTHENTICATION_SETUP.md
