import socket

class BullsAndCowsClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_ip, server_port):
        self.client_socket.connect((server_ip, server_port))
        print("Connected to the server.")

    def play(self):
        player_name = input("Enter your name: ")
        self.client_socket.send(player_name.encode())
        print("Enter 'QUIT' to exit the game.")

        while True:
            guess = input("Enter your guess: ")
            if self.has_duplicates(guess):
                print("Warning: Duplicate digits are not allowed in the guess number.")
                continue
            self.client_socket.send(guess.encode())
            result = self.client_socket.recv(1024).decode().strip()
            print(result)
            if result == "Congratulations! You guessed the number.":
                play_again = input("Do you want to play again? (yes/no): ")
                self.client_socket.send(play_again.encode())
                if play_again.lower() == "yes":
                    restart_message = self.client_socket.recv(1024).decode().strip()
                    print(restart_message)
                else:
                    break
            elif result == "QUIT":
                break

        self.client_socket.close()


    def has_duplicates(self, number):
        return len(set(number)) != len(number)

if __name__ == "__main__":
    client = BullsAndCowsClient()
    client.connect("localhost", 5000)
    client.play()
