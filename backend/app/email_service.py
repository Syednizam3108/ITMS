"""
Email service for sending violation penalty slip notifications using SendGrid
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from datetime import datetime
from typing import Optional
import os
import base64

class EmailService:
    def __init__(self):
        # SendGrid configuration
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY", "")
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@itms.gov")
        self.recipient_email = "syednizamsyed225@gmail.com"
        
    async def send_violation_email(
        self,
        vehicle_number: str,
        violation_type: str,
        fine_amount: float,
        location: str,
        timestamp: datetime,
        violation_id: str,
        image_path: Optional[str] = None,
        confidence: Optional[float] = None
    ):
        """Send email notification for violation with penalty slip using SendGrid"""
        try:
            if not self.sendgrid_api_key:
                print("⚠️ SendGrid API key not configured")
                return False
            
            # Create HTML email body with penalty slip
            html_body = self._create_penalty_slip_html(
                vehicle_number=vehicle_number,
                violation_type=violation_type,
                fine_amount=fine_amount,
                location=location,
                timestamp=timestamp,
                violation_id=violation_id,
                confidence=confidence
            )
            
            # Create SendGrid message
            message = Mail(
                from_email=self.sender_email,
                to_emails=self.recipient_email,
                subject=f"🚨 Traffic Violation Alert - {violation_type}",
                html_content=html_body
            )
            
            # Attach violation image if available
            if image_path and os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as img_file:
                        img_data = img_file.read()
                        encoded_file = base64.b64encode(img_data).decode()
                        
                        attachment = Attachment(
                            FileContent(encoded_file),
                            FileName(os.path.basename(image_path)),
                            FileType('image/jpeg'),
                            Disposition('attachment')
                        )
                        message.attachment = attachment
                except Exception as img_err:
                    print(f"⚠️ Could not attach image: {img_err}")
            
            # Send email via SendGrid
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 202]:
                print(f"✅ Email sent successfully to {self.recipient_email} for violation {violation_id}")
                return True
            else:
                print(f"⚠️ SendGrid returned status code: {response.status_code}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def _create_penalty_slip_html(
        self,
        vehicle_number: str,
        violation_type: str,
        fine_amount: float,
        location: str,
        timestamp: datetime,
        violation_id: str,
        confidence: Optional[float] = None
    ) -> str:
        """Create HTML formatted penalty slip"""
        confidence_text = f" (Confidence: {confidence:.0%})" if confidence else ""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .penalty-slip {{
                    background-color: white;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #dc2626;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .info-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 12px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #374151;
                }}
                .info-value {{
                    color: #6b7280;
                }}
                .violation-box {{
                    background-color: #fef2f2;
                    border-left: 4px solid #dc2626;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .violation-type {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #dc2626;
                }}
                .fine-amount {{
                    background-color: #fee2e2;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .fine-amount h2 {{
                    margin: 0;
                    color: #991b1b;
                    font-size: 32px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                    text-align: center;
                    color: #6b7280;
                    font-size: 12px;
                }}
                .warning {{
                    background-color: #fffbeb;
                    border: 1px solid #fbbf24;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="penalty-slip">
                <div class="header">
                    <h1>🚨 TRAFFIC VIOLATION PENALTY SLIP</h1>
                    <p style="margin: 5px 0 0 0;">Intelligent Traffic Management System</p>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Violation ID:</span>
                    <span class="info-value">{violation_id}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Vehicle Number:</span>
                    <span class="info-value">{vehicle_number}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Date & Time:</span>
                    <span class="info-value">{timestamp.strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Location:</span>
                    <span class="info-value">{location}</span>
                </div>
                
                <div class="violation-box">
                    <div class="violation-type">
                        ⚠️ {violation_type}{confidence_text}
                    </div>
                </div>
                
                <div class="fine-amount">
                    <p style="margin: 0; font-size: 14px; color: #991b1b;">PENALTY AMOUNT</p>
                    <h2>₹{fine_amount:,.2f}</h2>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Important Notice:</strong><br>
                    This violation has been automatically detected and recorded by our AI-powered traffic management system. 
                    Please pay the fine within 15 days to avoid additional penalties.
                </div>
                
                <div class="footer">
                    <p><strong>Intelligent Traffic Management System (ITMS)</strong></p>
                    <p>This is an automated email. Please do not reply.</p>
                    <p>For queries, contact: support@itms.gov</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

# Global email service instance
_email_service = None

def get_email_service() -> EmailService:
    """Get or create email service singleton"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
