import socket
import threading

# Número total de ingressos disponíveis
available_tickets = 25

# Lock para garantir que as reservas sejam feitas de forma concorrente e segura
lock = threading.Lock()


# Função para tratar cada cliente de forma concorrente
def handle_client(client_socket, client_address):
    global available_tickets
    try:
        # Envia o número de ingressos disponíveis ao cliente
        with lock:
            client_socket.send(f"Ingressos disponíveis: {available_tickets}".encode('utf-8'))

        # Recebe a resposta do cliente se ele deseja comprar ou não
        choice = client_socket.recv(1024).decode('utf-8')

        if choice.lower() == "sim":
            with lock:
                if available_tickets > 0:
                    available_tickets -= 1
                    response = f"Reserva confirmada! Ingressos restantes: {available_tickets}"

                    # Log da escolha do cliente
                    print(f"Cliente {client_address} comprou um ingresso. Ingressos restantes: {available_tickets}")
                else:
                    response = "Ingressos esgotados!"
        else:
            response = "Você escolheu não comprar o ingresso."

        # Envia a resposta ao cliente
        client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Erro ao processar cliente {client_address}: {e}")

    finally:
        # Fecha a conexão com o cliente independentemente de falhas
        client_socket.close()


# Função principal para iniciar o servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Servidor de reserva de ingressos em execução...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}")

        # Cria uma nova thread para tratar cada cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


if __name__ == "__main__":
    start_server()
