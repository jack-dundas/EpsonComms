import requests

variables_dict={
    "estop":False,
    "speed":100,
    "accel":200,
    "waypoint_1":12.52,
    "recipe_1":True,
    "recipe_2":False,
    "recipe_3":False,
    "waypoint_2":1125.2519523,
    "waypoiny_3":135.0,
    "start_flag":False
}
res = requests.get("http://127.0.0.1:5000/update_variables/{variables}".format(variables=variables_dict))

print(res.text)