from flask import Flask, request, jsonify, render_template, send_file, redirect
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():    
    return render_template("home.html")

@app.route("/admin", methods=["GET"])
def admin():    
    return render_template("admin.html")

# trick to handle easily post pages
@app.route("/page", methods=["GET"])
def index():
    template_name = request.args.get("template_name")
    if not template_name:
        return jsonify({"error": "No template specified"}), 400
    try:
        # DevOps teacher told me to do this, so I did
        # I don't know if it's a good idea, but it works
        pwd = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(pwd, "templates", template_name)
        if not os.path.exists(template_path):
            return jsonify({"error": "Template not found"}), 404
        if os.path.isfile(template_path):
            return send_file(template_path, as_attachment=False)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/posts", methods=["GET"])
def posts():
    return redirect("/page?template_name=posts.html")

@app.route("/contact", methods=["GET"])
def contact():
    return redirect("/page?template_name=contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
