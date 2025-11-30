import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import items
import re
import users


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query", "")
    if query:
        results = items.find_items(query)       
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)


@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    return render_template("show_item.html", item=item, classes=classes)




def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)


@app.route("/create_items", methods=["POST"])
def create_items():
    require_login()

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    author = request.form["author"]
    if not author or len(title) > 50:
        abort(403)
    

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0],parts[1]))
    
    #print(classes)
    #classes = request.form.getlist("classes")

    #section = request.form["section"]
    #if section:
    #    classes.append(("Osasto", section))
    #genre = request.form["genre"]
    #if genre:
    #    classes.append(("Laji", genre))
    
    description = request.form["description"]
    if len(title) > 500:
        abort(403)
    
    rate = request.form["rate"]
    if not rate:
        abort(403)    
    

    user_id = session["user_id"]
    items.add_item(title, author, description, rate, user_id, classes)
    return redirect("/")

#=====================
##ARVION MUOKKAAMINEN
#=====================

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





@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
    require_login()
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

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0],parts[1]))

    description = request.form["description"]
    if len(title) > 500:
        abort(403)
    
    rate = request.form["rate"]
    if not rate:
        abort(403)
    items.update_item(item_id, title, author, description, rate, classes)
    return redirect(f"/item/{item_id}")



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
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


#============
#REKSITERÖITYMINEN
#=============

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        return "VIRHE: kaikki kentät täytettävä"

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo luotu"

    return redirect("/login")


   # if password1 != password2:
   #     return "VIRHE: salasanat eivät ole samat"
   # 
    #try:
    #    users.create_user(username, password1)
    #except sqlite3.IntegrityError:
    #    return "VIRHE: tunnus on jo luotu"

    #return "tunnus luotu"


#-============
#KIRJAUTUMINEN
#=============
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]
    
    user_id = users.check_login(username, password)


   
#        if check_password_hash(password_hash, password):
#            session["user_id"] = user_id
#            session["username"] = username
#            return redirect("/")
#        else:
#            return "VIRHE: väärä tunnus tai salasana" 
    if not user_id:
        session.pop("user_id", None)
        session.pop("username", None)
        return render_template(
            "login.html",
            error="VIRHE: väärä tunnus tai salasana"
        )    
    session["user_id"] = user_id
    session["username"] = username
    return redirect("/")
#        else:
#            return "VIRHE: väärä tunnus tai salasana"



    #        session["user_id"] = user_id
    #        session["username"] = username
    #        return redirect("/")

    #if request.method == "POST":
    #    username = request.form["username"]
    #    password = request.form["password"]

    #    user_id = users.check_login(username, password)
    #    if user_id: 
    #        session["user_id"] = user_id
    #        session["username"] = username
    #        return redirect("/")




 #       sql = "SELECT id, password_hash FROM users WHERE username = ?"
 #       result = db.query(sql, [username])
#
#        if not result:
#            return "VIRHE: väärä tunnus tai salasana"

#        user_id = result[0][0]         
#        password_hash = result[0][1]  

#        if check_password_hash(password_hash, password):
#            session["user_id"] = user_id
#            session["username"] = username
#            return redirect("/")
#        else:
#            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


#KÄYTTÄJÄSIVUT

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)