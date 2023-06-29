# Cows-and-Bulls
It's a multiplayer game
Its works this way. Two clients connect to a server and the server produces a 4-digit number with non-repeating characters. 
Both clients numbers will be saved in the server data. Who finds the opponent's number first he is considered to ba a winner.
Output is evaluated in this way. If the chosen number is present in the opponent's number but in diff position then it is considered to be a cow(if more than one Cows), if it is present in the same position it is considered to be Bull
eg : client1 - 1642 ; client2 - 9613
if clinet1 says 6073 then the output is 1cow and 1bulls because 6 is present but in diff positions, and on bull because 3 is present in the same position.

