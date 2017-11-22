from threading import Thread
import socket

target = ("0.0.0.0",6000)
konusammi = False

def dinle(server):
    global konusammi
    server.send(bytes(input(str(server.recv(1024),encoding="utf-8")),encoding="utf-8"))
    konusammi = True
    try:
        while True:
            data = str(server.recv(1024),encoding="utf-8")
            if data:
                print(data,end="")
    except:
        pass
    finally:
        print("Ciktim gitti \u2764")
        server.close()

def konus(server):
    try:
        while True:
            server.send(bytes(input(">>> "),encoding="utf-8"))
    except:
        pass
    finally:
        print("Ciktim gitti \u2764")
        server.close()


with socket.socket() as client:
    client.connect(target)
    
    dinleTh = Thread(target=dinle,args=(client,))
    dinleTh.start()
    
    while(not konusammi):
        pass
    
    konusTh = Thread(target=konus,args=(client,))
    konusTh.start()
    
    konusTh.join()

