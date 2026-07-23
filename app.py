from flask import Flask, render_template, request, redirect, send_from_directory
import qrcode
import os

DATA_PATH = "./data"

def get_latest():
    fpath = DATA_PATH + "/latest"
    if not os.path.isfile(fpath):
        return 1
    with open(DATA_PATH + "/latest", "r") as f:
        return int(f.read())

def update_latest(idx):
    with open(DATA_PATH + "/latest", "w") as f:
        f.write(str(idx + 1))

app = Flask(__name__)

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
            print(request.form)
            # TODO тут ошибка 
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
        img.save(DATA_PATH + f"/{latest_idx}.png")
        update_latest(latest_idx)
        return redirect(f"/view/{latest_idx}")

@app.route("/view/<id>")
def view(id):
    fpath = DATA_PATH + f"/{id}.png"
    if not os.path.isfile(fpath):
        # TODO тут ошибка
        return redirect("/")
    return render_template("view.html", fpath=f"{id}.png", id=id)

@app.route("/data/<path:filename>")
def get_file(filename):
    return send_from_directory(DATA_PATH, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)