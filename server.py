import socket
import threading
import random

class BullsAndCowsServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 5000))
        self.server_socket.listen(5)
        self.players = {}
        
    def generate_secret_number(self):
        digits = list(range(10))
        random.shuffle(digits)
        secret_number = ''.join(str(d) for d in digits[:4])
        print(f"Generated secret number: {secret_number}")
        return secret_number

    def handle_client(self, client_socket, player_name):
        try:
            print(f"Connected to client {player_name}")
            secret_number = self.generate_secret_number()
            self.players[client_socket] = secret_number
            
            while True:
                guess = client_socket.recv(1024).decode().strip()
                if guess == "QUIT":
                    client_socket.send("QUIT".encode())
                    break
                print(f"({player_name}): Guessed number: {guess}, Secret number: {secret_number}")
                result = self.check_guess(guess, secret_number)
                client_socket.send(result.encode())
                if result.startswith("Congratulations"):
                    play_again = client_socket.recv(1024).decode().strip().lower()
                    if play_again == "yes":
                        secret_number = self.generate_secret_number()
                        self.players[client_socket] = secret_number
                        client_socket.send("Game restarted. Guess again.".encode())
                    else:
                        client_socket.send("Thank you for playing. Goodbye!".encode())
                        break
        except ConnectionResetError:
            print(f"Player {player_name} disconnected.")
        except ConnectionAbortedError:
            print(f"Player {player_name} aborted the connection.")
        finally:
            client_socket.close()
            del self.players[client_socket]

    def check_guess(self, guess, secret_number):
        if len(guess) != 4 or not guess.isdigit():
            return "Invalid guess. Please enter a 4-digit number."
        
        bulls = sum(1 for g, s in zip(guess, secret_number) if g == s)
        cows = sum(1 for g in guess if g in secret_number) - bulls
        
        if bulls == 4:
            return "Congratulations! You guessed the number."
        else:
            return f"Bulls: {bulls}, Cows: {cows}"

    def start(self):
        print("Server listening on {'127.0.0.1'}:{5000}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connected to client at {addr[0]}:{addr[1]}")
                player_name = client_socket.recv(1024).decode().strip()
                self.players[client_socket] = None
                threading.Thread(target=self.handle_client, args=(client_socket, player_name)).start()

        except KeyboardInterrupt:
            self.stop_server()
            print("Server interrupted.")

        self.server_socket.close()

if __name__ == "__main__":
    server = BullsAndCowsServer()
    server.start()
