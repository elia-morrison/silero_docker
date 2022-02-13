import socket
from src.model import SileroModel
from multiprocessing import Process, Pipe
import time


def tts_worker(conn, *args, **kwargs):
    model = SileroModel(*args, **kwargs)
    while True:
        text = conn.recv()
        start = time.time()
        audio = model.apply_tts(text)
        end = time.time()
        print(f'Spent {end-start} time to process this text!')
        conn.send(audio)


def init_worker_daemon(func, *args):
    worker = Process(target=func, args=args, daemon=True)
    worker.start()
    return worker


HOST = socket.gethostbyname('tts_dns')
PORT = 9898
MODELPATH = 'data/model_baya.pt'
ENCODING = 'utf-8'


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    worker = init_worker_daemon(tts_worker, child_conn, MODELPATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            sock_conn, addr = s.accept()
            with sock_conn:
                print('Connected by', addr)
                while True:
                    msg = sock_conn.recv(1024).decode(ENCODING)
                    if not msg:
                        break

                    print(f'Sock MSG read: {msg}')

                    if msg == 'START':
                        if worker.is_alive():
                            worker.terminate()

                        print('Starting process...')

                        worker = init_worker_daemon(
                            tts_worker, child_conn, MODELPATH)
                    elif msg == 'STOP':
                        if worker.is_alive():
                            worker.terminate()

                        print('Shutting down...')
                    else:
                        if worker.is_alive():
                            parent_conn.send(msg)
                            audio = parent_conn.recv()
                            sock_conn.sendall(
                                'Audio processed!'.encode(ENCODING))
