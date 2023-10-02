# read_sensor function returns sensor temperature and humidity
def read_sensor():
    global temp, hum
    temp = hum = 0

    try:
      sensor.measure()
      temp = sensor.temperature()
      hum = sensor.humidity()
      if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
        res = ('{0},{1}'.format(temp, hum))
        return (res)
      else:
        return ('Invalid sensor readings.')
    except OSError as e:
        return ('Failed to read sensor.')

# web_page function returns HTML page
def web_page():
  if temp >= 25:
      LED.on()
      LED_state = "ON"
  else:
      LED.off()
      LED_state = "OFF"

  html = """<!DOCTYPE html>
  <html>
  <head><meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
      html {font-family: Arial;display: inline-block;margin: 0px auto;text-align: center;}
      h1 { font-size: 3.0rem; }
      p { font-size: 3.0rem; }
      .units { font-size: 1.2rem; }
      .dht-labels{font-size: 1.5rem;vertical-align:middle;padding-bottom: 15px;}
      .led-labels{font-size: 1.5rem;vertical-align:middle;padding-bottom: 15px;}
  </style>
  <script>
      setInterval(loadDoc,5000)
      function loadDoc() {
          var xhttp = new XMLHttpRequest()
          xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200){ 
                    document.getElementById(\"webpage\").innerHTML =this.responseText}
          }
          xhttp.open(\"GET\", \"/\", true)
          xhttp.send()
      }
  </script>
  </head>
  <body>
  <div id=\"webpage\">
      <h1>ESP8266 DHT Server</h1>
      <p>
        <span class="dht-labels">Temperature: </span> 
        <span>""" + str(temp) + """</span>
        <sup class="units">&deg;C</sup>
      </p>
      <p> 
        <span class="dht-labels">Humidity: </span>
        <span>""" + str(hum) + """</span>
        <sup class="units">%</sup>
      </p>
      <p> 
        <span class="led-labels">LED state: </span>
        <span>""" + str(LED_state) + """</span>
      </p>
  </div>
  </body>
  </html>"""
  return html


# create a socket object named s on ESP8266
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((hostname/IP address/empty string, PORT))
# '' empty string refers to the server will accept connections on all available IPv4 interfaces.
s.bind(('', 80))
# It makes a listening socket with the maximum number of queued connections is 5
s.listen(5)

# start to listen requests and send responses
while True:
  # accept connections
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  # The data exchange between the client and server using the send() and recv() methods
  # recv method specifies the maximum data that can be received at once.
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  print(read_sensor())
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
