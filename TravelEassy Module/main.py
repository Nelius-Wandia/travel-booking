from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from admin_users import AdminUser
# from notifications import SMS, Email
from generals import Generals

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["access_tokens"] = []
generals = Generals()


@app.route("/signup", methods=['GET', 'POST'])
def Register():
    if not request.get_json(): return False
    print(request.get_json())
    # Get User data
    company_name = request.get_json()['company_name']
    phone = request.get_json()['phone']
    email = request.get_json()['email']
    means_type = request.get_json()['means_type']
    till_number = request.get_json()['till_number']
    bank_account = request.get_json()['bank_account']
    crypto_wallet = request.get_json()['crypto_wallet']
    password = request.get_json()['password']
    # img_logo = request.files["img_logo"]
    img_logo = "img_logo.png"

    # create user Account
    metadata = {
        "company_name": company_name,
        "phone": phone,
        "email": email,
        "means_type": means_type,
        "password": password,
        "till_number": till_number,
        "bank_account": bank_account,
        "crypto_address": crypto_wallet,
        "logo": img_logo
    }
    print(metadata)
    user = AdminUser()
    if not user.CreateUser(metadata): 
        return jsonify({
            "state": False,
            "message": "Account Already Exists",
            "data": None
        })
    
    # Send sms verification code set @ user.verification
    # notification = SMS(user_id=user.user_id)
    # message = f"TravelEazzy Verification code\n{user.verification}\n Your logistics partner"
    # notification.SendInstantSMS([phone], message)

    # Respond to request
    access_token = generals.GenAccessToken(app.config["access_tokens"])
    unit_token = {
        "token": access_token,
        "timestamp": generals.GetCurrentTime(),
        "user_id": user.user_id
    }
    app.config["access_tokens"].append(unit_token)
    response = jsonify({
        "state": True,
        "message": "Account Created Successfully",
        "data": None
    })
    response = make_response(response)
    response.set_cookie("auth_token", access_token)
    return response

@app.route('/signin', methods=['GET', 'POST'])
def Login():
    if not request.get_json(): return False
    email = request.get_json()['email']
    password = request.get_json()['password']
    ip_address = request.remote_addr
    print(ip_address)
    user = AdminUser()
    if not user.AuthenticateUser(email, password):
        print("Failed Authentication")
        return jsonify({
            "state": False,
            "message": "Authentication Failed",
            "data": None
        })

    if not user.is_valid():
        return jsonify({
            "state": False,
            "message": "Account is Disabled. Please Contact Admin",
            "data": None
        })

    # user Authentication using email/phone and password
    # Auth_token valid for 30 days
    # @ json return account details including - (account_profile, buses, drivers, products, trips, comments, notifications)
    
    access_token = generals.GenAccessToken(app.config["access_tokens"])
    unit_token = {
        "token": access_token,
        "timestamp": generals.GetCurrentTime(),
        "user_id": user.user_id
    }
    app.config["access_tokens"].append(unit_token)
    response = jsonify({
        "state": True,
        "message": "Account login Successful",
        "data": "Enter json data here ....."
    })
    response = make_response(response)
    response.set_cookie("auth_token", access_token)
    print(app.config["access_tokens"])
    return response

if __name__ == '__main__':
    app.run(debug=True)