import os

# Flask and some of its extensions use the value of the secret key as
# a cryptographic key, useful to generate signatures or tokens. The Flask-WTF
# extension uses it to protect web forms against a nasty attack called
# Cross-Site Request Forgery or CSRF

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-do-you-?'