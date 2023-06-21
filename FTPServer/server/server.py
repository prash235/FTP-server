import socket as sc
import threading as th
import os, sys
import shutil  # Shutil module in Python provides many functions of high-level operations on files and collections of files
from commands import COMMANDS


def get_args(name, params):
    print(params)
    if params == '':
        return []
    elif COMMANDS[name][1] <= 1:
        params = [params.replace('[', '').replace(']', '')]
    elif name == 'writefil':
        params = params.split()
        print(params)
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


def clear_path(path):
    for c in ['../', './', '/', '..\\', '.\\', '\\']:
        path = path.replace(c, '')
    return path


def get_user_path():
    path = ''
    for d in USER_PATH:
        path += '/' + d
    return path + '/'


def get_root_path():
    return ROOT_DIR + get_user_path()


def ld_command(name, params):
    global ROOT_DIR, USER_PATH
    name = name.lower()

    if name == '' or name == 'end':
        return ''

    if name in COMMANDS:
        params = get_args(name, params)
        if name != "writefil":
            if not (COMMANDS[name][0] <= len(params) <= COMMANDS[name][1]):
                return '! LdCommand «' + name + '» params error, use «hep ' + name + '» to learn'
    else:
        return '! LdCommand «' + name + '» not found, use «hep» to learn LdCommands'

    if name == 'hep':
        text = ''
        if len(params) == 0:
            i = 1
            text += 'LdFileManager\nNote: Use brackets «[» and «]» for param\nwith space on multiparams commands\n'
            text += 'LdCommands (* - optional param):\n'
            for key in COMMANDS:
                text += f'{i}. {key} - {COMMANDS[key][2]}\n'
                i += 1
        else:
            text += f'LdFileManager LdCommand «{params[0]}»:'
            if params[0] in COMMANDS:
                text += COMMANDS[params[0]][2] + '\n'
            else:
                text += f'! LdCommand «{params[0]}» not found'
        return text
    elif name == 'setrot':
        new_path = params[0]
        if not os.path.isdir(new_path):
            return '! Path is not dir'
        else:
            ROOT_DIR = new_path
            file = open(SETTING_FILE, 'w')
            file.write(ROOT_DIR)
            file.close()
            return 'Root dir changed'
    elif name == 'getrot':
        return f'Root dir is «{ROOT_DIR}»'

    if ROOT_DIR == '':
        return f'! LdCommand «{name}» need root dir'

    if name == 'ind':
        in_dir = clear_path(params[0])
        path = get_root_path() + in_dir
        if os.path.exists(path) and os.path.isdir(path):
            USER_PATH.append(in_dir)
            return ''
        else:
            return 'Directory not exists'
    elif name == 'out':
        if len(USER_PATH) > 0:
            USER_PATH.pop()
            return ''
        else:
            return 'You in root dir!'
    elif name == 'lis':
        text = ''
        i = 1
        for f in os.listdir(get_root_path()):
            text += f'{i}. {f}\n'
            i += 1
        return text
    elif name == 'credir':
        path = get_root_path() + clear_path(params[0])
        try:
            os.mkdir(path)
        except OSError:
            return '! Directory not created'
        else:
            return 'Directory created'
    elif name == 'crefil':
        path = get_root_path() + clear_path(params[0])
        if os.path.exists(path):
            return 'File already exists'
        else:
            try:
                open(path, 'w').close()
            except OSError:
                return '! File not created'
            else:
                return 'File created'
    elif name == 'rendir':
        old_path = get_root_path() + clear_path(params[0])
        new_path = get_root_path() + clear_path(params[1])
        if os.path.exists(old_path) and os.path.isdir(new_path):
            try:
                os.rename(old_path, new_path)
            except OSError:
                return '! Directory not renamed'
            else:
                return 'Directory renamed'
        else:
            return 'Directory not exists'
    elif name == 'renfil':
        old_path = get_root_path() + clear_path(params[0])
        new_path = get_root_path() + clear_path(params[1])
        if os.path.exists(old_path) and os.path.isfile(new_path):
            try:
                os.rename(old_path, new_path)
            except OSError:
                return '! File not renamed'
            else:
                return 'File renamed'
        else:
            return 'File not exists'
    elif name == 'deldir':
        path = get_root_path() + clear_path(params[0])
        if os.path.exists(path) and os.path.isdir(path):
            try:
                os.rmdir(path)
            except OSError:
                return '! Directory not deleted'
            else:
                return 'Directory deleted'
        else:
            return 'Directory not exists'
    elif name == 'delfil':
        path = get_root_path() + clear_path(params[0])
        if os.path.exists(path) and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                return '! File not deleted'
            else:
                return 'File deleted'
        else:
            return 'File not exists'
    elif name == 'copfil':
        path_old = get_root_path() + params[0]
        path_new = get_root_path() + params[1]
        if os.path.exists(path_old) and os.path.isfile(path_old):
            try:
                shutil.copy(path_old, path_new)
            except IOError:
                return '! File not copied'
            else:
                return 'File copied'
        else:
            return 'File not exists'
    elif name == 'movfil':
        path_old = get_root_path() + params[0]
        path_new = get_root_path() + params[1]
        if os.path.exists(path_old) and os.path.isfile(path_old):
            try:
                shutil.move(path_old, path_new)
            except IOError:
                return '! File not moved'
            else:
                return 'File moved'
        else:
            return 'File not exists'
    elif name == 'redfil':
        path = get_root_path() + clear_path(params[0])
        max_lines = -1
        if len(params) > 1:
            try:
                max_lines = int(params[1])
            except ValueError:
                return '! LdCommand «' + name + '» second param not is number'
            if max_lines < 0:
                max_lines = 0
        if os.path.exists(path) and os.path.isfile(path):
            try:
                fil = open(path, 'r', encoding='utf-8')
                i = 1
                text = ''
                for line in fil.readlines():
                    if max_lines != -1 and i > max_lines:
                        break
                    text += f'{i}. {line}'
                    i += 1
                fil.close()
                return text
            except BaseException:
                return '! File not read'
        else:
            return 'File not exists'
    elif name == 'writefil':
        path = get_root_path() + clear_path(params[0])
        dataAppend = ""
        if len(params) > 1:
            try:
                for i in range(1, len(params)):
                    dataAppend += params[i] + " "
            except ValueError:
                return '! LdCommand «' + name + '» second param not is number'
            if dataAppend == "":
                print("Nothing to append")
        if os.path.exists(path) and os.path.isfile(path):
            try:
                myFile = os.open(path, os.O_APPEND | os.O_WRONLY)
                os.write(myFile, dataAppend.encode('utf-8'))
            except Exception as e:
                print(str(e))
            finally:
                os.close(myFile)
        else:
            return 'File not exists'
    elif name == 'statfile':
        path = get_root_path() + '/' + str(params[0])
        res = f"The current status of the file is : \n {os.stat(path=path)}"
        return res
    elif name == 'cftftp':
        path = get_root_path() + clear_path(params[0])
        if os.path.exists(path):
            return 'File already exists'
        else:
            try:
                fil = open(path, 'w')
                fil.write(params[1])
                fil.close()
            except OSError:
                return '! File not copied'
            else:
                return 'File copied'
    elif name == 'cffftp':
        path = get_root_path() + clear_path(params[0])
        if os.path.exists(path) and os.path.isfile(path):
            try:
                fil = open(path, 'r', encoding='utf-8')
                text = fil.read()
                fil.close()
                return f'{params[0]}<LdImp>{text}'
            except BaseException:
                return '! File not read'
        else:
            return 'File not exists'

    return ''


