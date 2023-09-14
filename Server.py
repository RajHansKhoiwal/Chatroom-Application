import socket
from statistics import mean
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 43389

server.bind((host, port))
server.listen()

clients = []
client_names = []


# send any recieved message to all the connected clients 
# except the client whose message is being broadcastes
def broadcast(message, curr_client):
	for client in clients:
		if client!=curr_client:
			client.send(message)


# function to remove client from the chat room
def remove_client(client):
	index = clients.index(client)
	clients.remove(client)
	client.close()
	name = client_names[index]
	broadcast(f'{name} has left! Member count={len(clients)}'.encode('utf-8'), client)
	client_names.remove(name)


# Function to handle clients'connections
def handle_client(client):
	while True:
		try:
			message = client.recv(1024)
			break_mssg = (message.decode()).split(': ')
			if(break_mssg[-1]=='quit'):
				remove_client(client)
				break
			broadcast(message, client)
		except:
			remove_client(client)
			break


# Main function to receive the clients connection
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('name?'.encode('utf-8'))
        name = client.recv(1024).decode()
        client_names.append(name)
        clients.append(client)
        print(f'The name of this client is {name}')
        broadcast(f'SERVER: {name} has joined. Member count={len(clients)}'.encode('utf-8'), '')
        client.send(''.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()