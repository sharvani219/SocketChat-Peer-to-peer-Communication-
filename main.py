import socket
import threading
import os
import sys

def setup_server_socket():
    #Set up the server socket that listens on an available port and return the socket and port number.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 0))  # Bind to an available port
    server_socket.listen(1)
    port = server_socket.getsockname()[1]
    print(f"Server listening on port: {port}")
    return server_socket, port

def connect_to_server(host, port):
    #Connect to the server at the given host and port.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
    except socket.error as e:
        print(f"Could not connect to server: {e}")
        sys.exit(1)
    return client_socket

def send_messages(conn):
    #Send messages and handle the 'transfer' command for file transfers.
    try:
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                conn.sendall('exit'.encode('utf-8'))
                print("Exiting...")
                break
            elif message.startswith('transfer '):
                filename = message.split(maxsplit=1)[1]
                send_file(filename, conn)
            else:
                conn.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send message: {e}")

def receive_messages(conn):
    #Receive messages and handle file transfers or exit commands.
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("Connection closed by the other side.")
                break
            message = data.decode('utf-8')
            if message.lower() == 'exit':
                print("Other user has left the chat.")
                break
            elif message.startswith('TRANSFER '):
                handle_file_receive(conn, message)
            else:
                print(f"Received: {message}")
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        conn.close()
        print("Connection closed.")

def send_file(filename, conn):
    #Send a file after notifying the receiver with the file size.
    try:
        if not os.path.exists(filename):
            print("File not found.")
            return
        file_size = os.path.getsize(filename)
        conn.sendall(f"TRANSFER {filename} {file_size}".encode('utf-8'))
        with open(filename, 'rb') as f:
            bytes_sent = f.read(1024)
            while bytes_sent:
                conn.sendall(bytes_sent)
                bytes_sent = f.read(1024)
        print(f"File {filename} sent successfully.")
    except Exception as e:
        print(f"Failed to send file: {e}")

def handle_file_receive(conn, command):
    #Receive a file based on a preceding TRANSFER command.
    _, filename, file_size = command.split()
    file_size = int(file_size)
    with open('received_' + filename, 'wb') as f:
        while file_size > 0:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            file_size -= len(data)
    print(f"File received and saved as 'received_{filename}'.")

def main():
    inp = input("⌨️ Enter User name: 'Alice/Bob': ").lower()
    server_socket, my_port = setup_server_socket()
    other_port = int(input(f"Enter the other user's port number: "))
    host = socket.gethostbyname(socket.gethostname())
    
    if inp == 'alice':
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")
        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
        send_messages(conn)
    else:
        conn = connect_to_server(host, other_port)
        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
        send_messages(conn)

if __name__ == "__main__":
    main()
