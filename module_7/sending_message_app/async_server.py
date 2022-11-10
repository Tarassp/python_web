import asyncio
import socket

HOST = "127.0.0.1"
PORT = 65432


async def handle_client(new_socket):
    loop = asyncio.get_running_loop()
    while True:
        data = (await loop.sock_recv(new_socket, 1024)).decode('utf8')
        if not data:
            break
        print(f"Message from client: {data!r}")
        await loop.sock_sendall(new_socket, data.upper().encode('utf8'))

    new_socket.close()
    print("Socket is closed")


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)

    loop = asyncio.get_event_loop()
    while True:
        try:
            new_socket, _ = await loop.sock_accept(server)
            await loop.create_task(handle_client(new_socket))
        except KeyboardInterrupt as err:
            print(f'Destroy server: {err}')
        finally:
            new_socket.close()

if __name__ == "__main__":
    asyncio.run(run_server())
