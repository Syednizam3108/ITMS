# SendGrid Setup Guide for ITMS

## Why SendGrid?

✅ **Free Tier**: 100 emails/day forever  
✅ **Reliable**: 99%+ delivery rate  
✅ **No Gmail restrictions**: No 2FA or app passwords needed  
✅ **Professional**: Better than personal Gmail  
✅ **Scalable**: Upgrade to 40K emails/month for $15  
✅ **Analytics**: Track opens, clicks, bounces

---

## Step-by-Step Setup

### 1. Create SendGrid Account (2 minutes)

1. Go to: https://sendgrid.com/free/
2. Click **"Start for Free"**
3. Fill in:
   - Email address
   - Password
   - Company name (can be "Personal" or "ITMS Project")
4. Verify your email
5. Complete account setup

**Free Plan includes:**
- 100 emails/day (forever free)
- No credit card required
- Full API access
- Email analytics

### 2. Create API Key (1 minute)

1. Log in to SendGrid dashboard: https://app.sendgrid.com/
2. Go to **Settings** → **API Keys** (left sidebar)
3. Click **"Create API Key"** button
4. Configure:
   - **API Key Name**: `ITMS Backend`
   - **API Key Permissions**: Select **Full Access** (easiest)
     - Or **Restricted Access** → Check **Mail Send** only
5. Click **"Create & View"**
6. **IMPORTANT**: Copy the API key NOW (you can only see it once!)
   - It starts with `SG.`
   - It's about 69 characters long
   - Example: `SG.aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890...`

### 3. Configure ITMS Backend

**Option A: Automated Setup**
```powershell
.\setup_email.ps1
```
Paste your SendGrid API key when prompted.

**Option B: Manual Setup**

Create `backend/.env` file:
```env
SENDGRID_API_KEY=SG.your-actual-api-key-here
SENDER_EMAIL=noreply@itms.gov
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=traffic_violation_db
```

### 4. Test Email (30 seconds)

```powershell
cd backend
python test_email.py
```

You should see:
```
✅ SUCCESS! Test email sent successfully!
Check inbox at: 23rahul54@gmail.com
```

---

## Sender Email Configuration

### Default Sender
The default sender is `noreply@itms.gov` - this works fine for testing.

### Using Custom Domain (Optional)
To use your own domain (e.g., `notifications@yourdomain.com`):

1. **Verify Domain in SendGrid:**
   - Go to **Settings** → **Sender Authentication**
   - Click **Authenticate Your Domain**
   - Follow DNS setup instructions

2. **Update .env:**
   ```env
   SENDER_EMAIL=notifications@yourdomain.com
   ```

### Single Sender Verification (Quick Alternative)
If you don't have a custom domain:

1. Go to **Settings** → **Sender Authentication**
2. Click **Verify a Single Sender**
3. Fill in details:
   - From Name: ITMS System
   - From Email: your-verified-email@gmail.com
   - Reply To: Same as above
4. Verify the email sent to you
5. Update .env:
   ```env
   SENDER_EMAIL=your-verified-email@gmail.com
   ```

---

## Monitoring & Analytics

### Check Email Delivery

1. Go to SendGrid Dashboard: https://app.sendgrid.com/
2. Click **Activity** in left sidebar
3. See real-time email delivery status:
   - ✅ Delivered
   - 📧 Processed
   - ⚠️ Bounced
   - 🚫 Blocked

### Daily Stats
- **Dashboard** → View email volume
- Track opens, clicks, bounces
- Monitor your free tier quota (100/day)

---

## Troubleshooting

### Issue: "401 Unauthorized"
**Cause:** Invalid API key

**Solution:**
1. Check API key starts with `SG.`
2. Verify no extra spaces in .env file
3. Create new API key if needed

### Issue: "403 Forbidden"
**Cause:** API key doesn't have Mail Send permission

**Solution:**
1. Go to **Settings** → **API Keys**
2. Delete old key
3. Create new key with **Full Access** or **Mail Send** permission

### Issue: Email not received
**Check:**
1. SendGrid Activity Feed (Dashboard → Activity)
2. Spam folder at 23rahul54@gmail.com
3. Sender email verification status
4. Daily quota (100 emails/day max on free tier)

### Issue: "API key not configured"
**Solution:**
```powershell
# Check .env file exists and has correct key
cd backend
cat .env
# Should show: SENDGRID_API_KEY=SG.xxxxx
```

---

## Upgrading SendGrid Plan

### When to Upgrade?
- Sending more than 100 emails/day
- Need priority support
- Want advanced analytics

### Plans:
- **Free**: 100 emails/day forever
- **Essentials**: $19.95/month → 50K emails/month
- **Pro**: $89.95/month → 1.5M emails/month

Upgrade at: https://app.sendgrid.com/settings/billing

---

## Security Best Practices

✅ **Never commit .env file to Git**  
✅ **Rotate API keys every 3-6 months**  
✅ **Use Restricted Access (Mail Send only) in production**  
✅ **Monitor Activity Feed for suspicious activity**  
✅ **Keep SendGrid account password secure**

---

## Production Recommendations

### 1. Verify Domain
- Improves deliverability
- Reduces spam score
- Professional sender address

### 2. Set Up DKIM/SPF
- Automatic with domain verification
- Increases email trust score

### 3. Enable Event Webhooks
- Get real-time delivery notifications
- Track bounces and complaints
- Improve email lists

### 4. Use IP Pools (Paid plans)
- Dedicated IP address
- Better reputation control

---

## Comparison: SendGrid vs Gmail

| Feature | SendGrid Free | Gmail SMTP |
|---------|--------------|------------|
| Daily Limit | 100 emails | 100-500 emails |
| Setup Complexity | ⭐⭐ Easy | ⭐⭐⭐ Complex |
| 2FA Required | ❌ No | ✅ Yes |
| App Password | ❌ No | ✅ Required |
| Deliverability | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| Analytics | ✅ Full | ❌ None |
| Professional | ✅ Yes | ❌ No |
| Scalability | ⭐⭐⭐⭐⭐ Easy | ⭐⭐ Limited |

---

## Support Resources

- **SendGrid Docs**: https://docs.sendgrid.com/
- **API Reference**: https://docs.sendgrid.com/api-reference/
- **Status Page**: https://status.sendgrid.com/
- **Support**: https://support.sendgrid.com/

---

## Quick Commands

```powershell
# Setup
.\setup_email.ps1

# Test
cd backend
python test_email.py

# Check config
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key:', os.getenv('SENDGRID_API_KEY')[:10] + '...')"

# Start backend
python -m uvicorn main:app --reload
```

---

**You're all set!** 🎉 

SendGrid will now handle all your ITMS violation notification emails with 99%+ delivery reliability.
