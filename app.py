from flask import Flask, render_template, request, redirect, flash
import requests
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
config = json.load(open('config.json'))
app.secret_key = "secret"
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["80 per hour"],
    storage_uri="memory://",
)


@app.route('/new', methods=['POST'])
@limiter.limit("1/day")
def new():
    endpoint = config['endpoint']
    token = config['token']
    domain = config['domain']
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': token
    }
    if name == "":
        name = email
    payload = {
        "active": "1",
        "domain": domain,
        "local_part": email,
        "name": name,
        "password": password,
        "password2": password,
        "quota": "512",
        "force_pw_update": "0",
        "tls_enforce_in": "1",
        "tls_enforce_out": "1",
    }

    r = requests.post(endpoint + "/api/v1/add/mailbox", headers=headers, json=payload)
    if r.status_code == 200:
        return redirect(endpoint + "/SOGo/", code=302)
    else:
        flash("Error: " + r.text)
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ip=request.remote_addr, domain=config['domain'], xconnecting = request.headers.get('X-Connecting-IP'))
