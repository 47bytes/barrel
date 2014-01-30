#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import hmac
import random
import os
import string

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/home/rt/devel/python/barrel/barrel/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Form validation

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16

AGE_MIN = 1
AGE_MAX = 300

DEPOSIT_MIN = 0.00
DEPOSIT_MAX = 9999999999.99

# Sex type.
MALE = 1
FEMALE = 2
OTHER = 9
SEX_TYPE = {
    MALE: u'Male',
    FEMALE: u'Female',
    OTHER: u'Other',
}

# Model
STRING_LEN = 64


def rstr(length=5, special_chars=True, numbers=True, upper_case=True):
    chars_lower = 'a b c d e f g h i j k l m n o p q r s t u v w x y z '
    n = '1 2 3 4 5 6 7 8 9 0 '
    special = '! $ % & / ( ) * + - _ < > = ? # '

    chars = chars_lower
    if upper_case:
        chars += chars_lower.upper()
    if numbers:
        chars += n
    if special_chars:
        chars += special

    chars = chars.split()
    val = list()
    for i in range(length):
        val.append(chars[random.randint(0, len(chars)-1)])
    return ''.join(val)

def salt(length=10, digestmod=hashlib.md5):
    rnd = rstr(length=length)
    h = hmac.new(rnd, digestmod=digestmod)
    return h.hexdigest()


def get_current_time():
    return datetime.datetime.utcnow()


def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_AVATAR_EXTENSIONS


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as err:
        raise err
