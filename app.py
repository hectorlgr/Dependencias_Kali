from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def index():
    return "Aplicación de ejemplo para gestión de dependencias"

@app.get("/hello")
def hello():
    nombre = request.args.get("name", "mundo")
    return {"mensaje": f"Hola, {nombre}!"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
