import time

# import RPi.GPIO as GPIO

# from mfrc522 import SimpleMFRC522
from app import app, db
from flask import Response, request, render_template

from app.models import Book
# reader = SimpleMFRC522()
scans = set()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inventory")
def inventory():
    books = Book.query.all()
    return render_template('inventory.html', rows=books)

@app.route('/register')
def my_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    text = request.form['text']
    # try:
    #     rfid, title = reader.write(text)
    # finally:
    #     GPIO.cleanup()
    book = Book(rfid=rfid, title=title)
    db.session.add(book)
    db.session.commit()
    return "Registered {title} to {rfid}".format(rfid=rfid, title=title)

@app.route("/checkout")
def checkout():
    global scans
    checkout = scans
    scans = set()
    return render_template('checkout.html', rows=checkout)

@app.route('/scanning')
def scanning():
    # start = time.time()
    # timeout = 1.0
    # while time.time() < start + timeout:
    #     try:
    #         id, text = reader.read_no_block()
    #         if (id and id not in scans):
    #             scans.add(id)
    #             break
    #     finally:
    #         GPIO.cleanup()
    return render_template('stream.html', rows=scans)


