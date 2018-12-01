# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request,render_template,send_file
import sys,os
app = Flask(__name__)
@app.route('/')
def root():
        return "Hello World"
