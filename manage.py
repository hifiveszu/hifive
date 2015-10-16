#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import sys

from flask_script import Manager, Server
from app import create_app
from app.core.models import User

if os.path.exists('etc/config'):
    with open('etc/config') as f:
        for line in f:
            name, value = line.strip().split('=')
            os.environ.setdefault(name, value)

app = create_app(os.environ.get('FLASK_ENV', 'default'))
manager = Manager(app)
manager.add_command('runserver', Server(use_debugger=True, use_reloader=True))


@manager.command
def create_user():
    print 'Create System Administrator Account'

    is_superuser = raw_input('is_superuser (Option, y or n): ')
    if is_superuser is 'y' \
            and User.objects.filter(is_superuser=True).first():
        print "superuser is exist"
        sys.exit(1)
    else:
        is_superuser = False

    is_manager = raw_input('is_manager (Option, y or n): ')
    if is_manager is 'y':
        is_manager = True
    else:
        is_manager = False

    is_staff = raw_input('is_staff (Option, y or n): ')
    if is_staff is 'y':
        is_staff = True
    else:
        is_staff = False

    user_name = raw_input('Username (Required): ')
    if not user_name:
        print 'username is required'
        sys.exit(1)
    if User.objects.filter(user_name=user_name).first():
        print 'username %s already exists'
        sys.exit(1)

    email = raw_input('Email (Required): ')
    if not email:
        print 'email is required'
        sys.exit(1)
    if User.objects.filter(email=email).first():
        print 'email %s already exists'
        sys.exit(1)

    phone = raw_input('Phone (Optional): ')

    password = raw_input('Password (Required): ')
    if not password:
        print 'password is required'
        sys.exit(1)
    password2 = raw_input('Confirm Password (Required): ')
    if password != password2:
        print 'Password not confirmed'
        sys.exit(1)

    obj = dict(
        user_name=user_name,
        password=password,
        email=email,
        phone=phone,
        is_superuser=is_superuser,
        is_manager=is_manager,
        is_staff=is_staff,
    )
    user = User.objects.create(**obj)
    user.change_password(password)
    user.save()

    print 'Account created. Please login and update your profile.'
    print user.to_json()


if __name__ == "__main__":
    manager.run()
