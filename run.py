#!flask/bin/python
from app import app,db,gl
db.create_all()
gl.auth()
app.run(debug = True)
