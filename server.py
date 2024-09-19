import socket
import threading
import tabulate

# GLOBAL VARIABLES ARE HERE >>>>>
ROOMS = {}
CLIENTS = {}
ROOM_COUNTER = 1
SERVER_RUNNING = True
HOST = "localhost"
PORT = 5555

# Server binding and listening are here >>>>>
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print("Server is listening on port 5555")


def send_message_to_room(room_id, message):
    for client in ROOMS[room_id]["clients"]:
        try:
            client.send(message.encode())
        except:
            # If sending fails, remove the client from the room
            remove_client((client, room_id))

# Function to remove a client from a room
def remove_client(sender):
    client, room_id = sender
    try:
        ROOMS[room_id]["clients"].remove(client)
        client.close()
    except ValueError:
        pass  # Client was already removed or not in the list



# Function to handle receiving messages from a client
def handle_client(client_socket):
    global ROOM_COUNTER
    name = client_socket.recv(1024).decode()
    CLIENTS[client_socket] = name
    room_id = None
    while SERVER_RUNNING:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data.lower() == "quit":
                if room_id:
                    ROOMS[room_id]["clients"].remove(client_socket)
                    send_message_to_room(room_id, f"{name} has left the room")
                client_socket.close()
                break
            elif data.lower() == "create":
                if room_id:
                    client_socket.send("You are already in a room.".encode())
                else:
                    ROOMS[ROOM_COUNTER] = {"clients": [client_socket], "creator": name}
                    room_id = ROOM_COUNTER
                    ROOM_COUNTER += 1
                    client_socket.send(f"Room {room_id} created. You are the creator.".encode())
            elif data.lower() == "join":
                if room_id:
                    client_socket.send("You are already in a room.".encode())
                else:
                    client_socket.send("Enter room id >>".encode())
                    room_id = int(client_socket.recv(1024).decode())
                    if room_id in ROOMS:
                        ROOMS[room_id]["clients"].append(client_socket)
                        send_message_to_room(room_id, f"{name} has joined the room")
                        client_socket.send(f"Joined room {room_id}".encode())
                    else:
                        client_socket.send("Room does not exist.".encode())
            elif data.lower() == "exit":
                if room_id:
                    ROOMS[room_id]["clients"].remove(client_socket)
                    send_message_to_room(room_id, f"{name} has left the room")
                    room_id = None
                    client_socket.send("Exited room.".encode())
                else:
                    client_socket.send("You are not in a room.".encode())
            elif data.lower() == "help":
                client_socket.send("Choose an option:\nCreate: To create a room\nJoin: To join a room\nExit: To Quit\nHelp: For Help".encode())
            else:
                if room_id:
                    send_message_to_room(room_id, f"{name}: {data}")
                else:
                    client_socket.send("You are not in a room. Use 'create' or 'join' to join a room.".encode())
        except:
            break
    if room_id:
        ROOMS[room_id]["clients"].remove(client_socket)
        send_message_to_room(room_id, f"{name} has left the room")
    CLIENTS.pop(client_socket, None)
    client_socket.close()
# Function to accept incoming connections
def accept_conn():
    while SERVER_RUNNING:
        try:
            client_socket, address = server.accept()
            print(f"Received conn from {address}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")
            continue



try:
    accept_thread = threading.Thread(target=accept_conn)
    accept_thread.start()
    while True:
        pass  # Keep the main thread alive
except KeyboardInterrupt:
    print("Shutting down server...")
    SERVER_RUNNING = False
    for client_socket in CLIENTS:
        client_socket.close()
    server.close()
    accept_thread.join()

