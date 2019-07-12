import time

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522
from flask import Flask, Response, request, render_template


reader = SimpleMFRC522()
app = Flask(__name__)
scans = set()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inventory")
def inventory():
    inventory = {}
    return render_template('inventory.html')

@app.route('/register')
def my_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    text = request.form['text']
    try:
        id, text = reader.write(text)
    finally:
        GPIO.cleanup()
    return "Registered {text} to {id}".format(text=text, id=id)

@app.route("/checkout")
def checkout():
    global scans
    checkout = scans
    scans = set()
    return render_template('checkout.html', rows=checkout)

@app.route('/scanning')
def scanning():
    start = time.time()
    timeout = 1.0
    while time.time() < start + timeout:
        try:
            id, text = reader.read_no_block()
            if (id and id not in scans):
                scans.add(id)
                break
        finally:
            GPIO.cleanup()
    return render_template('stream.html', rows=scans)

    
       