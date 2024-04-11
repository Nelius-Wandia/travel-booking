from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from admin_users import AdminUser

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/signup", methods=['GET', 'POST'])
def Register(self):
    if not request.get_json() and not request.files: return False
    company_name = request.get_json()['company_name']
    phone = request.get_json()['phone']
    email = request.get_json()['email']
    means_transport = request.get_json()['means_transport']
    till_number = request.get_json()['till_number']
    bank_account = request.get_json()['bank_account']
    crypto_wallet = request.get_json()['ctypto_wallet']
    password = request.get_json()['password']
    img_logo = request.files["img_logo"]

    metadata = {
        "company_name": company_name,
        "phone": phone,
        "email": email,
        "means_type": means_transport,
        "password": password,
        "till_number": till_number,
        "bank_account": bank_account,
        "crypto_address": crypto_wallet,
        "logo": img_logo
    }
    user = AdminUser()
    if not user.CreateUser(metadata): return False
    return "hahahha"

@app.route('/signin', methods=['GET', 'POST'])
def Login():
    if not request.get_json(): return False
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = AdminUser()
    if not user.AuthenticateUser(email, password):return jsonify({
        "state": False
        })
    print("Passed Auth")
    # user Authentication using email/phone and password
    # Auth_token valid for 30 days
    # @ json return account details including - (account_profile, buses, drivers, products, trips, comments, notifications)
    response = jsonify({
        "state": True
    })
    new_response = make_response(response)
    new_response.set_cookie("auth_token",user.user_id)
    return new_response
    # Return Access token

if __name__ == '__main__':
    app.run(debug=True)