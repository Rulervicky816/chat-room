# client.py

import socket
import threading
import sys

# Server info
HOST = '127.0.0.1'  # Localhost
PORT = 55555

def main():
    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {HOST}:{PORT}")
        print("Make sure the server is running first.")
        sys.exit(1)
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Choose a username
    username = input("Enter your username: ")
    if not username.strip():
        username = "Anonymous"

    # Flag to control threads
    running = True

    # Send messages to server
    def write():
        nonlocal running
        while running:
            try:
                message = input("")
                if message.lower() == 'quit':
                    running = False
                    break
                full_message = f'{username}: {message}'
                client.send(full_message.encode('utf-8'))
            except KeyboardInterrupt:
                running = False
                break
            except Exception as e:
                print(f"Error sending message: {e}")
                running = False
                break

    # Receive messages from server
    def receive():
        nonlocal running
        while running:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    print("Server disconnected.")
                    running = False
                    break
                if message == 'USERNAME':
                    client.send(username.encode('utf-8'))
                else:
                    print(message)
            except ConnectionResetError:
                print("Server disconnected.")
                running = False
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                running = False
                break

    # Run threads
    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    write_thread = threading.Thread(target=write, daemon=True)
    write_thread.start()

    # Wait for threads to finish
    try:
        while running:
            receive_thread.join(timeout=1)
            write_thread.join(timeout=1)
    except KeyboardInterrupt:
        print("\nDisconnecting from server...")
        running = False
    
    client.close()
    print("Disconnected from server.")

if __name__ == "__main__":
    main()
