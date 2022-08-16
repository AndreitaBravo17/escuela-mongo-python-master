from flask import request, jsonify, render_template, Response
import json
from bson import json_util

def login():
    return render_template('layouts/docente.html')

def process(mongo):
    if request.method == "POST":
        # Obtenemos los datos enviamos y los almacenamos
        username = request.form["username"]
        password = request.form["password"]
        # Creamos el objeto con los datos que buscaremos
        data = {"Cedula": username, "Contraseña": password}
        # Ejecutamos la consulta
        res = mongo.db.docentes.find_one(data)
        # Verfiicamos si la consulta obtuvo resultados
        if res:
            # Retornamos un json
            return jsonify(json.dumps(res, default=str))
        else:
            return jsonify({"result": False}) 
    else:
        # En caso de querer acceder a la ruta sin enviar nada
        return f"<h1>No ha enviado datos</h1>"

def get_and_post(mongo):
    # Buscamos el rol por defecto del docente
    rol = mongo.db.roles.find_one({"descripcion": "docente"})   
    rol_permiso = mongo.db.roles_permisos.find_one({"rol": rol["_id"]})
    
    # Creamos el nuevo docente para guardar
    if request.method == "POST":
        cedula = request.form["cedula"]
        nombre = request.form["nombre"]
        # Verificamos que no exista esa cedula en la base de datos
        buscarCedula = mongo.db.usuarios.find_one({"cedula": cedula})
        if buscarCedula :
            return jsonify({"result": False})

        data = {
            "cedula": cedula,
            "nombre": nombre,
            "username":  "@_" + cedula,
            "password" : cedula,
            "roles_permisos": [rol_permiso["_id"]]
        }

        # Insertamos el nuevo docente
        mongo.db.usuarios.insert_one(data)

        return jsonify({"result": True})
    if request.method == "GET":
        result = json_util.dumps(mongo.db.usuarios.find({"roles_permisos": {"$all": [rol_permiso["_id"]]}}))
    
        return Response(result, mimetype="application/json")