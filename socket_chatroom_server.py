import socket
import threading

def receive_messages(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(">> ",data.decode())

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	print("Process initiated");

except socket.error as err:
	print("Socket creation failed");
	
port = 12345;

#we will bind the server to listen for requests
#since we have used empty string instead of ipaddress
#server will listen to requests coming from any
#computer on the network
s.bind(('', port));
print("Socket binded to: ", port);

#socket will allow 5 unaccepted connections
#are kept waiting
#then it will refuse new connections
s.listen(5);
print("Socket is listening");
# Get the server's username
username = input("Enter your username: ")

while True:
    # Accept the connection and get the socket object and address of the client
    conn, add = s.accept()
    with conn:
        print("Got connection from ", add)
        conn.send(b"Connection successful")

        # Start a separate thread to receive messages from the client
        receive_thread = threading.Thread(target=receive_messages, args=(conn,))
        receive_thread.start()

        # Get the server's username
        username = input("Enter your username: ")

        # Enter and send messages to the client until the user inputs "exit"
        while True:
            data_sent = input("<< ").encode()
            if data_sent == "exit":
                break
            conn.sendall(f"{username}: {data_sent}".encode())
        print("Connection closed")
s.close();
