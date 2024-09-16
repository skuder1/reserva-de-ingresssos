import socket


def reserve_ticket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    # Recebe a informação sobre os ingressos disponíveis
    available_tickets = client.recv(1024).decode('utf-8')
    print(f"[SERVIDOR]: {available_tickets}")

    # Pergunta ao usuário se deseja comprar o ingresso
    choice = input("Você deseja comprar um ingresso? (Sim/Não): ")

    # Envia a escolha do usuário ao servidor
    client.send(choice.encode('utf-8'))

    # Recebe a resposta do servidor sobre a compra
    response = client.recv(1024).decode('utf-8')
    print(f"[SERVIDOR]: {response}")

    client.close()


# Executa o cliente
if __name__ == "__main__":
    reserve_ticket()
