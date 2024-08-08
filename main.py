from flask import (
    render_template, redirect, url_for, 
    session, send_file, abort, Flask,
    request, flash, get_flashed_messages
)
import settings
import utils
import utils.image_matcher
import utils.models

app = Flask(__name__)
app.secret_key = "JOH9cg9g(UG8783eyobO_U_Pz;Jc0y9weubB%ze6DRZcxblMc',]d[\\wek[jh]])"

@app.before_request
def before_each_request():
    if request.path.startswith("/s"):
        if not session.get("id", False):
            return redirect(url_for("login"))

    if request.path.startswith("/a"):
        if not session.get("admin_id", False):
            return redirect(url_for("admin_login"))


@app.get("/")
def index():
    render_template("index.html")


@app.get("/login")
def login_get():
    return render_template("login.html")

@app.post("/login")
def login_post():
    rollno = request.form.get("rollno")
    dob = request.form.get("dob")
    exists = utils.models.Student(rollno=rollno).get(rollno=rollno, dob=dob)
    if exists:
        session["id"] = exists.id
        session["rollno"] = exists.rollno
        return redirect(url_for("s_index"))
    flash("Student not found!")
    return redirect(url_for("index"))



@app.get("/admin_login")
def admin_login_get():
    
    ...

@app.post("/admin_login")
def admin_login_post():
    rollno = request.form.get("username")
    dob = request.form.get("dob")
    exists = utils.models.Student(rollno=rollno).get(rollno=rollno, dob=dob)
    if exists:
        session["id"] = exists.id
        session["rollno"] = exists.rollno
        return redirect(url_for("s_index"))
    flash("Student not found!")
    return redirect(url_for("index"))



@app.get("/register")
def register_get():
    return render_template("register.html")

@app.post("/register")
def register_post():
    rollno = request.form.get("username")
    dob = request.form.get("dob")
    exists = utils.models.Student(rollno=rollno).get(rollno=rollno, dob=dob)
    if exists:
        flash("Student not found!", 'error')
        return redirect(url_for("register_get"))
    created = utils.models.Student(rollno=rollno, dob=dob).create()
    session.clear()
    session["id"] = created.id
    session["rollno"] = created.rollno
    flash("Logged in!", 'message')
    return redirect(url_for("index"))


@app.get("/s")
def s_index():
    student = utils.models.Student(id=session["id"], rollno=session["rollno"])
    return render_template("s_index.html", student=student)


@app.get("/s/f")
def s_functions():
    student = utils.models.Student(id=session["id"], rollno=session["rollno"])
    functions = utils.image_matcher.get_user_functions(student)
    return render_template("s_functions.html", functions=functions)


@app.get("/s/f/<int:function_id>")
def s_function_view(function_id: int):
    student = utils.models.Student(id=session["id"], rollno=session["rollno"])
    function = utils.models.Function(id=function_id, name="", location="").get(id=function_id)
    if not function:
        return redirect(url_for("s_functions"))
    files_list = utils.image_matcher.match_images(student, function_id)
    return render_template("s_function_view", files_list=files_list, )


@app.get("/s/scanqr")
def s_scanqr_get():
    ...


@app.post("/s/scanqr")
def s_scanqr_post():
    function_id = request.form.get("function_id")
    student = utils.models.Student(id=session["id"], rollno=session["rollno"])
    function = utils.models.Function(id=function_id, name="", location="").get(id=function_id)
    if not function:
        return redirect(url_for("s_scanqr_get"))
    
    utils.models.Session(rollno=student.id).start(function.id)
    flash("Scanning successful!")
    return redirect(url_for("s_functions"))


@app.get("/a/f")
def a_functions():
    ...


@app.get("/a/f/create")
def a_function_create_get():
    admin = utils.models.Admin(id=session["id"]).get(id=session["id"])
    return render_template("a_function_create.html")

@app.post("/a/f/create")
def a_function_create_post():
    admin = utils.models.Admin(id=session["id"]).get(id=session["id"])
    name = request.form.get("name")
    location = request.form.get("location")
    start_on = request.form.get("start_on")
    end_on = request.form.get("end_on")
    created = utils.models.Function(name=name, location=location, start_on=start_on, end_on=end_on).create()
    flash(f"Function created! id: {created.id}", "message")
    return redirect(url_for("a_functions"))


@app.get("/a/f/<int:function_id>")
def a_function_view_get(function_id: int):
    admin = utils.models.Admin(id=session["id"]).get(id=session["id"])
    if not admin.get(id=admin.id):
        session.clear()
        flash("Admin not found!")
        return redirect(url_for("a_login"))
    
    function = utils.models.Function(id=function_id).get(id=function_id)
    function_sessions = utils.models.Session.get_all(function_id)
    return render_template("a_function_view.html", function=function, function_sessions=function_sessions)


# @app.post("/a/f/<int:function_id>")
# def a_function_view_post(function_id: int):
#     admin = utils.models.Admin(id=session["id"]).get(id=session["id"])
#     function = utils.models.Function(id=function_id).get(id=function_id)
    


@app.post("/a/f/<int:function>/delete")
def a_function_view_delete_post(function_id: int):
    admin = utils.models.Admin(id=session["id"]).get(id=session["id"])
    function = utils.models.Function(id=function_id).get(id=function_id)
    function.delete(function_id)
    flash("Function deleted!", "message")
    return redirect(url_for("a_functions"))


@app.post("/a/f/<int:function_id>/<int:session_id>/delete")
def a_function_session_delete(function_id: int, session_id: int):
    utils.models.Session(id=session_id).delete(function_id)
    return redirect(url_for("a_function_view_get", function_id=function_id))

@app.post("/a/f/<int:function_id>/<int:session_id>/end")
def a_function_session_stop(function_id: int, session_id: int):
    utils.models.Session(id=session_id).stop(function_id)
    return redirect(url_for("a_function_view_get", function_id=function_id))



if __name__ == "__main__":
    app.run(
        host = settings.HOST,
        port = settings.PORT
    )
