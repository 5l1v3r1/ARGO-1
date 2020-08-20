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

def getip(url):
    ip = "127.0.1.7"
    try:
        unitest = url.replace("http://", "").replace("https://", "").replace("/","").split(":")[0]
        if unitest[:3].isdigit():
            ip = unitest
        else:
            new = dns.resolver.query(unitest, "A")
            for A in new:
                return str(A.to_text())
    except Exception as e:
        socketio.emit('result', "~#Error " + str(e))
    if ip == "127.0.1.7":
        try:
            return socket.gethostbyname(unitest)
        except Exception as e:
            print(e)

def generatecommand(ip,url, num):
    if os.path.isfile("./resources/app/argoui/attack.py"):
        return "python3 ./resources/app/argoui/attack.py " + ip + " " + url + " " + str(num)
    elif os.path.isfile("./argoui/attack.py"):
        return "python3 ./argoui/attack.py " + ip + " " + url + " " + str(num)
    else:
        return "python3 ./attack.py " + ip + " " + url + " " + str(num)

def webanalizer(ip,url):
    socketio.emit('result', "~#Starting web analizer...")
    command = generatecommand(ip,url,3)
    data = subprocess.check_output(command, shell=True).decode().split("\\n\\t")
    for i in data:
        print(i)
        socketio.emit('result', str(removejunk(i)).replace("\n\t","\n").replace("(","").replace("'')","") + "\n")

def fuzz(ip,url):
    socketio.emit('result', "~#Start fuzzing...")
    command = generatecommand(ip, url, 4)
    data = subprocess.check_output(command, shell=True).decode().split("\\n\\t")
    for i in data:
        socketio.emit('result', str(removejunk(i).replace(">","")))

def scanport(ip,url):
    socketio.emit('result', "~#Port_scanning_Starting...")
    socketio.emit('result', "~#Scanning 1 to 10000 port!...")
    command = generatecommand(ip,url,2)
    openport = subprocess.check_output(command, shell=True).decode().split("\n")
    idata = ""
    x = 1
    for i in openport:
        if x == 2:
            idata = ""
            socketio.emit('result', "~#OPEN PORT  >>>	")
        socketio.emit('resultNO', " " +   str(removejunk(i)))
        x = x + 1

def scandns(ip,url):
    socketio.emit('result', "~#Dns Enum Starting...")
    dnsresult = ""
    try:
        command = generatecommand(ip,url,1)
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ip = getip(url)
    webanalizer(ip,url)
    scandns(ip,url)
    scanport(ip, url)
    fuzz(ip,url)

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
