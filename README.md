#Epson Communciation Protocol

This package creates a minimal python server for sending and receiving messages to the epson controller. 
The minimal starting code is as follows:
'''
import automation.epson
automation.epson.start_server()
try:
    # do stuff
finally:
    automation.epson.stop_server()
'''
this will launch a server on 127.0.0.1:5000
For production use, the root url will  provide all the info according to the agreed upon messaging format
For development use/debug use, a descriptive representation is provided at [127.0.0.1:5000/view](http://127.0.0.1:5000/view)

![alt text](https://github.com/jack-dundas/EpsonComms/blob/master/DebugView.png?raw=true)

To run:
1. clone this repo onto your laptop
1. a virtual env is provided for quick setup -> try '''source venv/scripts/activate'''
1. To launch the server, run '''python TestEpsonServer.py'''
1. The current saved message can be viewed by opening up [127.0.0.1:5000/view](http://127.0.0.1:5000/view) on your browser
1. The communication string that will be read by Epson can be viewed by opening up [127.0.0.1:5000/](http://127.0.0.1:5000/) on your browser
1. '''TestEpsonServer.py''' will attempt to set variables to random values, returning success messages if they were successful, and descriptive error messages if not. 



email me @jack.dundas@vention.cc with any questions!