from flask import Flask, request, redirect, render_template
from pymongo import MongoClient
from bson import json_util
import requests

app = Flask(__name__)

client = MongoClient()
db = client["APIIT"]
collection = db.to_dos

@app.route('/')
def index():
    recipe = "fried rice"
    response = requests.get("http://www.recipepuppy.com/api/?q={recipe}")
    response = response.json()["results"][0]
    return render_template("index.html", recipe=response)

@app.route('/search')
def search():
    recipe = request.args.get('a', 0, type=str)
    response = requests.get("http://www.recipepuppy.com/api/?q={recipe}")
    response = response.json()["results"][0]["title"]
    return jsonify(result=response)
@app.route('/view', methods=['GET'])
def get_todos():
    to_dos = list(collection.find())
    return json_util.dumps(to_dos)


@app.route('/add', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        new_todo = request.get_json()
        name = new_todo['name']
        description = new_todo['description']
        time = new_todo['time']

        collection.insert_one({
            "name": name, 
            "description": description,
            "time": time
        })
        return redirect('/view')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

