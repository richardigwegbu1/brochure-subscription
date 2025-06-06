import os
import uuid
import stripe
import boto3
import gspread
from flask import Flask, render_template, request, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Stripe setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = os.getenv("DOMAIN")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDS_JSON"), scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).worksheet(os.getenv("GOOGLE_SHEET_NAME"))

# S3 setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("S3_REGION")
)


@app.route('/')
def home():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    date = request.form['date']
    full_name = request.form['full_name']
    email = request.form['email']
    phone = request.form['phone']
    comment = request.form['comment']
    paid = "5"  # Fixed price for regular page

    file = request.files['file']
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    s3.upload_fileobj(file, os.getenv("S3_BUCKET_NAME"), filename)
    s3_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('S3_REGION')}.amazonaws.com/{filename}"

    # Log to Google Sheet
    sheet.append_row([date, full_name, email, phone, comment, paid, s3_url])

    # Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 500,  # $100 in cents

                'product_data': {
                    'name': 'Regular Brochure Page Subscription'
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"{DOMAIN}/success?name={full_name}",
        cancel_url=f"{DOMAIN}/",
    )

    return redirect(session.url, code=303)

@app.route('/success')
def success():
    full_name = request.args.get("name", "Friend")
    return render_template("success.html", full_name=full_name)

if __name__ == '__main__':
    app.run(debug=True)

