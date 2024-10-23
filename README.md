# Programming Assignment 1: Basics of Socket Programming
**Name:** Alaqsa Akbar \
**Email:** aakbar38@gatech.edu \
**Class:** CS-3251-B \
**Date:** 10/23/2024

## Files
### rpncalc.py
This file contains the implementation provided for the reverse-polish-notation (RPN) calculator. It has a class called RPNCalculator which can be called using:
```python
from rpncalc import RPNCalculator

rpn = RPNCalculator()
expression = '3 4 +'

result = rpn.evaluate(expression)
print(f'Result: {result}')
```
`RPNCalculator.evaluate()` can only take an expression of one operator. In addition, `RPNCalculator` only supports the following operators:
- Addition: `+`
- Subtraction: `-`
- Division: `/`
- Multiplication: `*`

This calculator is used in the servers only.

### tcpclient.py
This file includes the implementation for the client that uses TCP. You can call the file via:
```shell
python tcpclient.py hostname port expression
```
For example:
```shell
python tcpclient.py localhost 4000 '3 4 +'
```
The client file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_STREAM` (TCP). This then connects to the provided server address. The client seperates the expression down to its basic components in order to send it to the server as the server can only calculate expressions with one operator. In the meanwhile, it can identify if the expression is invalid. Similarly, it also checks for errors after reading the result from the server in the case that the server returned an error. The client can read up to 1024 bytes at once, which should be more than enough. The entire thing is wrapped in a `try` and `except` to catch errors such the inability to connect to the server. The client maitains an open connection with the server until it is done by sending an `'exit'` command when it finishes.

### tcpserver.py
This file includes the implementation for the server that uses TCP. You can call the file via:
```shell
python tcpserver.py port
```
For example:
```shell
python tcpserver.py 4000
```
The server file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_STREAM` (TCP) and binds to the local address using the provided port. It will listen to incoming requests using `socket.listen(5)`. The backlog was set to 5 arbitrarily. In an infinite while loop, the server will accept any request incoming and read 1024 bytes, then it will call its `RPNCalculator` instace to get the result for the incoming expression. If the incoming expression is invalid, the server will send `Invalid Expression` back otherwise it will send the correct result. The server will continously wait for an incoming request until it is shutdown. It will continue even if it encounters an error via the `try` and `except` blocks. The server maintains an open connection with the client until the client is done by recieving an `'exit'` command.

### udpclient.py
This file includes the implementation for the client that uses UDP. You can call the file via:
```shell
python udpclient.py hostname port expression
```
For example:
```shell
python tcpclient.py localhost 4000 '3 4 +'
```
The client file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_DGRAM` (UDP). Unlike the TCP implementation, this client does not connect to the destination address. A timeout period of 2 seconds is chosen using `socket.settimeout(2)` where a `Timeout` exception would be raised if the client does not recieve a reply from the server in that time. This is used in a custom defined `send_udp(socket, msg, addr)` function that will try to send `msg` to `addr` over `socket` 3 times before printing an error message and exiting. Similarly to TCP, the client seperates the expression down to its basic components in order to send it to the server while identifying errors. It also checks for errors after reading the result from the server in the case that the server returned an error. The client can read up to 1024 bytes at once, which should be more than enough. The entire thing is wrapped in a `try` and `except` to catch errors such the inability to send to the server.

### udpserver.py
This file includes the implementation for the server that uses TCP. You can call the file via:
```shell
python udpserver.py port
```
For example:
```shell
python udpserver.py 4000
```
The server file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_DGRAM` (UDP) and binds to the local address using the provided port. In an infinite while loop, the server will try to read any incoming message with a limit of 1024 bytes, then it will call its `RPNCalculator` instace to get the result for the incoming expression. If the incoming expression is invalid, the server will send `Invalid Expression` back otherwise it will send the correct result. The server will continously attempt to read incoming requests until it is shutdown. It will continue even if it encounters an error via the `try` and `except` blocks.

## Key Learnings
The programming assignment taught me the basics of socket programming and how TCP differs from UDP. I learnt how to program a basic client and server connection in Python. Here are some things I learnt:
- What sockets are and how they
    - Sockets are endpoints used for sending and recieving over a network
- Difference between `SOCK_STREAM` and `SOCK_DGRAM`
- How TCP works vs UDP
    - For instace, TCP connects to the server while UDP sends without connecting
- How to handle errors in connection (such as timeouts or using `try` and `except`)
- Packet sizes and buffer sizes
    - I learnt to choose the appropiate buffer size
- Utilizing `argparse` to create command line programs
- Timeouts in UDP and retrying before sending
- Gained a better understanding how IP addresses and ports work

## Challenges
Some challenges faced:
- Implementing the retry after timeout for the UDP
    - After learning about `socket.settimeout()` it was a bit easier
- Handling errors within the server to avoid the server shutting down
- Choosing the appropiate buffer size
    - I initially chose a buffer size too small but I increased it to fit the task
- Fragmenting the expression into its basic components so the server can understand it
    - This allows the client to communicate with the server without worrying of running out of buffer
- Maintaining an open TCP conenction between the client and server until no longer needed
    - The client sends an `'exit'` command when it is done

## Implementation Process
**These are the steps I took to implement the solution**

**The steps to implement the client:**
1. Read the documentation adn sample code from the lectures
2. Create the appropiate socket (TCP vs UDP)
3. Write code that can send a simple expression to a server
    - For TCP, first connect to the server address then send a message using `sock.sendall(msg.encode())`
    - For UDP, send a message directly without connecting to the server `socket.sendto(msg.encode(), addr)`
4. Develop a simple server to test your client

**The steps to implement the server:**
1. Read the documentation and sample code from the lectures
2. Develop a simple program that can read 1 message from a client
    - For TCP, use `socket.listen()` followed by `socket.accept()` in an infinite while loop then recieving from the client.
    - For UDP, use an infinite while loop and continously try to recieve using `data, addr = sock.recvfrom(1024)` 

**Test both the client and the server and debug errors. Further develop the code to match the rest of the requirements:**
1. Utilize the `RPNCalculator` in the servers to calculate an incoming expression
2. Send back the result to the client
3. Handle errors in the expression the `RPNCalculator` recieved by sending back an error message
4. For TCP server, add a method to maintain an open connection between the server and client
5. In the clients, segment the expression into its basic components and send each one iteratively until a final result is acheived.
6. Handle errors in the clients
7. For UDP client, implement a timeout using `socket.settimeout(2)` and a counter that decerements per retry for every time a message is sent.
8. Debug for any errors


## Known Bugs/Limitations
- The maximum buffer size for sending and recieving is 1024 bytes, although there shouldn't be a case where more than 1024 bytes are needed to be read since the expression is sent in chunks
- The server can only communicate with one endpoint at a time, no multithreading was implemented
- Does not support operators outside of `[+, -, *, /]`
- Expressions must be written in a specific format where all operands and operators are seperated by a space
