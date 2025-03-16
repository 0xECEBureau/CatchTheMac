from flask import Flask, request, jsonify, render_template
import jwt
import datetime
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(24).hex()

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        # read the payload from the token and unbased64 it without using the secret key
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

@app.route("/", methods=["GET", "POST"])
def home():
    token = None
    decoded_data = None
    
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return jsonify({"error": "Username required"}), 400
        if username == "admin":
            return jsonify({"error": "Invalid username"}), 400
        token = generate_token(username)
        # set cookie
        response = jsonify({"token": token})
        response.set_cookie("token", token)
        return response  # Return the response with the token set in the cookie
    
    if request.args.get("token"):
        decoded_data = decode_token(request.args.get("token"))
    
    return render_template("home.html", token=token, decoded_data=decoded_data)

@app.route("/robots.txt", methods=["GET"])
def robots():
    return jsonify({"hidden_pages": "aDmInIsTrAt0oOOooooR_0xECE"})

@app.route("/aDmInIsTrAt0oOOooooR_0xECE", methods=["GET"])
def admin():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token Admin required"}), 400
    
    payload = decode_token(token)
    print(payload)
    if "error" in payload:
        return jsonify(payload), 400
    
    if payload.get("username") != "admin":
        return jsonify({"error": "Access denied"}), 403
    
    return render_template("admin.html", flag="MAC{JwT_1s_vu1n3rabl3}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
