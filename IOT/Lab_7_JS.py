import socket
import RPi.GPIO as GPIO
ledBrightness = [0,0,0]
GPIO.setmode(GPIO.BCM)
pins = [4,17,27]
pwm = []
for i in pins:
    GPIO.setup(i,GPIO.OUT,initial=1)
    nPwm = GPIO.PWM(i,500)
    nPwm.start(0.0)
    pwm.append(nPwm)
def GetWebpage():
    webpage = f"""
      <head>
        <style>
          input[type="range"]{
          transform: rotate(270deg);
          background:transparent;
          -webkit-appearance: none;
        }
        
      input[type="range"]::-webkit-slider-runnable-track {
        background: linear-gradient(to right, gray 0%, gray 50%, #fff 50%, #fff 100%);
        height: 5vw;
        width: 10vh;
      }
          
        input[type="range"]::-webkit-slider-thumb {
          background-color: gray;
          margin-top:-2.5vw;
          height:10vw;
          width: 2vh;
          border-radius: 2vh;
          -webkit-appearance: none;
        }
        </style>
      </head>
      <h1 style="text-align: center; font-size: 40px; height:5vh;"><strong>Brightness Control</strong></h1>
      <div style="position:absolute; background-color: #99eeff; border: 2px solid #111; border-radius: 20px; display: table; height:90vh; width:90vw; right:2.5vw; box-shadow: 5px 5px 5px 5px #000000; text-align:center"><form style="line-height: 20px; " action="/led" method="POST"><span style="text-decoration: underline;">Adjust Brightness</span>: <br />
      <div style="position:absolute; left:5vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px; padding-top:5vh;">
      <span style="color: #ff0000; postion: relative; height:10vh;">LED 1</span><br />
      <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-left:-30vh; left:10vw" name="slider" type="range" value="range" />
      <div style="hidden: true; position:relative; height:65vh"></div>
        <br />{ledBrightness[0]}%
        </div>
      <div style="position:absolute; right:5vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px;padding-top:5vh;">
      <span style="color: #0000ff; postion: relative; height:10vh;">LED 3</span><br />
      <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-right:-30vh; right:10vw;" name="slider" type="range" value="range" />
      <div style="hidden: true; position:relative; height:65vh"></div>
        <br />{ledBrightness[0]}%
      </div>
      <div style="position:absolute; right:35vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px;padding-top:5vh;">
      <span style="color: #0000ff; postion: relative; height:10vh;">LED 3</span><br />
      <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-right:-30vh; right:10vw;" name="slider" type="range" value="range" />
      <div style="hidden: true; position:relative; height:65vh"></div>
        <br />{ledBrightness[0]}%
      </div>
      </form>
    """
    return webpage
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find(b'\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split(b'&')
    for pair in data_pairs:
        key_val = pair.split(b'=')
        if len(key_val) == 2:
            data_dict[str(key_val[0],'utf-8')] = key_val[1]
    return data_dict

def HandleWebPage():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',80))
    s.listen(1)
    while(True):
        conn, (connAdd,connPort) = s.accept()
        try:
            request =conn.recv(1024)
            data = parsePOSTdata(request)
            if len(data)>1:
                idx = int(data['rG1'])
                ledBrightness[idx] = int(data['slider'])
                print(ledBrightness)
                pwm[idx].ChangeDutyCycle(ledBrightness[idx])
            conn.send(b'HTTP/1.1 200 OK\nContent-type: text/html\nConnection: close\r\n\r\n')
            conn.sendall(bytes(GetWebpage(),'utf-8'))
            conn.close()
        except:
            conn.close()
try:
    HandleWebPage()
except Exception as e:
    print(e)