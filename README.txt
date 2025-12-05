Babylon Website (Premium Pub) - Full Package
===========================================

Contents:
- index.html, menu.html, gallery.html, contact.html
- style.css (shared premium styles)
- server.py (Flask backend: saves reservations to reservations.csv, sends email via SMTP, optional Twilio SMS)
- .env (template for environment variables)
- assets/img1.jpg ... img6.jpg (placeholder images)
- reservations.csv will be auto-created by server.py on first reservation

Setup (local):
1. Install Python 3.8+.
2. Create virtualenv:
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
3. Install dependencies:
   pip install flask python-dotenv pillow
   # If you plan to use Twilio SMS:
   pip install twilio
4. Copy .env and fill SMTP and (optionally) Twilio credentials.
5. Run the server:
   python server.py
6. Open http://127.0.0.1:5000/ in your browser.

Notes:
- Do NOT commit real credentials to source control.
- For production email reliability use a transactional provider (SendGrid, Mailgun, SES) and configure SPF/DKIM.
- Twilio requires E.164 phone numbers (e.g. +919876543210) for SMS delivery.

If you want me to modify any copy, UI details, or to produce a deploy-ready guide for Render/ Railway, tell me which platform you prefer.
