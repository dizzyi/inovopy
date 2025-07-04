Module inovopy.socket
=====================
# Socket Module
This module provide api for handle generic socket communication
for communicating with robot for control.

## Class
- `TcpListener` : A class for managing listening socket connection
- `TcpStream` : A class for managing socket communication to a client
- `SocketExecption` : An Excpetion Class for all socket related exception
## Example

```python
from inovopy.socket import TcpListener, TcpStream

listener = TcpListener()               # <-- create a new listener
stream: TcpStream = listener.accept()  # <-- accept a new connection
del(listener)                          # <-- delete the listener to stop listening

stream.write("Send this message")      # <-- send a str message
read_message : str = stream.read()     # <-- read a messagea as str
```

Sub-modules
-----------
* inovopy.socket.tcp_listener
* inovopy.socket.tcp_stream

Functions
---------

`detect_interfaces() ‑> list[str]`
:   try to automatically detect local ip of this machine
    in all local networks
    
    ## Return:
    `list[str]` a list of ip

Classes
-------

`EndOfCommunication(*args, **kwargs)`
:   end of communication exception

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`SocketException(*args, **kwargs)`
:   socket commuication exception

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException