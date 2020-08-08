from flask import Blueprint
from app.models import Employee, LunchTime
from twilio.twiml.messaging_response import MessagingResponse

messaging = Blueprint("messaging", __name__)


@messaging.route("/sms", methods=["GET", "POST"])
def sms_response():
    """
    a webhook that captures the text message sent to create 
    """
    pass
