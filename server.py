# server.py

import socket
import threading
import sys

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555        # You can change this if needed

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}... Waiting for connections.")
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)

clients = []
usernames = []

# Thread lock for thread-safe operations
lock = threading.Lock()

# Broadcast message to all clients
def broadcast(message):
    with lock:
        disconnected_clients = []
        for client in clients:
            try:
                client.send(message)
            except:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            remove_client(client)

# Remove client from lists
def remove_client(client):
    with lock:
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            usernames.remove(username)
            client.close()
            broadcast(f"{username} has left the chat.".encode('utf-8'))
            print(f"{username} disconnected.")

# Handle each client connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            broadcast(message)
        except Exception as e:
            print(f"Error handling client: {e}")
            remove_client(client)
            break

# Accept new clients
def receive():
    print("Server is ready to accept connections. Press Ctrl+C to stop the server.")
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            # Ask for username
            client.send('USERNAME'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            
            if not username.strip():
                username = "Anonymous"
            
            # Check if username is already taken
            with lock:
                if username in usernames:
                    username = f"{username}_{len([u for u in usernames if u.startswith(username)])}"
                
                usernames.append(username)
                clients.append(client)

            print(f"Username of the client is {username}")
            broadcast(f"{username} joined the chat!".encode('utf-8'))
            client.send("Connected to the server!".encode('utf-8'))

            # Start handling thread
            thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
            thread.start()
            
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")

def main():
    try:
        receive()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        # Close all client connections
        with lock:
            for client in clients:
                try:
                    client.close()
                except:
                    pass
        server.close()
        print("Server stopped.")

if __name__ == "__main__":
    main()
