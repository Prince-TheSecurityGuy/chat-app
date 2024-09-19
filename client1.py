import socket
import threading

# Set up the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "localhost"
PORT = 5555
RUNNING = True


# Function to send messages
def send_message():
    while RUNNING:
        try:
            message = input()
            client.send(message.encode())
        except:
            close_conn()
            break

# Function to receive messages
def receive_message():
    while RUNNING:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            close_conn()
            break

def close_conn():
    global RUNNING
    RUNNING = False
    client.close()

def connect_conn():
    client.connect((IP, PORT))

    name = ""
    while not name:
        name = input("Setup your name >> ")
        if not name:
            continue
        client.send(f"{name}".encode())
    
    send_thread = threading.Thread(target=send_message)
    receive_thread = threading.Thread(target=receive_message)
    send_thread.start()
    receive_thread.start()

# Connect to the server
connect_conn()


