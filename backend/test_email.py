"""
Test script for email notification functionality
Run this to test if email sending works correctly
"""
import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.email_service import EmailService

async def test_email():
    """Test sending a violation email"""
    print("=" * 60)
    print("  ITMS Email Notification Test")
    print("=" * 60)
    print()
    
    # Check environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    
    print("Configuration Check:")
    print(f"  ✓ Sender Email: {sender_email}")
    print(f"  ✓ SendGrid API Key Set: {'Yes' if sendgrid_key else 'No'}")
    print(f"  ✓ API Key Length: {len(sendgrid_key) if sendgrid_key else 0} characters")
    print()
    
    if not sendgrid_key:
        print("❌ Error: SendGrid API key not configured!")
        print("   Please run: setup_email.ps1")
        return False
    
    if not sendgrid_key.startswith("SG."):
        print("⚠ Warning: SendGrid API key should start with 'SG.'")
        print()
    
    # Create email service
    email_service = EmailService()
    
    print("Sending test email...")
    print(f"  From: {sender_email}")
    print(f"  To: {email_service.recipient_email}")
    print()
    
    # Send test email
    try:
        success = await email_service.send_violation_email(
            vehicle_number="TEST-1234",
            violation_type="No Helmet Violation (TEST)",
            fine_amount=500.0,
            location="Test Location - System Check",
            timestamp=datetime.now(),
            violation_id="TEST-" + datetime.now().strftime("%Y%m%d%H%M%S"),
            image_path=None,
            confidence=0.95
        )
        
        if success:
            print("=" * 60)
            print("✅ SUCCESS! Test email sent successfully!")
            print("=" * 60)
            print()
            print(f"Check inbox at: {email_service.recipient_email}")
            print("(Also check spam folder if not in inbox)")
            print()
            return True
        else:
            print("=" * 60)
            print("❌ FAILED! Email could not be sent")
            print("=" * 60)
            print()
            print("Check the error messages above for details")
            return False
            
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        print()
        print("Common issues:")
        print("  1. Invalid SendGrid API key")
        print("  2. API key doesn't have 'Mail Send' permissions")
        print("  3. SendGrid account not verified")
        print("  4. Network/firewall blocking API requests")
        print()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_email())
    sys.exit(0 if result else 1)
