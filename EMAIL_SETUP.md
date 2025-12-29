# Email Notification Setup Guide

## Overview
The system now sends automated email notifications with penalty slips to **23rahul54@gmail.com** whenever a traffic violation is detected.

## Features
✅ Automatic email on violation detection  
✅ Professional penalty slip with HTML formatting  
✅ Violation image attachment  
✅ Complete violation details (Vehicle, Type, Fine, Location, Timestamp)  
✅ Works for both auto-detected and manually created violations

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install python-dotenv
```

### 2. Get SendGrid API Key

#### Sign up for SendGrid (Free Tier):
1. Go to https://sendgrid.com/free/
2. Sign up for a free account (100 emails/day forever)
3. Verify your email address

#### Generate API Key:
1. Log in to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Name: "ITMS Backend"
5. Permissions: Select **Full Access** or **Restricted Access** with **Mail Send** enabled
6. Click **Create & View**
7. Copy the API key (starts with `SG.` - you can only see it once!)

### 3. Create .env File

Create a `.env` file in the `backend/` directory:

```bash
cd backend
notepad .env
```

Add the following content (replace with your actual credentials):

```env
# Email Configuration
SENDGRID_API_KEY=SG.your-api-key-here
SENDER_EMAIL=noreply@itms.gov

# MongoDB Configuration (if not already set)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=traffic_violation_db
```

**Important:** 
- The API key starts with `SG.` and is around 69 characters long
- Keep this file secure and never commit it to Git
- You can only see the API key once when creating it

### 4. Update .gitignore

Add to your `.gitignore` file:
```
backend/.env
.env
```

### 5. Restart the Backend Server

```bash
cd backend
python -m uvicorn main:app --reload
```

## Testing the Email Functionality

### Test 1: Auto-Detection (Live Camera)
1. Start the backend server
2. Open the frontend application
3. Go to the live detection page
4. Allow camera access
5. Trigger a violation (no helmet, phone usage, etc.)
6. Check email at **23rahul54@gmail.com**

### Test 2: Manual Violation Creation
```bash
# Using PowerShell
$body = @{
    vehicle_number = "TEST-1234"
    violation_type = "No Helmet Violation"
    location = "Test Location"
    fine_amount = 500
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/violations/" -Method POST -Body $body -ContentType "application/json"
```

### Test 3: API Testing (Postman/Thunder Client)
```
POST http://localhost:8000/violations/
Content-Type: application/json

{
    "vehicle_number": "TEST-5678",
    "violation_type": "Phone Usage While Riding",
    "location": "Main Road, Junction 5",
    "fine_amount": 1000
}
```

## Email Content Preview

The penalty slip email includes:

```
🚨 TRAFFIC VIOLATION PENALTY SLIP
Intelligent Traffic Management System

Violation ID: 507f1f77bcf86cd799439011
Vehicle Number: DL-01-AB-1234
Date & Time: December 16, 2025 at 02:30 PM
Location: Live Camera Feed

⚠️ No Helmet Violation (Confidence: 87%)

PENALTY AMOUNT
₹500.00

⚠️ Important Notice:
This violation has been automatically detected and recorded by our 
AI-powered traffic management system. Please pay the fine within 
15 days to avoid additional penalties.
```

## Troubleshooting

### Issue: Email Not Sending

**Check 1: Verify Credentials**
```python
# Test in Python console
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("SENDGRID_API_KEY"))
print(os.getenv("SENDER_EMAIL"))
```

**Check 2: SendGrid Settings**
- Ensure API key has **Mail Send** permissions
- Verify your SendGrid account is verified
- Check API key is correct (starts with `SG.`)
- API key should be around 69 characters long

**Check 3: Backend Logs**
Look for these messages in the console:
- ✅ `Email sent successfully to 23rahul54@gmail.com`
- ⚠️ `Failed to send email: [error message]`
- ⚠️ `SendGrid API key not configured`

**Check 4: SendGrid Dashboard**
- Go to https://app.sendgrid.com/
- Check **Activity Feed** for email delivery status
- Verify daily quota (100 emails/day on free tier)

### Issue: Wrong Email Address

To change the recipient email, edit `backend/app/email_service.py`:
```python
self.recipient_email = "new-email@example.com"  # Line 18
```

### Issue: Email Goes to Spam

1. Check Gmail spam folder
2. Mark the email as "Not Spam"
3. Add sender to contacts
4. Consider using a verified domain email instead of personal Gmail

## Customization

### Change Fine Amounts
Edit `backend/app/routers/detection.py`:
```python
def get_fine_amount(violation_type: str) -> float:
    fine_map = {
        "No Helmet Violation": 500.0,
        "Phone Usage While Riding": 1000.0,
        "Triple Riding Violation": 1500.0
    }
    return fine_map.get(violation_type, 0.0)
```

### Customize Email Template
Edit `backend/app/email_service.py` → `_create_penalty_slip_html()` method

### Add Multiple Recipients
Edit `backend/app/email_service.py`:
```python
self.recipient_emails = [
    "23rahul54@gmail.com",
    "officer1@example.com",
    "admin@example.com"
]
```

Then in `send_violation_email()`:
```python
message["To"] = ", ".join(self.recipient_emails)
```

## Security Best Practices

1. ✅ **Never commit .env file to Git**
2. ✅ **Use app passwords, not actual Gmail password**
3. ✅ **Rotate passwords periodically**
4. ✅ **Use environment-specific configurations for production**
5. ✅ **Consider using dedicated email service (SendGrid, AWS SES) for production**

## Production Considerations

For production deployment, consider:

1. **Use a dedicated email service:**
   - SendGrid
   - AWS SES
   - Mailgun
   - Postmark

2. **Add email queue:**
   - Redis + Celery
   - RabbitMQ
   - AWS SQS

3. **Implement retry logic:**
   - Exponential backoff
   - Dead letter queue

4. **Add email templates:**
   - Use Jinja2 templates
   - Support multiple languages
   - Responsive design

5. **Monitor email delivery:**
   - Track delivery rates
   - Monitor bounces
   - Handle unsubscribes

## Support

If you encounter any issues:
1. Check the backend console logs
2. Verify .env file configuration
3. Test Gmail credentials separately
4. Review the troubleshooting section above

For additional help, check the project documentation or contact the development team.
