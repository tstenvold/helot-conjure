# pyserverless

A simple serverless implementation for offloading process intensive operations from embedded and mobile devices without having to maintain a proper server.

The server accepts a JSON with a username, authentication token, and python code and will return the result. The Python code must have the desired data stored in a variable called `result`

JSON Format

`{
    "userName": "tester",
    "authToken": "abc123",
    "Code": "result = 2+2*4"
}`

## Server
The database needs to be configured first run with `--dbadmin` to initialize the database (option `3` then `1`)

## Client
The client shows a basic example of how to connect, send a json and recieve back the processed data

## Tests
Tests currently only operate as client requests but will in the future, test database aspects and server side etc.
Tests should be run from the main directory with `pytest test/` 
The test will purge the database and all info there will be lost.

## Current Problems
- Sandboxed run environment is laughable, so this only works for trusted request (see next point)
- I've not decided upon how authentication will actually take place
- Likely in the future the server will respond with a process id instead of returning the execution result itself. This will allow the process to run long without threat of timing out the connection and then allow the client to request the result multiple times.
