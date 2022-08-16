
from flask import request, jsonify, Response
from bson import json_util
from bson.objectid import ObjectId

def delete(mongo):
    # Buscamos el rol por defecto del docente
    rol = mongo.db.roles.find_one({"descripcion": "docente"})   
    rol_permiso = mongo.db.roles_permisos.find_one({"rol": rol["_id"]})

    if request.method == "POST":
        id = request.form["id"]
        # Verificamos si el usuario es un docente y ya está asignado a una aula
        # En caso de estarlo retornará una alerta
        foundUser = mongo.db.aulas.find_one({"docente": ObjectId(id)})
        if foundUser:
            response = {
                "result": False,
                "error": "No es posible borrar el docente, está asignado a un aula."
            }

            return jsonify(response)
        
        # En caso de no está asignado lo eliminará
        mongo.db.usuarios.delete_one({"_id": ObjectId(id)})
        return jsonify({
            "result": True,
            "message": "Usuario eliminado correctamente"
        })
    if request.method == "GET":
        return jsonify({"result": False})