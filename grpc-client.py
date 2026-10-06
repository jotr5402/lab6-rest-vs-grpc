#!/usr/bin/env python3

from __future__ import print_function

import argparse
import base64
from concurrent import futures
import io
import json
import random
import sys
import time

sys.path.append("./proto")

import grpc
import grpc_pb2
import grpc_pb2_grpc


def doRawImage(stub, debug=False):
  image = grpc_pb2.RawImageMsg(
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
  )

  response = stub.RawImage(image)

  if debug:
    print("Response is")
    print(response)


def doAdd(stub, debug=False):
  add = grpc_pb2.AddMsg(
    a = 5,
    b = 10
  )

  response = stub.Add(add)

  if debug:
    print("Response is")
    print(response)


def doDotProduct(stub, debug=False):
  dot_product = grpc_pb2.DotProductMsg(
    a = [random.random() for _ in range(100)],
    b = [random.random() for _ in range(100)]
  )

  response = stub.DotProduct(dot_product)

  if debug:
    print("Response is")
    print(response)


def doJsonImage(stub, debug=False):
  image_bytes = open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb").read()

  image = grpc_pb2.JsonImageMsg(
    img = base64.b64encode(image_bytes).decode("utf-8")
  )

  response = stub.JsonImage(image)

  if debug:
    print("Response is")
    print(response)


# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser(
  description='REST client for measuring server operations'
)

parser.add_argument(
  'host',
  help='IP address or hostname of the REST server'
)

parser.add_argument(
  'cmd',
  choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
  help='Operation to perform'
)

parser.add_argument(
  'reps',
  type=int,
  help='Number of repetitions for measurement'
)

parser.add_argument(
  '-p', '--port',
  type=int,
  default=5000,
  help='Server port (default: 5000)'
)

parser.add_argument(
  '-d', '--debug',
  action='store_true',
  help='Print the response from the server'
)

args = parser.parse_args()


# ---------------------------------------------------------
# Build server address
# ---------------------------------------------------------

addr = f"{args.host}:{args.port}"

print(f"Running {args.reps} reps against {addr}")

# ---------------------------------------------------------
# Perform requested operation
# ---------------------------------------------------------

cmd = None
match args.cmd:
  case "add":
    cmd = doAdd 
  case "rawImage":
    cmd = doRawImage
  case "dotProduct":
    cmd = doDotProduct
  case "jsonImage":
    cmd = doJsonImage

if cmd is not None:
  with grpc.insecure_channel(addr) as channel:
    stub = grpc_pb2_grpc.GrpcServiceStub(channel)

    start = time.perf_counter()

    for x in range(args.reps):
      cmd(stub, debug = args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")
