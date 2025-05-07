from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 Brochure Subscription App is Running!"

if __name__ == '__main__':
    app.run()

