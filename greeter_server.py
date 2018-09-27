# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python implementation of the GRPC helloworld.Greeter server."""
import os
from concurrent import futures

import grpc
import helloworld_pb2_grpc
import helloworld_pb2
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print('Hi, i am the greeter, in SayHello', os.getpid())
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    print('Starting up grpc server ...', os.getpid())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:16506')
    server.start()
    print('Started at', 'localhost:16506', os.getpid())
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Stoping grpc server ', os.getpid(), 'localhost:50051')
        server.stop(0)


def serve_ssl():
    print('Starting up grpc server (ssl)...', os.getpid())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    private_key_file = 'self.key'
    with open(private_key_file, 'rb') as f:
        private_key = f.read()

    cert_file = 'self.crt'
    with open(cert_file, 'rb') as f:
        cert_chain = f.read()

    server_cred = grpc.ssl_server_credentials(((private_key, cert_chain,),))
    server.add_secure_port('[::]:16506', server_cred)

    server.start()
    print('Started at', 'localhost:16506 (ssl)', os.getpid())
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Stoping grpc server ', os.getpid(), 'localhost:50051')
        server.stop(0)

if __name__ == '__main__':
    serve_ssl()
