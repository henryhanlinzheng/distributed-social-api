# Starter code for assignment 3 in ICS 32 Programming with Software Libraries

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

import socket
import time
import ds_protocol


def send(server: str, port: int, username: str, password: str,
         message: str, bio: str = None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            f_send = client.makefile('w')
            f_recv = client.makefile('r')

            join_str = ds_protocol.join_msg(username, password)
            f_send.write(join_str + '\r\n')
            f_send.flush()

            reply = f_recv.readline()
            resp_tuple = ds_protocol.extract_json(reply)

            if resp_tuple.type == 'error':
                print("Failed to join server: " + resp_tuple.message)
                return False

            token = resp_tuple.token
            timestamp = time.time()

            if message:
                post_str = ds_protocol.post_msg(token, message, timestamp)
                f_send.write(post_str + '\r\n')
                f_send.flush()

                reply = f_recv.readline()
                resp_tuple = ds_protocol.extract_json(reply)

                if resp_tuple.type == 'error':
                    print("Failed to post message: " + resp_tuple.message)
                    return False

            if bio:
                bio_str = ds_protocol.bio_msg(token, bio, timestamp)
                f_send.write(bio_str + '\r\n')
                f_send.flush()

                reply = f_recv.readline()
                resp_tuple = ds_protocol.extract_json(reply)

                if resp_tuple.type == 'error':
                    print("Failed to post bio: " + resp_tuple.message)
                    return False

        return True

    except Exception as e:
        print("Network error: " + str(e))
        return False
