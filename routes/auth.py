from flask import Blueprint, render_template, request, redirect
from validators.auth_validator import (username_validator, password_validator)
from services.auth_service import register_user_service, login_user_service
from flask_jwt_extended import set_access_cookies
auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_vali_error = username_validator(username)
        pass_vali_error = password_validator(password)
        if user_vali_error:
            return user_vali_error
        if pass_vali_error:
            return pass_vali_error
        service_error = register_user_service(username, password)
        if service_error:
            return service_error
        return redirect("/login")
    return render_template("register.html")
        
@auth.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_vali_error = username_validator(username)
        pass_vali_error = password_validator(password)
        if user_vali_error:
            return user_vali_error
        if pass_vali_error:
            return pass_vali_error
        token, service_error = login_user_service(username, password)
        if service_error:
            return service_error
        response = redirect("/chat")
        set_access_cookies(response, token)
        return response
    return render_template("login.html")

