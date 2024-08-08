from flask import (
    render_template, redirect, url_for, 
    session, send_file, abort, Flask,
    request, flash, get_flashed_messages
)

app = Flask(__name__)

@app.before_request
def before_each_request():
    if request.path.startswith("/s"):
        if not session.get("id", False):
            return redirect(url_for("login"))

    if request.path.startswith("/a"):
        if not session.get("admin_id", False):
            return redirect(url_for("admin_login"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        date_of_birth = request.form["date_of_birth"]
        # validate username and date of birth
        # if valid, log in user and redirect to /s
        session["id"] = username
        flash("Logged in successfully!")
        return redirect(url_for("s_index"))
    return render_template("login.html")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        date_of_birth = request.form["date_of_birth"]
        # validate username and date of birth
        # if valid, log in admin and redirect to /a
        session["admin_id"] = username
        flash("Logged in successfully!")
        return redirect(url_for("a_functions"))
    return render_template("admin_login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        date_of_birth = request.form["date_of_birth"]
        # validate username and date of birth
        # if valid, create new user and redirect to /login
        flash("User created successfully!")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/s")
def s_index():
    return render_template("s_index.html")


@app.route("/s/f")
def s_functions():
    return render_template("s_functions.html")


@app.route("/s/f/<int:function_id>")
def s_function_view(function_id: int):
    # retrieve function details from database
    # render function view template
    return render_template("s_function_view.html")


@app.route("/s/scanqr")
def s_scanqr():
    return render_template("s_scanqr.html")


@app.route("/a/f")
def a_functions():
    return render_template("a_functions.html")


@app.route("/a/f/create", methods=["GET", "POST"])
def a_function_create():
    if request.method == "POST":
        # create new function
        flash("Function created successfully!")
        return redirect(url_for("a_functions"))
    return render_template("a_function_create.html")


@app.route("/a/f/<int:function_id>")
def a_function_view(function_id: int):
    # retrieve function details from database
    # render function view template
    return render_template("a_function_view.html")


@app.route("/a/f/<int:function_id>/delete", methods=["POST"])
def a_function_delete(function_id: int):
    # delete function
    flash("Function deleted successfully!")
    return redirect(url_for("a_functions"))

if __name__=="__main__":
    app.run(debug=True)