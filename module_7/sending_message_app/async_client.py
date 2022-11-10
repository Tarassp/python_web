import socket
import asyncio


HOST = "127.0.0.1"
PORT = 65432

MESSAGE = "Python Web development"


async def run_client():
    loop = asyncio.get_event_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = HOST, PORT
        try:
            await loop.sock_connect(sock, server)
            print(f'Connection established {server}')
            for line in MESSAGE.split(' '):
                print(f'Send data: {line}')
                await loop.sock_sendall(sock, line.encode())
                response = await loop.sock_recv(sock, 1024)
                print(f'Response data: {response.decode()}')
        except Exception as error:
            print(f"Client side error: {error}")

    print(f'Data transfer completed')


if __name__ == '__main__':
    asyncio.run(run_client())
