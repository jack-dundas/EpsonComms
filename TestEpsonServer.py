import automation.epson, automation.epson.Frame
import requests
import time, os, random



if __name__ == "__main__":
    
    print("-"*20)    
    automation.epson.start_server()
    print("-"*20)      
    
    
    try:
        
        for i in range(100):
            keys = requests.get("http://127.0.0.1:5000/keys")
            
            #get a random key and a random value
            key = random.choice(keys.text.split(","))
            val = random.choice([*range(10), *[True]*5, *[False]*5, *[x * 0.1 for x in range(0, 10)]])
            input("Press Enter to send {key}[{val}]...".format(key=key, val=val))
            
            res = requests.get("http://127.0.0.1:5000/update_variable/{key}/{val}".format(key=key, val=val)).text            
            print(res)
            print("-"*20 + "\n")
            time.sleep(1)
        print("Exiting")

    finally:
        automation.epson.stop_server()