#!flask/bin/python
from app import app,gl
gl.auth()
app.run(host='0.0.0.0',port=8080,debug="True")
