# py_grpc_helloworld

openssl req -x509 -newkey rsa:4096 -keyout self.key -out self.crt -days 365  -nodes -subj '/CN=localhost'

python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. helloworld.proto

# To start server
python greeter_server.py

# To run client
python greeter_client.py