# Helot Conjure

A simple standalone SSL serverless implementation in Python for offloading process intensive operations from embedded and mobile devices without having to maintain a full server.

The server accepts a JSON with a username, authentication code, and python code and will return the result. The Python code must have the desired data stored in a variable called `result`

JSON Format

`{
    "userName": "tester",
    "authToken": "abc123",
    "Code": "result = 2+2*4"
}`

## Server
The database needs to be configured first run with `--dbadmin` to initialize the database (option `3` then `1`). The server also requires a `localhost.pem` file to be located in the main directory. Generate this file by running `openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout certificate.pem
Generating a 1024 bit RSA private key`

## Client
The client shows a basic example of how to connect, send a json and receive back the processed data.
The Advanced client shows a more involved example of sending a code snippet that returns an PIL Image Object

## Tests
Tests can be run without a server running by using the script `./tests/run_tests.sh`.
The script runs the tests and also generates a coverage report html and displays the coverage results.

## Current Problems
- Sandboxed run environment is laughable, so this only works for trusted request (see next point)
- Likely in the future the server will respond with a process id instead of returning the execution result itself. This will allow the process to run long without threat of timing out the connection and then allow the client to request the result multiple times.
