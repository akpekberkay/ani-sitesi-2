from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anilar.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"

db = SQLAlchemy(app)


class Ani(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(200))
    not_yazi = db.Column(db.String(500))
    tarih = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        dosya = request.files["foto"]
        not_yazi = request.form["not"]
        tarih = request.form["tarih"]

        if dosya:

            yol = os.path.join(
                app.config["UPLOAD_FOLDER"],
                dosya.filename
            )

            dosya.save(yol)

            yeni_ani = Ani(
                foto=dosya.filename,
                not_yazi=not_yazi,
                tarih=tarih
            )

            db.session.add(yeni_ani)
            db.session.commit()

            return redirect("/")

    anilar = Ani.query.order_by(Ani.id.desc()).all()

    return render_template(
        "index.html",
        anilar=anilar
    )


@app.route("/sil/<int:id>")
def sil(id):

    ani = Ani.query.get(id)

    if ani:

        foto_yolu = os.path.join(
            app.config["UPLOAD_FOLDER"],
            ani.foto
        )

        if os.path.exists(foto_yolu):
            os.remove(foto_yolu)

        db.session.delete(ani)
        db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)