import sqlite3
import secrets

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import config
import items
import users


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    token = request.form.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        abort(403)

def ensure_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

#==========
#KIRJAT
#==========
#Kirjat: lisää
@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_items", methods=["POST"])
def create_items():
    require_login()
    check_csrf()
    if "user_id" not in session:
        return redirect("/login")
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    author = request.form["author"]
    if not author or len(title) > 50:
        abort(403)
    all_classes = items.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    description = request.form["description"]
    if len(title) > 500:
        abort(403)
    rate = request.form["rate"]
    if not rate:
        abort(403)
    user_id = session["user_id"]
    item_id = items.add_item(title, author, description, rate, user_id, classes)
    return redirect(f"/item/{item_id}")

#Kirjat: muokkaa
@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes = items.get_all_classes()
    classes = {}
    for my_class in classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]
    return render_template("edit_item.html", item=item, classes=classes, all_classes=all_classes)

#Kirjat: päivitä
@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
    require_login()
    check_csrf()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    author = request.form["author"]
    if not author or len(title) > 50:
        abort(403)
    all_classes = items.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    description = request.form["description"]
    if len(title) > 500:
        abort(403)
    rate = request.form["rate"]
    if not rate:
        abort(403)
    items.update_item(item_id, title, author, description, rate, classes)
    return redirect(f"/item/{item_id}")

#Kirjat: poista
@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        return redirect("/item/" + str(item_id))
    return redirect("/item/" + str(item_id))

#Kirjat: näytä
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    comments_average = items.get_comments_average(item_id)
    images = items.get_images(item_id)
    return render_template(
        "show_item.html",
        item=item,
        classes=classes,
        comments=comments,
        comments_average=comments_average,
        images=images
    )

##KUVAT##
@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    images = items.get_images(item_id)
    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    file = request.files["image"]
    if not file.filename.endswith(".png"):
        return "VIRHE: väärä tiedostomuoto"
    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"
    items.add_image(item_id, image)
    return redirect("/images/" + str(item_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

#Kirjat: etsi
@app.route("/find_item")
def find_item():
    query = request.args.get("query", "")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

#Kirjat: kommentoi
@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()
    if "user_id" not in session:
        return redirect("/login")
    comment = request.form["comment"]
    if len(comment) > 500:
        abort(403)
    rate = int(request.form["rate"])
    if rate < 1 or rate > 5:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]
    if user_id == item["user_id"]:
        flash("Et voi kommentoida omaa kirjaa")
        return redirect("/item/" + str(item_id))
    try:
        items.create_comment(item_id, user_id, rate, comment)
    except sqlite3.IntegrityError:
        flash("Olet jo kommentoinut tämän kirjan")
        return redirect("/item/" + str(item_id))
    return redirect("/item/" + str(item_id))

@app.route("/remove_comment/<int:comment_id>", methods=["POST"])
def remove_comment(comment_id):
    require_login()
    check_csrf()
    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    item = items.get_item(comment["item_id"])
    if not item:
        abort(404)
    user_id = session["user_id"]
    if user_id not in (comment["user_id"], item["user_id"]):
        abort(403)
    items.remove_comment(comment_id)
    return redirect("/item/" + str(comment["item_id"]))

@app.route("/edit_comment/<int:comment_id>")
def edit_comment(comment_id):
    require_login()
    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)
    item = items.get_item(comment["item_id"])
    if not item:
        abort(404)
    return render_template("edit_comment.html", comment=comment, item=item)

@app.route("/update_comment/<int:comment_id>", methods=["POST"])
def update_comment(comment_id):
    require_login()
    check_csrf()
    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)
    new_comment = request.form["comment"]
    if len(new_comment) > 500:
        abort(403)
    rate = int(request.form["rate"])
    if rate < 1 or rate > 5:
        abort(403)
    items.update_comment(comment_id, rate, new_comment)
    return redirect("/item/" + str(comment["item_id"]))

#==========
#KÄYTTÄJÄ
#==========
#Käyttäjä: rekisteröityminen
@app.route("/register")
def register():
    ensure_csrf_token()
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username or not password1 or not password2:
        flash("VIRHE: Kaikki kentät täytettävä")
        return redirect("/register")
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat")
        return redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo luotu")
        return redirect("/register")
    flash("Tunnus luotu onnistuneesti")
    return redirect("/login")

#Käyttäjä: kirjautuminen
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        ensure_csrf_token()
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        flash("VIRHE: Väärä tunnus tai salasana")
        return redirect("/login")
    return redirect("/login")

#Käyttäjä: uloskirjautuminen
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

#Käyttäjä: näytä
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)
