from flask import Blueprint, request
from app.models import Employee, LunchTime
from twilio.twiml.messaging_response import MessagingResponse

messaging = Blueprint("messaging", __name__)


@messaging.route("/sms", methods=["POST"])
def sms_response():
    """
    a webhook that captures the text message sent to create 
    """
    number = request.form["From"]
    message_body = request.form["Body"]
    response = MessagingResponse()
    print(number)
    print(message_body)


@messaging.route("/hello")
def hello():
    return "Hello World"
