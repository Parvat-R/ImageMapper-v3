from flask import (
    render_template, redirect, url_for, 
    session, send_file, abort, Flask,
    request, flash, get_flashed_messages
)
import settings

app = Flask(__name__)


@app.get("/")
def index():
    ...



@app.get("/login")
def login_get():
    ...

@app.post("/login")
def login_post():
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
def s_function_view():
    ...


if __name__ == "__main__":
    app.run(
        host = settings.HOST,
        port = settings.PORT
    )
