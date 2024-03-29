# Key-Value Storage System
An origin Server, proxy server and a client interaction implemented via python socket programming with storing at the origin server, caching at the proxy server and updating the cache every 60 sec based on Principle of Locality.
## Description
This project introduces the concept of client/server architecture and caching. Task is to create a simple web and proxy server that stores and retrieves key-value pairs using a socket programming interface. The server only permits commands such as GET, PUT, and DUMP in the request field followed by the key and value stored. GET returns the value of the key specified, PUT stores the key and a specified value on the server and DUMP lists all of the key value pairs contained in the server. When the client makes a GET request, this request is passed through the proxy server. If the server has made the same request using the same key, the key-value should be retrieved from the proxy server instead of the server. An example of commands are below(commands are not case sensitive):
1. PUT name Derek Moss     // Saves the {name:Derek Moss} in the server.
2. PUT age 18              // Saves the {age:18} in the server.
3. GET name                // Returns "Derek Moss"
4. PUT gender M            // Saves the {gender:M} in the server.
5. DUMP                    // Returns "name", "age", "gender"
  
## Origin Server: 
Server keeps listening to only one client at a time. It stores the data in a dictionary received from the Client(in this case proxyServer). Server also returns the GET and DUMP requests. It stores the key-val when receivesa PUT resquest. In case of a GET request, it receives a key and returns the value if it is found else None. It returns all the keys stored when it receives a DUMP request.
## ProxyServer:  
ProxyServer keeps listening to only one client at a time as well as communicating with the origin server. It is basically designed to reduce the request overhead from the server and serves the clients when a frequently used GET request is made. The memory is updated in every 60 sec. For the PUT and DUMP requests it always reaches out to the server
## Client:
Telnet client is used

#### Codes are in python3
#### To enable Telnet in Windows 10 using DISM command –[Open cmd in admin mode->dism /online /Enable-Feature /FeatureName:TelnetClientand->type telnet <host address> <port number>]
