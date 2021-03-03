from . import app
@app.route("/")
def root():
    global _current_frame
    print(current_frame.pretty_str())
    return str(current_frame) 


@app.route("/current_frame")
def route_current_frame():
    global _current_frame
    try:
        _current_frame
    except NameError:
        return "ERROR - Current Frame not initialized"
    else:
        return _current_frame.pretty_str()
    
@app.route("/route_variable_names/{var_type}")
def route_variable_names(var_type):
    if var_type=="bool":
        return _current_frame.bool_registers.keys()
    elif var_type=="int":
        return _current_frame.int_registers.keys()
    elif var_type=="float" or var_type == "real":
        return _current_frame.float_registers.keys()
    
@app.route("/add_variable/{key}/{value}")
def add_variable(key,value):
    global _current_frame
    try:
        _current_frame[key]=value
        return str(current_frame)
    except Exception as e:
        return e

@app.route("/update_variable/{key}/{value}")
def update_variable(key,value):
    global _current_frame
    try:
        _current_frame[key]=value
        return str(current_frame)
    except Exception as e:
        return e

@app.route("/delete_variable/{key}")
def delete_variable(key):
    global _current_frame
    return ("deleting variabl....")

@app.route("/export")
def export():
    global _current_frame
    _current_frame.save_to_json()


