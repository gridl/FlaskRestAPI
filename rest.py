from flask import Flask, jsonify, abort, make_response, request, url_for
import os

app = Flask(__name__)
tasks = [
    {
        'id': 10,
        'title': 'Title 1',
        'description': 'Rest API',
        'done': False
    },
    {
        'id': 3,
        'title': 'Title 2',
        'description': 'IOS ',
        'done': False
    }
]
#GET ALL
@app.route('/list/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/test')
def get_test():
    for i in tasks:
        return jsonify({'task': i})

@app.route('/list/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    #print task
    if len(task) == 0:
        abort(404)
    return jsonify({'task' : tasks[0]})

@app.route('/list/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] +1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False

    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/list/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort (400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task' : task[0]})

@app.route('/list/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len (task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['url'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
        server = '127.0.0.1'
        port = int(os.environ.get('PORT', 8001))
        app.run(host=server, port=port, debug=True)

