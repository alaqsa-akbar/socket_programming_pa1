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
The client file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_STREAM` (TCP). This then connects to the provided server address. The client seperates the expression down to its basic components in order to send it to the server as the server can only calculate expressions with one operator. In the meanwhile, it can identify if the expression is invalid. Similarly, it also checks for errors after reading the result from the server in the case that the server returned an error. The client can read up to 1024 bytes at once, which should be more than enough. The entire thing is wrapped in a `try` and `except` to catch errors such the inability to connect to the server.

### tcpserver.py
This file includes the implementation for the server that uses TCP. You can call the file via:
```shell
python tcpserver.py port
```
For example:
```shell
python tcpserver.py 4000
```
The server file creates a socket of type `socket.AF_INET` (IP) and `socket.SOCK_STREAM` (TCP) and binds to the local address using the provided port. It will listen to incoming requests using `socket.listen(5)`. The backlog was set to 5 arbitrarily. In an infinite while loop, the server will accept any request incoming and read 1024 bytes, then it will call its `RPNCalculator` instace to get the result for the incoming expression. If the incoming expression is invalid, the server will send `Invalid Expression` back otherwise it will send the correct result. The server will continously wait for an incoming request until it is shutdown. It will continue even if it encounters an error via the `try` and `except` blocks.

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

## Key Learnings and Challenges
The programming assignment taught me 

## Known Bugs/Limitations
- The maximum buffer size for sending and recieving is 1024 bytes, although there shouldn't be a case where more than 1024 bytes are needed to be read since the expression is sent in chunks
- The server can only communicate with one endpoint at a time, no multithreading was implemented
- Does not support operators outside of `[+, -, *, /]`
- Expressions must be written in a specific format where all operands and operators are seperated by a space
