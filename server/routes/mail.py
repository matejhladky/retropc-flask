from flask import Blueprint, jsonify, request
from flask_mail import Message
from ..extensions import mail

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/send_mail', methods=['POST'])
def send_mail():
    data = request.get_json()
    email = data.get('email')
    message = data.get('message')
    product = data.get('product')

    msg = Message(subject="New Reservation", sender=email, recipients=['mat.hladky@gmail.com'])
    msg.body = f"Email: {email}\nMessage: {message}\nProduct: {product}"
    mail.send(msg)

    return jsonify({"message": "Email sent successfully!"}), 200
