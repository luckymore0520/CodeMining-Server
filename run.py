#!flask/bin/python
from app import app,db,gl
db.create_all()
gl.auth()
app.run(host='0.0.0.0',port=8080,debug="True")
