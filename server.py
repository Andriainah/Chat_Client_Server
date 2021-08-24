import socket 
import threading


class ChatServer:
    
    clients_list = []

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()
    #écouter la connexion entrante
    def create_listening_server(self):
    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creer un socket avec TCP et ipv4
        local_ip = '127.0.0.1'
        local_port = 10319
        # cela permet de redémarrer immédiatement un serveur TCP
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # cela oblige le serveur à écouter les requêtes provenant d'autres ordinateurs sur le réseau
        self.server_socket.bind((local_ip, local_port))
        print("Attendre des nouvelles messages")
        self.server_socket.listen(5) # écouter les connexions entrantes / max 5 clients
        self.receive_messages_in_a_new_thread()
    # fonction nouvelles messages
    def receive_messages(self, so):
        while True:
            incoming_buffer = so.recv(256) # initialise le buffer
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.broadcast_to_all_clients(so)  # envoyer à tous les clients
        so.close()
    # diffuser le message à tous les clients 
    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()
    # ajouter un nouvel client
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == "__main__":
    ChatServer()


