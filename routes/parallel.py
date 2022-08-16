from flask import request, jsonify
import json

def insert(mongo):
    if request.method == "POST":
        # Obtenemos los datos
        cedula = request.form["cedula"]
        stars = request.form["stars"]
        # hacemos la actualización
        result = mongo.db.estudiantes.update_one({"Id_Estudiante": cedula}, {
            "$set":{
                "Test.Estrellas": int(stars)
                }
            }
        )

        # Si la actualización salió bien retornamos un true
        if result :
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    if request.method == "GET":
        return f"<h1>No ha enviado datos</h1>"

def student_test(mongo):
    if request.method == "POST":
        cedula = request.form["cedula"]
        tiempo = request.form["tiempo"]
        resuelto = request.form["resuelto"]

        #Cambiar a booleano que viene en la request
        if resuelto == "true":
            resuelto = True
        else:
            resuelto = False

        # Hacemos el guardado de los datos
        result = mongo.db.estudiantes.update_one({"Id_Estudiante": cedula}, {
            "$set":{
                "Test.Tiempo": int(tiempo),
                "Test.Resuelto": resuelto,
                }
            }
        )

        # Si todo va bien retornamos un true
        if result :
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    if request.method == "GET":
        return f"<h1>No ha enviado datos</h1>"

def get_students(mongo):
    if request.method == "POST":
        # REcibimos el paralelo a buscar
        paralelo = request.form["paralelo"]
        # Hacemos la consulta
        res = list(mongo.db.estudiantes.find({"Paralelo":paralelo}))
        # Si la consulta trae resultados los retornamos
        if res:
            # Retormos un json
            return jsonify(json.dumps(res, default=str))
        else:
            return jsonify({"result": False}) 
    if request.method == "GET":
        return f"<h1>No ha enviado datos</h1>"