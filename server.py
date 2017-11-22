from threading import Thread, Lock
import socket

ip = ("0.0.0.0",6000)
clients = []
lock = Lock()

def sendAll(data,isim):
    mesaj = "\r>>> " + "[" + isim + "] " + data + "\n>>> "
    print(mesaj)
    silinecekler = []
    for client in clients:
        cSocket = client[0]
        try:
            lock.acquire()
            if isim!=client[1]:
                cSocket.send(bytes(mesaj,encoding="utf-8"))
            lock.release()
        except:
            silinecekler.append(client)
    for i in silinecekler:
        clients.remove(i)

def clientHandler(client):
    client.send(b"\rTatlim ismin? ")
    isim = str(client.recv(1024),encoding="utf-8")
    clients.append([client,isim])
    print("Serverdakiler: "+ ", ".join([i[1] for i in clients]))
    try:
        while True:
            data = str(client.recv(1024),encoding="utf-8")
            if data:
                sendAll(data,isim)
    except:
        pass
    finally:
        print(isim + " sunucudan ayrildi.")
        client.close()

with socket.socket() as server: # tcp kullaniyoruz. socket olusturduk.
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1) #socket kullanimda olsa dahi ac
    server.bind(ip) # serveri bir adrese bagla
    server.listen(15) # agi dinliyoruz
    print("Server basladi!")
    while True:
        client, addr = server.accept() # gelen baglantiyi kabul ediyoruz.
        clientThread = Thread(target=clientHandler,args=(client,))
        clientThread.start()
