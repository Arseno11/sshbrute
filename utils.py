import socket
import paramiko
from termcolor import colored
from colorama import Fore, Style

def handle_ssh_error(server, username, password, i, total_usernames, j, total_passwords, error):
    if isinstance(error, paramiko.AuthenticationException):
        print(colored(f'=> [ATTEMPT] target {server} - login "{username}" - pass "{password}" - {i} of {total_usernames} [{j}/{total_passwords}]', 'red'))
    elif isinstance(error, paramiko.SSHException):
        print(colored(f'=> Error connecting to {server}.', 'red'))
        return
    elif isinstance(error, socket.timeout):
        print(colored(f'=> Error reading SSH protocol banner for {server}.', 'red'))
        return True
    else:
        print(colored(f'=> Error: {str(error)}', 'red'))
        return True
