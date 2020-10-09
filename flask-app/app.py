from flask import Flask, request, escape

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "world")
    return f"SHOWCASE-LAB: Hello perfect {escape(name)}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
