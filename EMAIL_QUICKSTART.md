# Quick Start Commands for Email Notifications

## 🚀 Quick Setup (3 minutes)

### 1. Run Automated Setup
```powershell
.\setup_email.ps1
```
This will:
- Prompt for Gmail credentials
- Create .env file
- Install dependencies
- Update .gitignore

### 2. Start Backend
```powershell
cd backend
python -m uvicorn main:app --reload
```

### 3. Test Email Functionality
```powershell
cd backend
python test_email.py
```

---

## 📧 Email Notifications

### When emails are sent:
✅ Every time a violation is detected (auto or manual)  
✅ Includes professional penalty slip (HTML formatted)  
✅ Attaches violation image (if available)  
✅ Sent to: **23rahul54@gmail.com**

### What's included in the email:
- 🆔 Violation ID
- 🚗 Vehicle Number
- ⚠️ Violation Type (with confidence score)
- 💰 Fine Amount
- 📍 Location
- 📅 Date & Time
- 📸 Violation Image (attachment)

---

## 🧪 Testing

### Method 1: Live Detection
1. Start backend: `cd backend && python -m uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: http://localhost:5173
4. Go to Live Detection page
5. Trigger a violation (no helmet, phone usage, etc.)
6. Check email inbox

### Method 2: API Test (PowerShell)
```powershell
$body = @{
    vehicle_number = "TEST-1234"
    violation_type = "No Helmet Violation"
    location = "Test Road"
    fine_amount = 500
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/violations/" -Method POST -Body $body -ContentType "application/json"
```

### Method 3: Direct Test Script
```powershell
cd backend
python test_email.py
```

---

## 🔧 Configuration Files

### .env (backend/.env)
```env
SENDGRID_API_KEY=SG.your-api-key-here
SENDER_EMAIL=noreply@itms.gov
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=traffic_violation_db
```

### Change Recipient Email
Edit `backend/app/email_service.py` line 18:
```python
self.recipient_email = "new-email@example.com"
```

---

## ❌ Troubleshooting

### Email not sending?

**1. Check credentials**
```powershell
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'API Key Set: {bool(os.getenv(\"SENDGRID_API_KEY\"))}'); print(f'Sender: {os.getenv(\"SENDER_EMAIL\")}')"
```

**2. Verify SendGrid settings**
- ✅ API key starts with `SG.`
- ✅ API key has Mail Send permissions
- ✅ SendGrid account verified

**3. Check SendGrid dashboard**
- Go to: https://app.sendgrid.com/
- Check Activity Feed for delivery status

**4. Check backend logs**
Look for:
- `✅ Email sent successfully to 23rahul54@gmail.com`
- `⚠️ Failed to send email: [error]`

### Email in spam?
- Check spam folder
- Add sender to contacts
- Mark as "Not Spam"

---

## 📚 Documentation

- **Full Setup Guide**: [EMAIL_SETUP.md](EMAIL_SETUP.md)
- **Main README**: [README.md](README.md)
- **API Docs**: http://localhost:8000/docs (after starting backend)

---

## 🎯 Next Steps

1. ✅ Configure email (run `setup_email.ps1`)
2. ✅ Test email sending (`python backend/test_email.py`)
3. ✅ Start backend server
4. ✅ Trigger a violation
5. ✅ Check email at 23rahul54@gmail.com

**All done!** 🎉 Your system now sends automatic penalty slip emails for all violations.
