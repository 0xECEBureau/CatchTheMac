from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def support():
    flag = "MAC{S0C14L_3NG1N33R1NG_1S_R34L_H4CK1NG}"
    if request.method == "POST":
        name = request.form.get("name", "").lower()
        msg = request.form.get("message", "").lower()

        if ("presidente" in name or "présidente" in name) and "dossier" in msg and "mac" in msg and ("ec2" in msg or "fic" in msg):
            response = f"Accès autorisé. Voici le fichier : {flag}"
        else:
            response = "Votre ticket a été reçu. Nous reviendrons vers vous."
        return render_template("support.html", response=response)
    return render_template("support.html", response=None)



@app.route("/archives-secretes")
def archives():
    return render_template("archives.html")



@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path, "static"), "robots.txt")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
