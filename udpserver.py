import socket
import sys
import argparse
from rpncalc import RPNCalculator

##################################################################
#                  Formatted Print statements                    #
##################################################################
# We provided some print statements to assist with
# formatting the outputs for the autograder  :)

# To print to indicate when the server starts:
## print(f"Server started on port {port}. Accepting connections",flush=True)

# To print the received message after receiving the expression 
# from the client use:
## print(f"Received operation: {op1} {op2} {op}",flush=True)
# OR
## print(f"Received operation: {expression_x}",flush=True)

# Note: Replace variables inside {} with your own variables

# REMINDER: Use sys.stdout.flush() after or flush=True inside 
# any print statements to ensure that the output is printed
# on the terminal before timeout.

parser = argparse.ArgumentParser(description='TCP Server')
parser.add_argument('port', type=int, help='Port number to listen on')
args = parser.parse_args()

port = args.port
clac = RPNCalculator()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    server_address = ('localhost', port)
    sock.bind(server_address)

    print(f"Server started on port {port}. Accepting connections", flush=True)

    while True:        
        try:
            data, addr = sock.recvfrom(1024)
            data = data.decode()
            print(f"Received operation: {data}", flush=True)

            value = clac.evaluate(data)

            if clac.input_error:
                response = "Invalid expression"
            else:
                response = str(value)

            sock.sendto(response.encode(), addr)

        except socket.error as e:
            print(f"Socket error: {e}", flush=True)
        except Exception as e:
            print(f"Error during operation: {e}", flush=True)

except socket.error as e:
    print(f"Socket error on server: {e}", flush=True)

finally:
    sock.close()
