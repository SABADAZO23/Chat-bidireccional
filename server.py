import threading
import socket

host = '127.0.0.1'
port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

clients = []
apodos = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index= clients.index(client)
            clients.remove(client)
            client.close()
            apodo = apodos[index]
            broadcast(f'{apodo} dejo el chat...'.encode('utf-8'))
            apodos.remove(apodo)
            break
         

def receive_connections():
    while True:
        client, address = server_socket.accept()
        print(f'Conectado con {str(address)}')

        client.send('APODO'.encode('utf-8'))
        apodo = client.recv(1024).decode('utf-8')
        apodos.append(apodo)
        clients.append(client)

        print(f'El apodo del cliente es {apodo}')
        broadcast(f'{apodo} se unio al chat!'.encode('utf-8'))
        client.send('Conectado al servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
print('Servidor escuchando...')
receive_connections()