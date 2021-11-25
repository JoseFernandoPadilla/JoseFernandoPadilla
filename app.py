from flask import Flask, render_template, request #Importamos la clase de Flasck
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from werkzeug.utils import redirect

app = Flask(__name__) #cuando se crea y se ejecuta le asigna en automatico un identificador

#habilitando el uso del ORm en la app flask mediante el objeto "bd"
db = SQLAlchemy(app) 

#postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mzjietukrqkocq:b67f30b0ae3a008ceb0a4cd2e71b4ac43f42fde16ca144f63f5700f175de1088@ec2-52-86-193-24.compute-1.amazonaws.com:5432/d5n9q735ki5t9m'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Notas(db.Model):
    '''Clase Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self,tituloNota, cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota


@app.route('/') #te manda a la raiz del navegador
def index():
    objeto = {"nombre": "Fernando",
             "apellido" : "Padilla"}
    nombre = "Fernando"
    lista_nombres = ["Patricia", "fernando", "Marcelo"]
    return render_template("index.html", variable = lista_nombres)
    
@app.route("/about")
def about():
    return "Estas en la vista About"

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva = Notas(tituloNota=campotitulo, cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()
    return redirect("/leernotas")
    #return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo )
    #return "Nota creada" "" + campotitulo + "" + campocuerpo 

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo = nota.tituloNota
        cuerpo = nota.cuerpoNota
        print(nota.tituloNota)
        print(nota.cuerpoNota)

    return render_template("index.html", consulta = consulta_notas )

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota=int(id)).delete()
    print(nota)
    db.session.commit()
    return "Nota Eliminada"

@app.route("/editarnota/<id>")
def editar(id):
    nota = Notas.query.filter_by(idNota = int(id)).first()
    print(nota)
    print(nota.tituloNota)  
    print(nota.cuerpoNota)
    return render_template("modificaNota.html", nota = nota)

@app.route("/modificanota", methods=['POST'])
def modificarnota():
    idnota = request.form['idnota']
    nuevo_titulo = request.form['campotitulo']
    nuevo_cuerpo = request.form['campocuerpo']
    print("algo", nuevo_titulo, nuevo_cuerpo)
    print(idnota)
    nota = Notas.query.filter_by(idNota=int(idnota)).first()
    nota.tituloNota = nuevo_titulo
    nota.cuerpoNota = nuevo_cuerpo
    db.session.commit()
    return redirect("/leernotas")
    

if __name__ == "__main__":
    db.create_all()
    app.run()               #se le asigna etiqueta de principal
