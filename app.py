from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(_name_)

title = "To-Do sample application with Flask and MongoDB"
heading = "To-Do Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
todos = db.todos

def redirect_url():
    return request.args.get('next') or \ 
    request.referrer or \
    url_for('index')

@app.route("/list")
def lists():
    todos_1= todos.find()
    ar1="active"
    return render_template('index.html', ar1=ar1, todos = todos_1, title=title, heading=heading)    

@app.route("/")
@app.route("/incomplete")
def tasks():
    todos_1 = todos.find({"done": "no"})
    ar2="active"
    return render_template('index.html', ar2=ar2, todos = todos_1, title=title, heading=heading)


@app.route("/completed")
def completed():
    todos_1 = todos.find({"done": "yes"})
    ar3="active"
    return render_template('index.html', ar3=ar3, todos = todos_1, title=title, heading=heading)

@app.route("/done")
def done():
    id = request.values.get("_id") 
    task = todos.find({"_id":ObjectId(id)})  
    if(task[0]["done"] == "yes"):
        todos.update({"_id":ObjectId(id), {"$set": {"done": "no"}}}) 
    else:
        todos.update({"_id":ObjectId(id), {"$set": {"done": "yes"}}})  
    redir = redirect_url()

    return redirect(redir)

@app.route("/action", methods=['POST']) 
def addTask(): 
    name = request.values.get("name")
    desc = request.values.get("desc") 
    date = request.values.get("date")
    priority = request.values.get("priority")
    todos.insert({"name": name, "desc": desc, "date": date, "priority": priority, "done": "no"})
    return redirect("/list")

@app.route("/remove")
def deleteTask():
    key = request.values.get("_id")
    task = todos.find({"_id":ObjectId(id)})
    return render_template('update.html', tasks = task, heading = heading, title = title)

@app.route("/update")   
def update():
    id = request.values.get("_id")
    task = todos.find({"_id":ObjectId(id)})
    return render_template('update.html', tasks = task, heading = heading, title = title) 

@app.route("/action3", methods = ['POST'])  
def updateTask():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    priority = request.values.get("priority")
    id = request.values.get("id")
    todos.update({"_id":ObjectId(id)}, {'$set':{"name" : name, "desc" : desc, "date": date, "priority": priority}})
    return redirect("/")

@app.route("/search", methods = ['GET'])
def search():
    key = request.values.get("key")
    refer = request.values.get("refer")
    if (key == "_id"):
        todos_1 = todos.find({refer:ObjectId(key)})  
    else:
        todos_1 = todos.find({refer:key})
    return render_template('searchilst.html', todos=todos_1, title = title, heading = heading)          

if __name__ =="__main__" :

    app.run()