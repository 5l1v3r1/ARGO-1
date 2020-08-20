import os
import platform
import socket
from datetime import date
import asyncio
import psutil
import requests
from fake_useragent import UserAgent
from flask import Flask, render_template,request
from flask_socketio import SocketIO
import subprocess
import dns.resolver
from cprint import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
version = str(0.1) + " beta"

@app.route('/')
def hello_world():
    cpux = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    return render_template("home.html", Cpu=cpux, Mem=ram.percent, date=date.today(), version=version)


@app.route("/start",methods=['GET','PORT'])
def start():
    #ua = UserAgent()
    global version
    if request.method == "POST":
        url = request.form['URL']
        print(url)
        startscan(url)
    try:
        ip = requests.get("https://ident.me").content.decode()
    except:
        ip = "127.0.0.1"
    osx = platform.platform()
    version = version
    distrox = socket.gethostname()
    user = os.environ['USER']
    return render_template("start.html", IP=ip, Useragent="Mozilla/5.0 (Windows NT 6.2)", os=osx, version=version,
                           distro=distrox, user=user)


def scanport(url):
    ip = ""
    socketio.emit('result', "~#Port_scanning_Starting...")
    socketio.emit('result', "~#Scanning 1 to 10000 port!...")
    try:
        unitest = url.replace("http://", "").replace("https://", "").split(":")[0]
        if unitest[:3].isdigit():
            ip = unitest
        else:
            new = dns.resolver.query(unitest, "A")
            for A in new:
                ip = str(A.to_text())
    except:
        pass
    if os.path.isfile("./resources/app/argoui/attack.py"):
        command = "python3 ./resources/app/argoui/attack.py " + ip + " " + url + " 2"
    else:
        command = "python3 ./argoui/attack.py " + ip + " " + url + " 2"
    openport = subprocess.check_output(command, shell=True)
    print(openport.decode())
    socketio.emit('result', str(removejunk(openport.decode())))

def scandns(url):
    ip = "127.0.0.1"
    try:
        unitest = url.replace("http://", "").replace("https://", "").split(":")[0]
        if unitest[:3].isdigit():
            ip = unitest
        else:
            new = dns.resolver.query(unitest, "A")
            for A in new:
                ip = str(A.to_text())
    except Exception as e:
        print(e)
    dnsresult = ""
    try:
        if os.path.isfile("./resources/app/argoui/attack.py"):
            command = "python3 ./resources/app/argoui/attack.py " + ip + " " + url + " 1"
        else:
            command = "python3 ./argoui/attack.py " + ip + " " + url + " 1"
        dnsresult = subprocess.check_output(command, shell=True).decode().split("\\\\n")
    except Exception as e:
        cprint.err(e)
        socketio.emit('result',str(e))
    print(dnsresult)
    for i in dnsresult:
        socketio.emit('result', str(removejunk(i)))

def removejunk(data):
    return data.replace("\n", "").replace("\n\n", "").replace("\t", "").replace("[0m","").replace("[92m","").replace("['","\n").replace("]","").replace(","," ").replace("[","\n").replace("\'\"","")

def startx(url):
    socketio.emit('result', "~#Dns Enum Starting...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scandns(url)
    scanport(url)

@socketio.on('startscan')
def startscan(data):
    if data["url"] == "":
        socketio.emit('result', "please enter a valid url!")
        return 0
    else:
        #threading.Thread(target=startx,args=(data["url"]))
        startx(data["url"])


@socketio.on('ready')
def handle_connected_event(data):
    if data["connected"]:
        print("connected")
    result = "~#ARGO is ready_ "
    socketio.emit('result', result)


if __name__ == '__main__':
    socketio.run(app, debug=True)
