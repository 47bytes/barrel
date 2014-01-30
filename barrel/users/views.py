#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, views, jsonify, Response
from werkzeug import check_password_hash, generate_password_hash
import peewee

from ..extensions import db, mail, login_manager, oid
from .models import User
#from app.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')

class UserListAPI(views.MethodView):
    """
    User
    / : get all user, create new user
    """
    def get(self):
        # get all user

        user_list = list()
        for user in User.select():
            user_list.append(user.serialize)

        return Response(json.dumps(user_list, indent=4), mimetype='application/json')

    def post(self):
        resp = request.get_json()
        avatar = resp.get('avatar')
        email = resp.get('email')
        username = resp.get('username')
        first_name = resp.get('first_name') or ''
        last_name = resp.get('last_name') or ''
        password = resp.get('password')
        gender = resp.get('gender') or ''


        user = User.create(
            avatar=avatar, 
            email=email, 
            first_name=first_name, 
            gender=gender,  
            last_name=last_name, 
            password=password,
            username=username,
            created=datetime.datetime.now(),
            last_login=datetime.datetime.now(),
            activated=False,
        )
        
        return Response(json.dumps(user.serialize), mimetype='application/json')

    def put(self, id=None):
        return Response(status=405)

    def delete(self, id=None):
        return Response(status=405)


# user_list: get all user, create user
mod.add_url_rule('/', view_func=UserListAPI.as_view('user_list'))