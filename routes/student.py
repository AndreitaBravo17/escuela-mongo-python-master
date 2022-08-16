
from flask import request, jsonify, Response
from bson import json_util
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename

def delete(mongo, path):
    
    if request.method == "POST":
        id = request.form["id"]
        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        imgRuta = usuario["path"]
        os.unlink(os.path.join(path, imgRuta))
        mongo.db.usuarios.delete_one({"_id": ObjectId(id)})

        return jsonify({
            "result": True,
            "message": "Usuario eliminado correctamente"
        })
    if request.method == "GET":
        return jsonify({"result": False})

def save(mongo, path):
     # Buscamos el rol por defecto del docente
    rol = mongo.db.roles.find_one({"descripcion": "estudiante"})   
    rol_permiso = mongo.db.roles_permisos.find_one({"rol": rol["_id"]})

    if request.method == "POST":
        cedula = request.form["cedula"]
        aula = request.form["aula"]
        nombre = request.form["nombre"]
        # Verificamos si ya existe esa cedula
        foundUser = mongo.db.usuarios.find_one({"cedula": cedula})
        if foundUser:
            return jsonify({
                "result": False,
                "error": "Ya existe usuario con esa cédula"
            })

        keyName = "foto_"
        imagen = request.files['imagen']
        extension = secure_filename(imagen.filename).split(".")[1].lower() 
        # Nombre orignal de la imagen
        imgRuta = keyName + cedula+"." + extension
        imagen.save(os.path.join(path, imgRuta))

        data = {
            "cedula": cedula,
            "nombre": nombre,
            "username":  "@_" + cedula,
            "password" : cedula,
            "path": imgRuta,
            "roles_permisos": [rol_permiso["_id"]]
        }

        mongo.db.usuarios.insert_one(data)

        return jsonify({"result": True})
    if request.method == "GET":
        result = json_util.dumps(mongo.db.usuarios.find({"roles_permisos": {"$all": [rol_permiso["_id"]]}}))
    
        return Response(result, mimetype="application/json")