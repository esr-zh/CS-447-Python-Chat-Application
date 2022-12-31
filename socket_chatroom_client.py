import socket;
import threading

def receive_messages(sock):
    while True:
        #recieving data from server
        data = sock.recv(1024)
        if not data:
            break
        print(">> ",data.decode())

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	print("Process initialised");
	
except socket.error as err:
	print("Could not setup socket");

#port  over which the computers are connected	
port = 12345;

#ip address of another computer
ip = input("Enter the ip address of the server: ");

# Get the client's username
username = input("Enter your username: ")

with s:
#connecting to the server
	s.connect((ip,port));
	#recieving the data from server
	rec = s.recv(1024);
	print(rec.decode());
	
	# Start a separate thread to receive messages from the server
	receive_thread = threading.Thread(target=receive_messages, args=(s,))
	receive_thread.start()
	
	while True:
		#Enter message to be sent to server
		data_sent = (input("<< ")).encode();
		# If the user inputs "exit", close the connection
		if data_sent == "exit":
			break;
		s.sendall(f"{username}: {data_sent}".encode())
		#if empty string is sent
		#connection closes
		if not data_sent:
			break;

print("Connection closed");

#close the connection
s.close();
