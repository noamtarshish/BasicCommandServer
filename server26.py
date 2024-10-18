"""EX 2.6 server implementation
   Author:
   Date:
"""
import random
import socket
import time
from datetime import datetime
from random import randint

import protocol


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "TIME":
        response = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    elif cmd == "NAME":
        response = "SuperServer"
    elif cmd == "RAND":
        response = str(random.randint(1, 10))

    response_with_length = f"{len(response):02}{response}"
    return response_with_length

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print(f"Client sent: {cmd}")
            # 2. Check if the command is valid
            valid_cmd = protocol.check_cmd(cmd)
            # 3. If valid command - create response
            if valid_cmd:
                response = create_server_rsp(cmd)
                # 4. Send response to client
                client_socket.send(response.encode())
                # 5. If command is EXIT, break from while loop
                if cmd == "EXIT":
                    break
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == "EXIT":
            break

        # Send response to the client
        client_socket.send(response.encode())
        time.sleep(3)


    print("Closing\n")
    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
