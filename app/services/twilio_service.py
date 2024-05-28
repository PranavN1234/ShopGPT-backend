import twilio
from twilio.rest import Client
import os



twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
twilio_service_id = os.environ.get('TWILIO_SERVICE_ID')
def send_twilio_otp(phone_number):
    verification = twilio_client.verify.v2.services(twilio_service_id).verifications.create(to=phone_number, channel='sms')

    return verification.status

def verify_twilio_otp(otp, phone_number):
    verification_check = twilio_client.verify.v2.services(twilio_service_id).verification_checks.create(to=phone_number, code=otp)
    return verification_check.status

