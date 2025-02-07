import kavenegar


def send_temporary_code(phone_number, code):
    api = kavenegar.KavenegarAPI("API_KEY")

    try:
        response = api.sms_send(
            sender="YOUR_SENDER_NUMBER",
            receptor=phone_number,
            message=f"Your temporary password is: {code}",
        )
    except kavenegar.exceptions.KavenegarAPIException as e:
        print(f"Error: {e}")
