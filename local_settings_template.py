# -*- encoding: utf-8 -*-

import os

CURDIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_APPS_PATH = os.path.normpath(os.path.join(CURDIR,'..','apps')) 

ADMINS = (
        ('me', 'me@home.net')
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'db_name'             # Or path to database file if using sqlite3.
DATABASE_USER = 'me'             # Not used with sqlite3.
DATABASE_PASSWORD = 'passw0rd'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TEST_DATABASE_CHARSET = 'utf8'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'WhatANiceSecretKey'
