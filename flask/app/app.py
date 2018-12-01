# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request,render_template,send_file
import sys,thread,string,random, sqlite3,urllib,base64,hashlib,os
app = Flask(__name__)
