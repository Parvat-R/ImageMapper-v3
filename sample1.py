from utils.models import Student, Admin, datetime

s = Student(id=-1, rollno=61781922102094, dob=datetime.datetime.now())
s.create_table()
# s.create()
print(s.get(rollno = 61781922102094))
s.delete()
print(s.get(rollno = 61781922102094))
