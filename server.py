import threading
import socket

host = '0.0.0.0'
port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{message.decode('utf-8')}")
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)

            print(f"{nickname} hat sich vom Server getrennt!")
            broadcast(f"{nickname} hat sich vom Server getrennt!\n".encode('utf-8'))
            break


def receive():
    while True:
        client, address = server.accept()

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        nick = ''
        for namen in nicknames:
            nick = nick + namen + ' '

        print(f"Verbunden mit {str(address)} als Nickname {nickname}...")
        broadcast(f"{nickname} hat sich mit dem Server verbunden!\n".encode('utf-8'))
        client.send("Verbunden mit dem Server...\n".encode('utf-8'))
        client.send(f"Verbunden sind: {nick}\n*******************************************\n\n".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("\nChat-Server wurde gestartet...")
receive()
