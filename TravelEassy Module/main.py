from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from admin_users import AdminUser


app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if not request.get_json(): return False
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = AdminUser()
    if not user.AuthenticateUser(email, password):return jsonify({
        "data": False
        })
    print("Passed Auth")
    # user Authentication using email/phone and password
    # Auth_token valid for 30 days
    response = jsonify({
        "data": "data"
    })
    response = make_response(response)
    response.set_cookie("auth_token","Actual token")
    return response
    # Return Access token

if __name__ == '__main__':
    app.run(debug=True)