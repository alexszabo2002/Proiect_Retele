import socket
import json

def send_request(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65432))
    client.sendall(json.dumps(request).encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    client.close()
    return response

def print_pretty(json_response):
    data = json.loads(json_response)
    if isinstance(data, list):
        for item in data:
            print(f"Key: {item['key']}, Value: {item['value']}")
    elif isinstance(data, dict):
        if 'message' in data:
            print(data['message'])
        elif 'error' in data:
            print(f"Error: {data['error']}")
        else:
            for key, value in data.items():
                print(f"{key}: {value}")
    else:
        print(data)

if __name__ == '__main__':
    while True:
        print("Available commands: select, insert, update, delete, get_all, exit")
        command = input("Enter command: ").lower()
        
        try:
            if command == 'insert':
                key = int(input("Enter key: "))
                value = input("Enter value: ")
                request = {'command': 'add_object', 'key': key, 'value': value}
                response = send_request(request)
                print_pretty(response)
            
            elif command == 'delete':
                key = int(input("Enter key: "))
                request = {'command': 'delete_object', 'key': key}
                response = send_request(request)
                print_pretty(response)
            
            elif command == 'select':
                keys = input("Enter keys separated by space: ").split()
                keys = [int(k) for k in keys]
                request = {'command': 'select_objects', 'keys': keys}
                response = send_request(request)
                print_pretty(response)
            
            elif command == 'update':
                key = int(input("Enter key: "))
                new_value = input("Enter new value: ")
                request = {'command': 'update_object', 'key': key, 'value': new_value}
                response = send_request(request)
                print_pretty(response)
            
            elif command == 'get_all':
                request = {'command': 'get_all_objects'}
                response = send_request(request)
                print_pretty(response)
            
            elif command == 'exit':
                break
            
            else:
                print("Unknown command")
        except ValueError:
            print("Invalid input. Please enter the correct type of values.")
        except Exception as e:
            print(f"An error occurred: {e}")
