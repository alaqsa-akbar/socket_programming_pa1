import socket
import sys
import argparse

##################################################################
#                  Formatted Print statements                    #
##################################################################
# We provided some print statements to assist with
# formatting the outputs for the autograder  :)

# To print for invalid expression use:
## print("Invalid expression", flush=True)

# To print the final result for total value use:
## print(f"Total: {value}", flush=True)

# To print the sending message when sending to the server use:
## print(f"Sending operation: {op1} {op2} {op}", flush=True)
# OR 
## print(f"Sending operation: {expression_x}", flush=True)

# To print the error message after three timeouts use:
## print("Error - No response after 3 attempts", flush=True)

# Note: Replace variables inside {} with your own variables

# REMINDER: Use sys.stdout.flush() after or flush=True inside 
# any print statements to ensure that the output is printed
# on the terminal before timeout.


def send_udp(sock, msg, addr):
    retries = 0
    max_retries = 3

    while retries < max_retries:
        try:
            print(f"Sending operation: {word}", flush=True)
            sock.sendto(msg.encode(), addr)

            response, server_addr = sock.recvfrom(1024)
            return response.decode()

        except socket.timeout:
            retries += 1
        except socket.error as e:
            print(f"Socket error: {e}", flush=True)
            sys.exit(1)

    if retries == max_retries:
        print("Error - No response after 3 attempts", flush=True)
        sock.close()
        sys.exit(1)


parser = argparse.ArgumentParser(description='TCP Client')
parser.add_argument('hostname', help='IP or hostname')
parser.add_argument('port', type=int, help='port')
parser.add_argument('expression', help='expression')
args = parser.parse_args()

expression = args.expression
expression = expression.strip().split(' ')

valid_expression = len(expression) > 2

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    server_address = (args.hostname, args.port)

    while len(expression) != 1:
        for i in range(len(expression)):
            if expression[i] in ['+', '-', '*', '/']:
                if (i-2) < 0:
                    valid_expression = False
                    break
                word = expression.pop(i-2)
                word += f' {expression.pop(i-2)}'
                word += f' {expression.pop(i-2)}'

                response = send_udp(sock, word, server_address)

                if response == "Invalid expression":
                    valid_expression = False
                    break

                expression.insert(i-2, response)
                break

        if len(expression) == 2:
            valid_expression = False
        if not valid_expression:
            break

    if not valid_expression:
        print("Invalid expression", flush=True)
        sys.stdout.flush()
        sys.exit(1)
    else:
        print(f"Total: {expression[0]}")
        sys.stdout.flush()

except socket.error as e:
    print(f"Socket error: {e}")
    sys.stdout.flush()
    sys.exit(1)
    
finally:
    sock.close()