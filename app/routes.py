from flask import (
    Flask, 
    request,
    render_template
    )
import requests
BACKEND_URL = "http://127.0.0.1:5000/tasks"
app=Flask(__name__)


@app.get("/")
def view_home():
    return render_template("index.html")

@app.get("/list")
def view_task_list():
    response = requests.get(BACKEND_URL)
    response = response.json()
    return render_template(
        "list.html",
        tasks=response["tasks"]
    )

@app.get("/tasks/details/<int:task_id>")
def task_detail(task_id):
    URL = "%s/%s" % (BACKEND_URL, task_id)
    response =requests.get(URL).json()
    return render_template(
        "detail.html",
        task=response["task"]
    )

@app.get("/task/new")
def task_form():
    return render_template("new.html")

@app.post("/task/new")
def create_task():
    mssg = "created"
    raw_data = request.form
    task_json = {
        "title": raw_data.get("title"),
        "subtitle": raw_data.get("subtitle"),
        "body": raw_data.get("body")
    }
    response = requests.post(BACKEND_URL, json=task_json)
    if response.status_code == 201:
        return render_template("create_success.html", mssg=mssg)
    else:
        return render_template("create_failure.html", mssg=mssg)

@app.get("/task/update/<int:task_id>")
def task_update_form(task_id):
    return render_template("update_task.html", task_id=task_id)


@app.route("/task/updates/<int:task_id>", methods=["PUT","POST"])
def update_task(task_id):
    mssg="updated"
    URL = "%s/%s" % (BACKEND_URL, task_id)
    raw_data = request.form
    task_json = {
        "id": task_id,
        "title": raw_data.get("title"),
        "subtitle": raw_data.get("subtitle"),
        "body": raw_data.get("body")
    }
    print(task_json)
    response = requests.put(URL, json=task_json)
    if response.status_code == 204:
        return render_template("create_success.html", mssg=mssg)
    else:
        return render_template("create_failure.html", mssg=mssg)


@app.route("/task/<int:task_id>")
def delete_task(task_id):
    mssg = "deleted"
    URL = "%s/%s" % (BACKEND_URL, task_id)
    print(URL)
    response =requests.delete(URL)
    print(response)
    if response.status_code == 204:
        return render_template("create_success.html", mssg=mssg)
    else:
        return render_template("create_failure.html")