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
    <h1 style="text-align: center; font-size: 40px;"><strong>Brightness Control</strong></h1>
    <form style="text-align: center; line-height:20px" action="/led" method="POST">
    <span style="text-decoration: underline;">Adjust Brightness</span>: <br />
    <input name="slider" type="range" value="range" /><br/><br/>
    <span style="text-decoration: underline;">Select LED</span>: <br />
    <input name="rG1" type="radio" value="0" /><span style="color: #ff0000;">LED 1</span> ({ledBrightness[0]}%)<br />
    <input name="rG1" type="radio" value="1" /><span style="color: #339966;">LED 2</span> ({ledBrightness[1]}%)<br />
    <input name="rG1" type="radio" value="2" /><span style="color: #00ccff;">LED 3</span> ({ledBrightness[2]}%)<br />
    <br/>
    <input type="submit" value="Apply Brightness" /></form>
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