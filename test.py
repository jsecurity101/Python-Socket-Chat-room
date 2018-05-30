
 
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4000 
PORT = 12345

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    
    SOCKET_LIST.append(server_socket)
 
    print "Chat has server started on port " + str(PORT) #shows success of connection
 
    while 1:

        
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        for sock in ready_to_read:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected has connected to chat" % addr #shows on server side
                broadcast(server_socket, sockfd, "[%s:%s] entered our chat room\n" % addr) #shows on client side
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)  # data has been lost and no connection from client

                except:
                    broadcast(server_socket, sock, "Client (%s, %s) has left the chat room " % addr) #Client left chat room, connection was broken
                    continue

    server_socket.close()
    

def broadcast (server_socket, sock, message): #sends message to all clients
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock :
           try :
                socket.send(message)
           except :
                socket.close() 
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())
