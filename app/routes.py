import time

# import RPi.GPIO as GPIO

# from mfrc522 import SimpleMFRC522
from app import app, db
from flask import Response, request, redirect, url_for, render_template

from app.models import Book
# reader = SimpleMFRC522()
scans = set()
cart = set()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/inventory")
def inventory():
    books = Book.query.all()
    return render_template('inventory.html', rows=books)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    form_title = request.form['title']
    # try:
    #     rfid, title = reader.write(form_title)
    # finally:
    #     GPIO.cleanup()
    book = Book(rfid=rfid, title=title)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/checkout")
def checkout():
    global scans, cart
    cart = scans.copy()
    books = Book.query.filter(Book.rfid.in_(cart)).all()
    scans = set()
    return render_template('checkout.html', rows=books)

@app.route("/checkout", methods=['POST'])
def checkout_post():
    global cart
    lendee = request.form['lendee']
    books = Book.query.filter(Book.rfid.in_(cart)).all()
    for book in books:
        book.loaned_to = lendee
        db.session.commit()
    return redirect(url_for('index'))

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
    scans.add(33)
    scans.add(35)
    books = Book.query.filter(Book.rfid.in_(scans)).all()
    return render_template('stream.html', rows=books)


