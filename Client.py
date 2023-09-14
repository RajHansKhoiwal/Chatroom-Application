import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

name = input('Enter login name: ')
client.connect(('localhost', 43389))

# function to recieve any message send from the server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "name?":
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

# function to take input from the client and send the message to the server
def client_send():
    while True:
        get_input = input()
        message = f'{name}: {get_input}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()