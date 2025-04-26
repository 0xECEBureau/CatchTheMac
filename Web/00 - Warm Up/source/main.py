from flask import Flask, Response, render_template

app = Flask(__name__)

@app.route('/')
def index():
    response = Response(render_template('home.html'))
    response.headers['Flag'] = 'MAC{h16den_1n_h3aDeRs}'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)