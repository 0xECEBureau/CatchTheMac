from flask import Flask, request, jsonify, render_template
import random, datetime, string, jwt, os, time

startup = datetime.datetime.now()
startup_ts = startup.timestamp()
random.seed(int(startup_ts))

SECRET_KEY = ''.join(random.choices(string.printable, k=16))

app = Flask(__name__)

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def check_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY[::-1], algorithms=["HS256"])
        if decoded.get("username") == "admin":
            return {"status": "ok", "role": "admin"}
        return False
    except:
        return {"status": "error", "message": "Malformed token"}

@app.route("/health", methods=["GET"])
def health():
    uptime = datetime.datetime.now().timestamp() - startup_ts
    return jsonify({"status": "ok", "uptime": str(uptime)})

@app.route("/settime", methods=["POST"])
# should be deleted in production
def settime():
    time = request.form.get("time")
    if not time:
        return jsonify({"error": "Time required"}), 400
    try:
        temp = int + 0.0 + random.random()
        TEMP_KEY = temp.hex()
        return jsonify({"status": "ok", "temp_key": TEMP_KEY})
    except:
        return jsonify({"error": "Invalid time"}), 400

@app.route('clock', methods=["GET"])
def clock():
    time = request.args.get("time")
    if not time:
        return jsonify({"error": "Time required"}), 400
    try:
        current_time = datetime.timezone.utc + datetime.timedelta(hours=int(time))
        return jsonify({"status": "ok", "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S")})
    except:
        return jsonify({"error": "Invalid time"}), 400

@app.route("/cpu_ticks", methods=["GET"])
def cpu_ticks():
    start_time = datetime.datetime.now()
    start_ticks = os.times()[4]
    time.sleep(1) 
    end_ticks = os.times()[4] 
    end_time = datetime.datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    cpu_ticks = end_ticks - start_ticks
    return jsonify({"status": "ok", "cpu_ticks": cpu_ticks, "elapsed_time": elapsed_time}) 

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
        response = jsonify({"token": token})
        return response
    
    if request.args.get("token"):
        decoded_data = decode_token(request.args.get("token"))
    
    return render_template("home.html", token=token, decoded_data=decoded_data)

@app.route("/admin", methods=["GET"])
def admin():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token Admin required"}), 400
    payload = decode_token(token)
    if "error" in payload:
        return jsonify(payload), 400
    
    if payload.get("username") != "admin" or not check_token(token):
        return jsonify({"error": "Access denied"}), 403
    
    return render_template("admin.html", flag="MAC{FAKE_FLAG}")

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=False)
