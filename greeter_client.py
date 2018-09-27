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

"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import grpc
import helloworld_pb2_grpc

import helloworld_pb2


def run():
    channel = grpc.insecure_channel('localhost:16506')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


def run_secure_crt():
    print('Secure Client call (crt)')
    private_crt_file = 'self.crt'
    trusted_certs = open(private_crt_file).read()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('localhost:16506', credentials)

    stub = helloworld_pb2_grpc.GreeterStub(channel)

    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received (crt): " + response.message)


def run_secure_pem():
    print('Secure Client call (pem)')
    private_pem_file = 'self.key'

    channel = grpc.secure_channel(
        'localhost:16506',
        credentials=grpc.ssl_channel_credentials(
            private_key=open(private_pem_file, 'rb').read()))

    stub = helloworld_pb2_grpc.GreeterStub(channel)

    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received (pem): " + response.message)


if __name__ == '__main__':
    run_secure_crt()
    # run_secure_pem()
