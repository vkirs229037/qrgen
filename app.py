from flask import Flask, render_template, request, redirect, send_from_directory, flash
import qrcode
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("settings.py")
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("expected environment variable SECRET_KEY to be set")
app.secret_key = secret_key

def get_latest():
    fpath = app.config["DATA_PATH"] + "/latest"
    if not os.path.isfile(fpath):
        return 1
    with open(app.config["DATA_PATH"] + "/latest", "r") as f:
        return int(f.read())

def update_latest(idx):
    with open(app.config["DATA_PATH"] + "/latest", "w") as f:
        f.write(str(idx + 1))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create", methods=["POST"])
def create():
    if request.method == "POST":
        content = request.form.get("content")
        if not content:
            flash("Содержимое не может быть пустым")
            return redirect("/")
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=15,
            border=4
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        latest_idx = get_latest()
        img.save(app.config["DATA_PATH"] + f"/{latest_idx}.png")
        update_latest(latest_idx)
        return redirect(f"/view/{latest_idx}")

@app.route("/view/<id>")
def view(id):
    fpath = app.config["DATA_PATH"] + f"/{id}.png"
    if not os.path.isfile(fpath):
        return render_template("notfound.html"), 404
    return render_template("view.html", fpath=f"{id}.png", id=id)

@app.route("/data/<path:filename>")
def get_file(filename):
    return send_from_directory(app.config["DATA_PATH"], filename, as_attachment=True)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Страница не найдена!", code=404)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", error="Произошла внутренняя ошибка сервера", code=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)