from flask import (
    render_template, redirect, url_for, 
    session, send_file, abort, Flask,
    request, flash, get_flashed_messages
)
import settings

app = Flask(__name__)


@app.before_request
def before_each_request():
    if request.endpoint.startswith("/s"):
        if not session.get("id", False):
            return redirect(url_for("login"))

    if request.endpoint.startswith("/a"):
        if not session.get("admin_id", False):
            return redirect(url_for("admin_login"))


@app.get("/")
def index():
    render_template("index.html")


@app.get("/login")
def login_get():
    render_template("login.html")

@app.post("/login")
def login_post():
    if request.method == "POST":
        username = request.form.get("username")
        password = hashPassword(request.form.get("password", ""))
        exists = DB.checkUser(username, password)
        if not exists:
            session["error"] = "Invalid Username or Password!"
            return redirect(url_for("login_post"))

        user = DB.getUserId(username)
        if user is None:
            session["error"] = "User Id Fetch Error! Report this to admins."
            return redirect(url_for("login_post"))

        userSession = DB.createUserSession(user)

        if userSession is None:
            session["error"] = "Create Session Error! Report this to admins."
            return redirect(url_for("login_post"))

        session["username"] = username
        session["sessionid"] = userSession.id
        session["success"] = "Login Successful!"
        return redirect(url_for("index"))



@app.get("/admin_login")
def admin_login_get():
    ...

@app.post("/admin_login")
def admin_login_post():
    ...



@app.get("/register")
def register_get():
    ...

@app.post("/register")
def register_post():
    ...


@app.get("/s")
def s_index():
    ...


@app.get("/s/f")
def s_functions():
    ...

@app.get("/s/f/<int:function_id>")
def s_function_view(function_id: int):
    ...


@app.get("/s/scanqr")
def s_scanqr():
    ...



@app.get("/a/f")
def a_functions():
    ...


@app.get("/a/f/create")
def a_function_create_get():
    ...

@app.post("/a/f/create")
def a_function_create_post():
    ...


@app.get("/a/f/<int:function_id>")
def a_function_view_get(function_id: int):
    ...


@app.post("/a/f/<int:function_id>")
def a_function_view_post(function_id: int):
    ...


@app.post("/a/f/<int:function>/delete")
def a_function_view_delete_post(function_id: int):
    ...


@app.post("/a/f/<int:function_id>/<int:session_id>/delete")
def a_function_session_delete(function_id: int, session_id: int):
    ...



if __name__ == "__main__":
    app.run(
        host = settings.HOST,
        port = settings.PORT
    )