def input_port():
    global DEFAULT_PORT
    while True:
        new_port = input(f'Press «Enter» to start server on port {DEFAULT_PORT} or pre-input other port (1024-65535)\n> ')
        if new_port == '':
            return DEFAULT_PORT
        else:
            if new_port.isnumeric():
                new_port = int(new_port)
                if 1024 <= new_port <= 65535:
                    return new_port


def client_receiver(conn, addr):
    global client_count, client_shutdown, client_shutdown_log
    client = f'Client{addr[1]}'
    print(f'{client} [{addr[0]}:{addr[1]}] connected to ftp server')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        print(f'Ftp server receive data from {client}: «{data}»')
        args = data.split(' ', 1) # name of the command miltay aani tyachya pudhcha
        command_resp = ld_command(args[0], args[1] if len(args) == 2 else '')
        resp = get_user_path() + '<LdSep>' + command_resp
        conn.send(resp.encode())
    conn.close()
    client_count -= 1
    print(f'{client} disconnected from server')


def server_start(server, port):
    print(f'Starting ftp server on port {port}...')
    try:
        server.settimeout(1)
        server.bind(('', port))
        server.listen(100)
    except OSError:
        print(f'! Error starting ftp server on port {port}, try another port')
        return False
    print(f'Ftp server started on port {port}')
    return True


