import os
import sqlite3
import datetime
from typing import List
import settings
from . import models
from pathlib import Path

def user_in_function(student: models.Student, function_id):
    session_files = os.listdir(settings.SESSION_ROOT)
    expected_fname = models.session_sql_path(function_id)

    if expected_fname.split("/")[-1] not in session_files:
        return False

    db = sqlite3.connect(expected_fname)
    result = db.execute("select * from Session where rollno = ?", [student.rollno])
    res = result.fetchall()
    db.close()
    print(res)
    ss = []
    if res:
        for i in res:
            ss.append(models.Session(id = i[0], rollno=i[1], start_time=i[2], stop_time=i[3]))
        return ss

    return False


def get_user_functions(student: models.Student):
    session_files = os.listdir(settings.SESSION_ROOT)
    functions: List[models.Function] = []
    for session_file in session_files:
        db = sqlite3.connect(os.path.join(settings.SESSION_ROOT, session_file))
        result = db.execute("select * from Session where rollno = ?", [student.rollno])
        res = result.fetchone()
        if res:
            function_id = int(session_file.replace("f", "").split(".")[0])
            function = models.Function(id=function_id).get(id=function_id)
            functions.append(function)
    
    return functions

def match_images(student: models.Student, function_id: models.Function):
    user_sessions: List[models.Session] = user_in_function(student, function_id)

    if not user_sessions:
        return []

    function_images = models.get_function_images(function_id)
    matched_images = []

    for sessions in user_sessions:
        for image_file_name in function_images:
        # print(fname)
            if image_file_name.startswith("ct-"):
                # image file name pattern:
                # ct-<taken_date>_<taken_time>-<image_number>.jpeg
                true_name = Path(image_file_name).stem
                created_time = datetime.datetime.strptime(
                    true_name.replace("ct-", "").split(".")[0], "%Y_%m_%d_%h_%m_%S"
                )
            
                if created_time and (
                    sessions.start_time <= created_time and
                    created_time <= sessions.stop_time
                ):
                    matched_images.append(image_file_name)

    return matched_images
