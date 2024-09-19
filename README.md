# Client-Server Chat Application

This project is a Python-based client-server chat application that allows multiple users to join rooms, send messages, and communicate with one another. Users can create new rooms or join existing ones. The project demonstrates socket programming, multithreading, and basic command handling.

## Features

- **Multiple Rooms**: Users can create and join different chat rooms.
- **Messaging**: Once in a room, users can send and receive messages.
- **Commands**:
  - `create`: Create a new chat room.
  - `join`: Join an existing chat room.
  - `exit`: Leave the current room.
  - `help`: Get a list of available commands.
  - `quit`: Disconnect from the server.

## Technologies Used

- Python 3
- Socket programming
- Multithreading

## Getting Started

### Prerequisites

Ensure you have Python 3 installed on your machine.

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/chat-app.git

2. Navigate to the project directory:

    ```bash
    cd chat-app

3. Install any dependencies if required (none needed for basic functionality).


## Running the Application
1. Start the Server:
In the terminal, navigate to the project folder and run:

    ```bash
    python server.py

This will start the server on localhost at port 5555. The server will listen for incoming client connections.

2.  Start the Client:
In a separate terminal window or machine, navigate to the same project folder and run:
    ```bash
    python client.py

This will start the client and attempt to connect to the server. Enter your name to set up the client and join or create chat rooms.

### Usage
After starting both the server and the client, the client will prompt for the following commands:

- `create`: Create a new room.
- `join`: Join an existing room by providing a room ID.
- `exit`: Exit the current room.
- `quit`: Disconnect from the server.
- `help`: Get a list of commands.

### Example
- Start the server.
- Connect two clients.
- One client can create a room using create, while the other can join using join followed by the room ID.
- Both clients can send messages within the room.