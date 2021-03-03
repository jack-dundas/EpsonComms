from flask import Flask
import json
import os, subprocess, sys, time
from automation.epson import Frame
DEBUG_MODE = True


_current_frame = Frame.Frame()
server = None

def create_app():
    app=Flask("automation.epson")

    @app.route("/")
    def root():
        global _current_frame
        return str(_current_frame) 

    @app.route("/view")
    def route_current_frame():
        global _current_frame
        try:
            _current_frame
        except NameError:
            return "ERROR - Current Frame not initialized"
        else:
            # html = [_current_frame.pretty_str(), ]
            return _current_frame.pretty_str()
        
    @app.route("/add_variable/{key}/{value}")
    def add_variable(key,value):
        global _current_frame
        try:
            _current_frame[key]=value
            _current_frame.save_to_json()
            return "ok"
        except Exception as e:
            return e

    @app.route("/update_variable/<key>/<value>")
    def update_variable(key,value):
        global _current_frame
        try:
            if isinstance(value, str):
                value=eval(value) #string to type conversion, dangerous and quick! 
            msg = _current_frame.__setitem__(key,value,update=True)
            _current_frame.save_to_json()
            return "ok:\t"+msg
        except Exception as e:
            return str(e)

    @app.route("/update_variables/<variables_dict>")
    def update_dict(variables_dict):
        try:
            variables_dict = eval(variables_dict)
            for k,v in variables_dict.items():
                update_variable(k,v)
            return "ok"
        except Exception as e:
            return "Error during dictionary upload of {k}[{v}]: {}".format(k,v,e)
        
    
    @app.route("/delete_variable/<key>")
    def delete_variable(key):
        global _current_frame
        try:
            del _current_frame[key]
            _current_frame.save_to_json()
            return _current_frame.comm_str()
        except Exception as e:
            return str(e)
        
    @app.route("/keys")
    def get_keys():
        global _current_frame
        return ",".join(_current_frame._keys())

    return app

def start_server():
    global server
    os.environ["FLASK_APP"]="automation.epson:create_app()"
    os.environ["FLASK_ENV"]="development"
    os.environ["FLASK_DEBUG"]="1"
    server = subprocess.Popen(["python","-m","flask","run"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("starting server")
    #delay to let server start up, this should be improved.....
    for i in range(10):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(.2)
    print("done")
    
def stop_server():
    server.kill()
