from flask import Flask, render_template, Response


app = Flask(__name__)


from . import server