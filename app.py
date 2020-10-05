from flask import Flask, request, escape

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "world")
    return f"IKS-LAB: Hello beautiful {escape(name)}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
