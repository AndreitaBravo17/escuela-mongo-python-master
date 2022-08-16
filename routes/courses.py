
from flask import request, jsonify, Response
from bson import json_util
from bson.objectid import ObjectId

def insert(mongo):
    if request.method == "POST":
        # Obtenemos los datos
        nivel = request.form["nivel"]
        paralelo = request.form["paralelo"]
        docente = request.form["docente"]
        # Verificamos que no exista esa aula
        buscarAula = mongo.db.aulas.find_one({
            "nivel": nivel,
            "paralelo": paralelo
        })

        if buscarAula != None:
            return jsonify({
                "error": "Aula ya existe" 
            })

        # Verificamos si el docente no ha sido asignado
        buscarDocente = mongo.db.aulas.find_one({
            "docente": ObjectId(docente)        
        })

        if buscarDocente != None:
            return jsonify({
                "error": "Docente ya ha sido asignado" 
            })
        
        data = {
            "nivel": nivel, 
            "paralelo": paralelo,
            "docente": ObjectId(docente),
            "estudiantes": []
        }

        # Inseramos el auka nueva
        result = mongo.db.aulas.insert_one(data)
        if result:
            # Retornamos un json como respuesta
            return jsonify({"result": True})

        return jsonify({"result": False})

    if request.method == "GET":
        result = mongo.db.aulas.aggregate([
            { "$lookup": {
                    "from": "usuarios",
                    "foreignField": "_id",
                    "localField": "docente",
                    "as": "docente"
                }
            }
        ])
        response = json_util.dumps(result)
        return Response(response, mimetype="application/json")
    
    return f"<h1>No ha enviado datos</h1>"

def delete(mongo):
    if request.method == "POST":
        id = request.form["id"]
        mongo.db.aulas.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": True})
    if request.method == "GET":
        return jsonify({"result": False})