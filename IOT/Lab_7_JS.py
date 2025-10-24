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
    webpage = """
          <head>
      <style>
        input[type="range"]{
        transform: rotate(270deg);
        background:transparent;
        -webkit-appearance: none;
        appearance: none;
      }
    input[type="range"]::-webkit-slider-runnable-track {
      background: linear-gradient(to right, gray 0%, gray var(--rangeVal), #fff var(--rangeVal), #fff 100%);
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
    <div style="position:absolute; background-color: #99eeff; border: 2px solid #111; border-radius: 20px; display: table; height:90vh; width:90vw; right:2.5vw; box-shadow: 5px 5px 5px 5px #000000; text-align:center">
        <form id="form1" style="line-height: 20px; " action="" method="POST">
    <div style="position:absolute; left:5vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px; padding-top:5vh;">
    <span style="color: #ff0000; position: relative; height:10vh;">LED 1</span><br />
    <div style=" position:relative; height:65vh"></div>
    <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-left:-30vh; left:10vw;" id="slider1" name="slider1" type="range" value="""+f"{ledBrightness[0]}"+""" oninput="InputSlider(this,'l1')" onchange="SubmitForm()" />
      <br /><strong id="l1">0%</strong>
      </div>
    <div style="position:absolute; right:5vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px;padding-top:5vh;">
    <span style="color: #0000ff; position: relative; height:10vh;">LED 3</span><br />
    <div  style=" position:relative; height:65vh"></div>
    <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-right:-30vh; right:10vw;" id="slider3" name="slider3" type="range" value="""+f"{ledBrightness[2]}"+""" oninput="InputSlider(this,'l3')" onchange="SubmitForm()"/>
      <br /><strong id="l3">0%</strong>
    </div>
    <div style="position:absolute; right:35vw; height:80vh; width:20vw; background-color: #eeeeee; border-radius: 50px;padding-top:5vh;">
    <span style="color: #00ff00; position: relative; height:10vh;">LED 2</span><br />
    <div style=" position:relative; height:65vh"></div>
    <input style="position:absolute; top:35vh; height:10vh; width:60vh; margin-right:-30vh; right:10vw;" id="slider2" name="slider2" type="range" value="""+f"{ledBrightness[1]}"+""" oninput="InputSlider(this,'l2')" onchange="SubmitForm()"/>
      <br /><strong id="l2">0%</strong>
    </div>
    </form>
    <script>
        InputSlider(document.getElementById("slider1"),"l1");
        InputSlider(document.getElementById("slider2"),"l2");
        InputSlider(document.getElementById("slider3"),"l3");
        function InputSlider(inp,s) {
    inp.style.setProperty('--rangeVal',inp.value+"%");
    document.getElementById(s).textContent =inp.value+"%"
    }
    function SubmitForm(){
      document.getElementById("form1").submit();
    }
      </script>
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
    global ledBrightness
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',80))
    s.listen(3)
    while(True):
        conn, (connAdd,connPort) = s.accept()
        print([conn,connAdd,connPort])
        try:
            request =conn.recv(1024)
            data = parsePOSTdata(request)
            if len(data)>1:
                ledBrightness = [int(data['slider1']),int(data['slider2']),int(data['slider3'])]
                print(ledBrightness)
                for idx,b in zip(pwm,ledBrightness):
                  idx.ChangeDutyCycle(b)
            conn.send(b'HTTP/1.1 200 OK\nContent-type: text/html\nConnection: close\r\n\r\n')
            conn.sendall(bytes(GetWebpage(),'utf-8'))
            conn.close()
        except Exception as e:
            print(e)
            conn.close()
try:
    HandleWebPage()
except Exception as e:
    print(e)