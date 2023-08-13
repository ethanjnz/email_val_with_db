from flask import flash, redirect, request, render_template
from flask_app.models.user import User
from flask_app import app


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/create")
def create_email():
    if not User.val_email(request.form):
        return redirect("/")

    potential_user = User.check_for_email(request.form["email"])
    if potential_user:
        flash("Email in use, Please try again.")
        return redirect("/")
    User.create(request.form)
    return redirect("/success")


@app.get("/success")
def display_info():
    users = User.get_all()
    return render_template("emails.html", users=users)


@app.route("/delete/<int:user_id>")
def delete(user_id):
    User.delete(user_id)
    return redirect("/success")
