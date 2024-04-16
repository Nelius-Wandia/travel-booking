from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from admin_users import AdminUser
from buses import Buses
from notifications import SMS, Email
from generals import Generals

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["access_tokens"] = []
generals = Generals()

def ValidateToken(cookie_data):
    if not cookie_data: return False
    auth_token = cookie_data.get('auth_token')
    user_id = False
    for token in app.config["access_tokens"]:
       if token["token"] == auth_token: 
           user_id = token["user_id"]
    
    if not user_id: return False
    user = AdminUser(user_id=user_id)
    if not user.is_valid(): return False
    return user_id


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
    notification = SMS(user_id=user.user_id)
    message = f"TravelEazzy Verification code\n{user.verification}\n Your logistics partner"
    notification.SendInstantSMS([phone], message)

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

    # Fetch User data 
    user_profile = user.FetchUserProfile()
    user_buses = Buses().GetAllBuses(user_id=user.user_id)
    response = jsonify({
        "state": True,
        "message": "Account login Successful",
        "data": {
            "account_profile": user_profile,
            "buses": user_buses,
            "drivers": "Not set"
        }
    })
    response = make_response(response)
    response.set_cookie("auth_token", access_token)
    print(app.config["access_tokens"])
    return response

@app.route("/bus/<string:args>", methods=['GET', 'POST'])
def AddBus(args):
    user_id = ValidateToken(request.cookies)
    print(user_id)
    if not user_id:
        return jsonify({
            "state": False,
            "message": "AuthToken Error",
            "data": None
        })
    
    if args == "add":
        request_data = request.get_json()
        license = request_data["licesnse_plate"]
        no_seats = request_data["no_seats"]
        model = request_data["model"]
        colour = request_data["colour"]
        seat_config = request_data["seat_config"]

        metadata = {
            "company_id": user_id,
            "license_plate": license,
            "no_seats": no_seats,
            "model": model,
            "color": colour,
            "arrangement": seat_config
        }
        bus = Buses()
        bus.AddBus(metadata)

    elif args == "update":
        request_data = request.get_json()
        license = request_data["licesnse_plate"]
        no_seats = request_data["no_seats"]
        model = request_data["model"]
        colour = request_data["colour"]
        seat_config = request_data["seat_config"]

        bus = Buses()
        metadata = {
            "company_id": user_id,
            "license_plate": license,
            "no_seats": no_seats,
            "model": model,
            "color": colour,
            "arrangement": seat_config
        }
        bus.UpdateBus(metadata)

    elif args == "delete":
        bus_id = request.get_json()["bus_id"]
        bus = Buses(bus_id=bus_id)
        bus.DeleteBus()

    # Get all Buses
    user_buses = bus.GetAllBuses(user_id=user_id)
    return jsonify({
        "state": True,
        "message": "Bus added Successfully",
        "data": user_buses
    })
    
if __name__ == '__main__':
    app.run(debug=True)