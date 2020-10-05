from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "world")
    return "IKS-LAB: Hello beautiful {escape(name)}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
