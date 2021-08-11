from flask import Flask, request, jsonify
from models import db, Task
from flask_cors import CORS 

#from models import Person

app = Flask(__name__)
 # This will enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://jonathan:123456@localhost/jonathan_base_de_datos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/tareas": {"origins": "http://localhost:port"}})
CORS(app)

db.init_app(app)

# generate sitemap with all your endpoints
@app.route('/') #Esto es un decorador
def home():
    return jsonify({"mensaje":"Bienvenidos a mi app"})

@app.route('/tareas/<id>', methods=['GET'])
def get_detail_task(id):
    task_found = Task.query.get(id)
    if not task_found:
        return jsonify({ "message": 'tarea no encontrada', "tareas": {}})
    return jsonify({ "message": 'tarea obtenida satisfactoriamente', "task": task_found.serialize()})

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tasks = Task.query.all()
    print(tasks)
    allTasks = [task.serialize() for task in tasks]
    return jsonify({"mensaje":"Bienvenidos a mi app GET",'tasks': allTasks})

@app.route('/tareas', methods=['POST'])
def agregar_tareas_post():
    name = request.json["name"]
    done = request.json["done"]
    new_task = Task(name = name, done = done)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"mensaje":"Bienvenidos a mi app POST","task" : new_task.serialize()})

@app.route('/tareas/<id>', methods=['PUT'])
def get_update_task(id):
    task_found = Task.query.get(id)
    if not task_found:
       return jsonify({ "message": 'tarea no encontrada', "task": {}}).headers.add('Access-Control-Allow-Origin', '*')
    task_found.name = request.json["name"]
    task_found.done = request.json["done"]

    db.session.commit()
    return jsonify({ "message": 'tarea actualizada satisfactoriamente', "task": task_found.serialize()})

@app.route('/tareas/<id>', methods=['DELETE'])
def get_delete_task(id):
    task_found = Task.query.get(id)
    if not task_found:
        return jsonify({ "message": 'tarea no encontrada', "task": {}})

    db.session.delete(task_found)
    db.session.commit()

    return jsonify({ "message": 'tarea eliminada satisfactoriamente'})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=True)
