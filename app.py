from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from DAO.SessionDAO import SessionDAO
from DAO.ProductsDAO import ProductsDAO
from bson.json_util import dumps
app = Flask(__name__)


@app.route('/')
def index():
    return "API de productos"


# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    session = SessionDAO()
    if session.login(username, password):
        return jsonify({"status": True, "message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"status": False, "message": "Inicio de sesión fallido: contraseña o usuario incorrecto"}), 400


# Ruta para obtener todos los productos
@app.route('/register', methods=['POST'])
def user_register():
    data = request.get_json()
    name = data["username"]
    email = data["email"]
    password = data["password"]
    session = SessionDAO()
    if session.existName(name) and session.existEmail(email):
        return jsonify({"status": False, "message": "Ya existe ese usuario o email"}), 400

    result = session.register(name, email, password)
    return jsonify({"status": result, "message:": "Registro completo"}), 201


@app.route('/GetAllProducts', methods=['GET'])
def GetProducts():
    products = ProductsDAO()
    result = products.GetProducts()
    if result is None:
        return jsonify({"status": False, "message": "No hay productos"}), 404
    else:
        return jsonify({"status":True, "data": result}), 200

@app.route('/RegisterProduct', methods=['POST'])
def RegisterProducts():
    data = request.get_json()
    products = ProductsDAO()
    result = products.RegisterProduct(data["name"], data["description"], data["image"], data["price"], data["stock"])
    if result is None:
        return jsonify({"status": False, "message": "Error"}), 404
    else:
        return jsonify({"status":True, "data": result}), 200
    
@app.route('/DeleteProduct', methods=['DELETE'])
def DeleteProducts():
    data = request.get_json()
    products = ProductsDAO()
    result = products.DeleteProduct(data["id"])
    if result is None:
        return jsonify({"status": False, "message": "No hay producto"}), 404
    else:
        return jsonify({"status":True, "data": result}), 200
    
    
if __name__ == '__main__':
    app.run(debug=True)
