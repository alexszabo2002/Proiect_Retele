# Database Object Access Management

## Project Requirements

- The server manages a list of objects retrieved from a database, each identified by a unique key.
- Clients can query the server to select a list of objects with specific key values.
- The server keeps track of the keys for the selected objects for each client.
- Clients can update or delete objects by key.
- When an object is modified, the server notifies all clients who previously selected the object.
- Changes to objects are saved in the server's memory and the database.

## Usage Instructions

1. **Setup the Database:**

   Run the following command to set up the database:
   ```sh
   python database_setup.py

2. **Start the Server:**

    Run the server using the command:
    ```sh
    python server.py

3. **Client Operations:**

    To retrieve a list of objects with specific key values:
    ```sh
    python client.py get_keys [key1] [key2] ...

    To update an object by key:
    ```sh
    python client.py update [key] [new_value]

    To delete an object by key:
    ```sh
    python client.py delete [key]
