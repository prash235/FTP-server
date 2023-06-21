import socket as sc
import os


def input_port():
    global DEFAULT_PORT
    while True:
        new_port = input(f'Press «Enter» to start client on server port {DEFAULT_PORT} or pre-input other port (1024-65535)\n> ')
        if new_port == '':
            return DEFAULT_PORT
        else:
            if new_port.isnumeric():
                new_port = int(new_port)
                if 1024 <= new_port <= 65535:
                    return new_port


def client_start(client, port):
    print(f'Starting client on server port {port}...')
    try:
        client.connect(('192.168.123.4', port))
    except OSError as err:
        print(err)
        return False
    print(f'Client connected to server on port {port}')
    return True


def get_args(name, params):
    if params == '':
        return []
    else:
        temp = ''
        in_brackets = False
        for s in params:
            if s == '[':
                in_brackets = True
            elif s == ']':
                in_brackets = False
            else:
                if s == ' ' and not in_brackets:
                    temp += '<LdSep>'
                else:
                    temp += s
        params = temp.split('<LdSep>')
    return params


print('LdFtpClient is started...')

USER_PATH = '/'
DEFAULT_PORT = 25000
socket = sc.socket()

while True:
    PORT = input_port()
    if client_start(socket, PORT):
        break
    if PORT == DEFAULT_PORT:
        DEFAULT_PORT = DEFAULT_PORT + 1


while True:
    data = input(USER_PATH + '> ')
    if data == 'end':
        print(f'Client disconnected from ftp server')
        break
    try:
        args = data.split(' ', 1)
        name = args[0]
        if name == 'cftftp' and len(args) > 1:
            params = get_args(name, args[1])
            path = 'home/' + params[0]
            if os.path.exists(path) and os.path.isfile(path):
                try:
                    file = open(path, 'r', encoding='utf-8')
                    text = file.read()
                    print('file data: ' + text)
                    file.close()
                    data = data + ' [' + text + ']'
                except BaseException:
                    print('! File not read')
                    continue
            else:
                print('File not exists')
                continue

        socket.send(data.encode())
        data = socket.recv(1024)
        data = data.decode()
        data = data.split('<LdSep>', 1)
        USER_PATH = data[0]
        if len(data) == 2:
            data = data[1]
            if '<LdImp>' in data:
                imp = data.split('<LdImp>')
                if len(imp) == 2:
                    path = 'home/' + imp[0]
                    if os.path.exists(path):
                        data = 'File on client already exists'
                    else:
                        try:
                            fil = open(path, 'w')
                            fil.write(imp[1])
                            fil.close()
                            data = 'File copied'
                        except OSError:
                            data = '! File not copied'
            print(data)
    except OSError:
        print(f'! Error send data, server disconnect')
        break

socket.close()

print('LdFtpClient is finished...')
