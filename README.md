This command-line chat application, built in Python, uses sockets and threading to allow users on the same network to send messages and transfer files.

Requirements:
-Python 3.x

How to Use:
-Open a terminal window.
-Navigate to the directory where the ChatApp code is saved.
-Run the command: python ChatApp.py.
-Enter "Alice" or "Bob" when prompted for the username.
-Alice will automatically have a server socket set up and will display a port number.
-Bob should enter the port number shown on Alice's console to connect to her.
-Start typing messages and press Enter to send them.
-To transfer a file, type transfer <file_path> and press Enter. The application will check for the file's existence and send it if found.
-To exit the chat, type exit. This will close the connection and terminate the application.

How It Works:
The ChatApp uses Python's socket and threading modules:
Server Socket (Alice): Starts and listens on an automatically assigned port, waiting for a connection.
Client Socket (Bob): Connects to the server using the provided port number.
Message and File Transfer: Users can send text messages or initiate file transfers using specific commands. Messages like transfer <file_path> trigger file transmission, and exit closes the connection.

Error Handling and Notifications:
Errors in message transmission or file handling are reported to the console.
Notifications confirm when messages are sent or files are transferred/received.

Acknowledgements:
This code was written by Sharvani Gouni and Singam Vineetha