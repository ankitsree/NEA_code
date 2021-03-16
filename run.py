from flask_program import app,db

if __name__ == '__main__':#if this is the file is the main file then run the code below
    db.create_all()
    app.run(debug=True)
