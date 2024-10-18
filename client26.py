"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import time

import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("54.71.128.194", 8850))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            # If the command is valid:
            print(f"Sending command: {user_input} to server\n")
            # 1. Add length field ("RAND" -> "04RAND")
            command_to_send = protocol.create_msg(user_input)
            # 2. Send it to the server
            my_socket.send(command_to_send.encode())
            time.sleep(2)
            # 3. If command is EXIT, break from while loop
            if user_input == "EXIT":
                break
            # 4. Get server's response
            valid_msg, response = protocol.get_msg(my_socket)
            # 5. If server's response is valid, print it
            if valid_msg:
                print(f"Server response: {response}\n")

            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
