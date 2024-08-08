import os
import datetime
import sqlite3
from pydantic import BaseModel
import settings


def session_sql_path(function_id: int):
    return os.path.join(settings.DATABASE_ROOT, "sessions", f"f{function_id}.sqlite3")

def get_function_images(function_id: int):
    return os.listdir(
        os.path.join(settings.STORAGE_ROOT, f"{function_id}")
    )

class DBModel(BaseModel):
    id: int = -1

    def create(self):
        table_name = self.__class__.__name__
        columns = list(self.model_dump(exclude={"id"}).keys())
        column_values = list(self.model_dump(exclude={"id"}).values())
        column_filler = ', '.join(columns)
        value_filler = ', '.join(['?']*len(column_values))
        query = f"insert into {table_name} ({column_filler}) values ({value_filler})"
        db = sqlite3.connect(settings.DATABASE_FILE)
        db.execute(query, column_values)
        db.commit()
        db.close()
        return self

    
    def get(self, **kwargs):
        table_name = self.__class__.__name__
        query = f"select * from {table_name} where {' = ? and '.join(kwargs.keys())} = ?"
        db = sqlite3.connect(settings.DATABASE_FILE)
        result = db.execute(query, list(kwargs.values()))
        row = result.fetchone()
        db.close()
        if row:
            columns = list(self.model_fields.keys())
            return self.model_construct(self.model_fields_set, **dict(zip(columns, row)))
        return None
    
    def update(self, **kwargs):
        table_name = self.__class__.__name__
        db = sqlite3.connect(settings.DATABASE_FILE)
        column_list = ' = ? , '.join(kwargs.keys()) + " = ?"
        value_list = tuple(kwargs.values())
        id_value = self.id
        query = f"update {table_name} set {column_list} where id = ?"
        db.execute(query, (value_list, id_value))
        db.commit()


    def delete(self, id: int = -1):
        id = id if id != -1 else self.id
        table_name = self.__class__.__name__
        query = f"delete from {table_name} where id = ?"
        print(query.replace("?", str(id)))
        db = sqlite3.connect(settings.DATABASE_FILE)
        db.execute(query, [id])
        db.commit()
        db.close()

class Student(DBModel):
    rollno: int
    dob: datetime.datetime = datetime.datetime.now()

    def create_table(self):
        table_name = self.__class__.__name__
        db = sqlite3.connect(settings.DATABASE_FILE)
        db.execute(f"create table if not exists {table_name} (id integer primary key, rollno integer unique, dob date)")
        db.commit()
        db.close()

class Admin(DBModel):
    username: str
    dob: datetime.datetime

    def create_table(self):
        table_name = self.__class__.__name__
        db = sqlite3.connect(settings.DATABASE_FILE)
        db.execute(f"create table if not exists {table_name} (id integer primary key, username text unique, dob date)")
        db.commit()
        db.close()


class Session(BaseModel):
    id: int = -1
    rollno: int
    start_time: datetime.datetime | None = None
    stop_time: datetime.datetime | None = None
    
    def create_table(self, function_id: int):
        db = sqlite3.connect(session_sql_path(function_id))
        db.execute(f"create table if not exists Sessions (id integer primary key, rollno integer, start_time date, stop_time date)")
        db.commit()
        db.close()
    
    
    def get_previous_start_time(self, function_id, id=-1):
        id = id if id != -1 else self.id
        db = sqlite3.connect(session_sql_path(function_id))
        result = db.execute(f"select start_time from Sessions where id < ? order by id desc limit 1", (id,))
        row = result.fetchone()
        db.close()
        if row:
            return row[0]
        return datetime.datetime.now()

    def start(self, function_id: int):
        self.start_time = self.get_previous_start_time(function_id)
        db = sqlite3.connect(session_sql_path(function_id))
        db.execute(f"insert into Sessions (rollno, start_time) values (?, ?)", (self.rollno, self.start_time))
        db.commit()
        db.close()

    def stop(self, function_id: int):
        db = sqlite3.connect(session_sql_path(function_id))
        db.execute(f"update Sessions set stop_time = ? where id = ?", (self.stop_time, self.id))
        db.commit()
        db.close()

    def delete(self, function_id: int):
        db = sqlite3.connect(session_sql_path(function_id))
        db.execute(f"delete from Sessions where id = ?", (self.id,))
        db.commit()
        db.close()
    
    @staticmethod
    def get_all(function_id: int):
        db = sqlite3.connect(session_sql_path(function_id))
        result = db.execute("select * from Sessions")
        rows = result.fetchall()
        db.close()
    
        session_list = []
        for row in rows:
            session_instance = Session(id=row[0], rollno=row[1], start_time=row[2], stop_time=row[3])
            session_list.append(session_instance)    
        
        return session_list
    
    def get_with_roll(self, function_id: int):
        db = sqlite3.connect(session_sql_path(function_id))
        result = db.execute("select * from Sessions where rollno = ?", (self.rollno,))
        rows = result.fetchall()
        db.close()
        session_list = []
        for row in rows:
            session_instance = Session(id=row[0], rollno=row[1], start_time=row[2], stop_time=row[3])
            session_list.append(session_instance)    
        
        return session_list


class Function(DBModel):
    name: str
    location: str
    start_on: datetime.datetime = datetime.datetime.now()
    end_on: datetime.datetime
    
    def create_table(self):
        table_name = self.__class__.__name__
        db = sqlite3.connect(settings.DATABASE_FILE)
        db.execute(f"create table if not exists {table_name} (id integer primary key, name text, location text, start_on date, end_on date)")
        db.commit()
        db.close()