def server_listening(server):
    global client_count, server_shutdown
    while True:
        try:
            new_conn, new_addr = server.accept()
            th.Thread(target=client_receiver, args=(new_conn, new_addr)).start()
            client_count += 1
            server_shutdown = 30
        except sc.timeout:
            pass

        if client_count == 0:
            server_shutdown -= 1
            if 0 < server_shutdown <= 5:
                print(f'Server shutdown after {server_shutdown} seconds...')
            if server_shutdown <= 0:
                break

        if client_shutdown:
            print(client_shutdown_log)
            break


def server_command(name, params):
    global ROOT_DIR
    name = name.lower()

    if name == '' or name == 'end':
        return False

    if name in ['setrot', 'getrot', 'staftp']:
        params = get_args(name, params)
    else:
        print('! LdCommand «' + name + '» not found')
        return True

    if name == 'setrot':
        new_path = params[0]
        if not os.path.isdir(new_path):
            print('! Path is not dir')
        else:
            ROOT_DIR = new_path
            file = open(SETTING_FILE, 'w')
            file.write(ROOT_DIR)
            file.close()
            print('Root dir changed')
        return True
    elif name == 'getrot':
        print(f'Root dir is «{ROOT_DIR}»')
        return True

    if ROOT_DIR == '':
        print(f'! LdCommand «{name}» need root dir')
        return True

    if name == 'staftp':
        global PORT, DEFAULT_PORT, server_shutdown
        while True:
            PORT = input_port()
            if server_start(socket, PORT):
                server_shutdown = 30
                break
            if PORT == DEFAULT_PORT:
                DEFAULT_PORT = DEFAULT_PORT + 1

        server_listening(socket)
        return True

    return True



DEFAULT_PORT = 25000
client_count = 0
client_shutdown = False
client_shutdown_log = ''
server_shutdown = 0
socket = sc.socket()


SETTING_FILE = 'settings.ldm'
ROOT_DIR = ''
USER_PATH = []

try:
    file = open(SETTING_FILE, 'r')
    ROOT_DIR = file.readline()
    file.close()
    if not os.path.isdir(ROOT_DIR):
        ROOT_DIR = ''
except IOError:
    pass

print('FtpServer is started...')
if ROOT_DIR == '':
    print('Warning! Root dir not set!')
else:
    print(f'Root dir is «{ROOT_DIR}»')
print('Use server commands: «end», «setrot», «getrot», «staftp»')

while True:
    print('> ', end='')
    text = input().split(' ', 1)
    if not server_command(text[0], text[1] if len(text) == 2 else ''):
        break

print('LdFtpServer is shutdown...')

# LDM files are used when the entire set of visualization data cannot be loaded into active memory, such as in scientific visualization.
