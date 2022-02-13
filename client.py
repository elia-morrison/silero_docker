import socket
print("I'm running!")
HOST = socket.gethostbyname('tts_dns')
print("Got host!")
PORT = 9898

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('Socket inited')
    s.connect((HOST, PORT))
    print('Connected')
    s.sendall('Я в своём познании настолько преисполнился, что уже проживаю на триллионах таких же планет.'
              .encode('utf-8'))
    print('Content sent')
    data = s.recv(1024)
    print('Received', repr(data))
