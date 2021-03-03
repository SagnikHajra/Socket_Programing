# Key-Value Storage System
A Server, proxy server and a client interaction implemented via python socket programming with storing at server, caching at proxy server and updating the cache every 60 sec based on Pricipal of Locality.
## Description
This project introduces the concept of client/server architecture and caching. Task is to create a simple web and proxy server that stores and retrieves key-value pairs using socket programming interface. The server only permits commands such as GET, PUT, and DUMP in the request field followed by the key and value stored. GET returns the value of the key specified, PUT stores the key and a specified value on the server and DUMP lists all of the key value pairs contained in the server. When the client makes a GET request, this request is passed through the proxy server. If the server has made the same request using the same key, the key-value should be retrieved from the proxy server instead of the server. An example of commands are below(commands are not case sensitive):
1. PUT name Derek Moss
2. PUT age 18
3. GET name
4. PUT gender M
5. DUMP
### Codes are in python3
### Telnet client is used. 
### To enable Telnet in Windows 10 using DISM command –[Open cmd in admin mode->dism /online /Enable-Feature /FeatureName:TelnetClientand->type telnet <host address> <port number>]
  
 ## Server: 
 Server keeps listening to only one client at a time. It stores the data in a dictionary received from Client(in this case proxyServer). Server also returns the GET and DUMP requests. In case of GET request, it receives a key and return the value if it is found else None. It returns all the keys stored when receives a DUMP request.
## ProxyServer:  ProxyServer keeps listening to only one client at a time as well as communicate with the main server. It basically designed to reduce the request overhead from the server and serves the clients when a frequestly used GET request is made. The frequency is 60 sec. For the PUT and DUMP requests it always reaches out to the server






