import socket
import sqlite3
import threading
import json

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def handle_client(client_socket):
    with client_socket:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            request = json.loads(request)
            command = request['command']
            
            if command == 'get_all_objects':
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM objects')
                objects = cursor.fetchall()
                conn.close()
                response = json.dumps([dict(obj) for obj in objects])
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'select_objects':
                keys = request['keys']
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM objects WHERE key IN ({seq})'.format(seq=','.join(['?']*len(keys))), keys)
                objects = cursor.fetchall()
                conn.close()
                if not objects:
                    response = json.dumps({'error': 'One or more keys do not exist.'})
                else:
                    response = json.dumps([dict(obj) for obj in objects])
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'add_object':
                key = request['key']
                value = request['value']
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM objects WHERE key = ?', (key,))
                obj = cursor.fetchone()
                if obj:
                    response = json.dumps({'error': f'Key {key} already exists.'})
                else:
                    cursor.execute('INSERT INTO objects (key, value) VALUES (?, ?)', (key, value))
                    conn.commit()
                    response = json.dumps({'message': f'Object with key {key} added.'})
                conn.close()
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'update_object':
                key = request['key']
                new_value = request['value']
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM objects WHERE key = ?', (key,))
                obj = cursor.fetchone()
                if obj:
                    cursor.execute('UPDATE objects SET value = ? WHERE key = ?', (new_value, key))
                    conn.commit()
                    response = json.dumps({'message': f'Object with key {key} updated.'})
                else:
                    response = json.dumps({'error': f'Key {key} does not exist.'})
                conn.close()
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'delete_object':
                key = request['key']
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM objects WHERE key = ?', (key,))
                obj = cursor.fetchone()
                if obj:
                    cursor.execute('DELETE FROM objects WHERE key = ?', (key,))
                    conn.commit()
                    response = json.dumps({'message': f'Object with key {key} deleted.'})
                else:
                    response = json.dumps({'error': f'Key {key} does not exist.'})
                conn.close()
                client_socket.sendall(response.encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen(5)
    print('Server listening on port 65432')

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
