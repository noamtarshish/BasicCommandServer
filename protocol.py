
LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data == 'RAND' or data == 'NAME' or data == 'TIME' or data == 'EXIT':
        return True
    else:
        return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    return f"{len(data):02}{data}"


def get_msg(my_socket):
    """Extract message from protocol, without the length field.
       If length field does not include a number, returns False, "Error" """
    try:
        # שלב ראשון - קבלת שדה האורך
        length_field = my_socket.recv(LENGTH_FIELD_SIZE).decode()
        if not length_field.isdigit():
            return False, "Error"

        # שלב שני - המרת שדה האורך למספר
        message_length = int(length_field)

        # שלב שלישי - קבלת ההודעה עצמה על פי האורך
        message = ''
        while len(message) < message_length:
            chunk = my_socket.recv(message_length - len(message)).decode()
            if not chunk:
                break
            message += chunk

        return True, message
    except Exception as e:
        print(f"Error occurred: {e}")
        return False, "Error"

