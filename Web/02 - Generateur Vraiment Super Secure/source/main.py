from flask import Flask, request, jsonify, render_template
import jwt 
import datetime

app = Flask(__name__)
SECRET_KEY = "lovelovelove"

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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
            return jsonify({"error": "Forbidden username"}), 403
        token = generate_token(username)
        # set cookie
        response = jsonify({"token": token})
        response.set_cookie("token", token)
        return response
    
    if request.args.get("token"):
        decoded_data = decode_token(request.args.get("token"))
    
    return render_template("home.html", token=token, decoded_data=decoded_data)

@app.route("/robots.txt", methods=["GET"])
def robots():
    return jsonify({"hidden_pages": "aDmI-nIsTrAt@0oOOoooo00R_0x3Ce"})

@app.route("/aDmI-nIsTrAt@0oOOoooo00R_0x3Ce", methods=["GET"])
def admin():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token Admin required"}), 400
    
    payload = decode_token(token)
    if "error" in payload:
        return jsonify(payload), 400
    
    if payload.get("username") != "admin":
        return jsonify({"error": "Access denied"}), 403
    
    return render_template("admin.html", flag="MAC{Y0u_4r3_4_1337_h4ck3r}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
