
from flask import request, jsonify, Response
from bson import json_util
from bson.objectid import ObjectId


def access(mongo):
    # Buscamos el rol por defecto del administrador
    rol = mongo.db.roles.find_one({"descripcion": "administrador"})   
    rol_permiso = mongo.db.roles_permisos.find_one({"rol": rol["_id"]})

    if request.method == "POST":
        # Obtenemos los datos enviamos y los almacenamos
        username = request.form["username"]
        password = request.form["password"]
        # Creamos un objeto con las credenciales
        data = {
            "username": username, 
            "password": password, 
        }
        # Buscamos un usuario con las credencial enviadas
        foundUser = mongo.db.usuarios.find_one(data)
        # Si las credenciales están incorrectas retornamos de inmediato
        if foundUser == None:
            return jsonify({
                "access": False, 
                "error": "Usuario o contraseña incorrecto"
            })

        # Creamos un objeto con las credenciales
        data = {
            "username": username, 
            "roles_permisos": [ObjectId(rol_permiso["_id"])]
        }
        # Verificamos si ese usuario es administrador
        result = mongo.db.usuarios.find_one(data, {"password": 0, "username": 0})

        if result:
            # Creamos la respuesta y la retornamos 
            response = {"access": True, "body": result}
            response = json_util.dumps(response)
            return Response(response, mimetype="application/json")

        else:
            response = {
                "access": False,
                "error": "Acceso denegado. Usuario no es administrador"
            }     
            response = json_util.dumps(response)
            return Response(response, mimetype="application/json")

    else:
        # En caso de querer acceder a la ruta sin enviar nada
        return f"<h1>No ha enviado datos</h1>"
