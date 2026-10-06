import argparse
import base64
from concurrent import futures
import io
import sys

sys.path.append("./proto")

import grpc
import grpc_pb2
import grpc_pb2_grpc

from PIL import Image

class GrpcServiceServicer(grpc_pb2_grpc.GrpcServiceServicer):
  def Add(self, request, context):
    return grpc_pb2.AddReply(
      sum = request.a + request.b
    )


  def RawImage(self, request, context):
    try:
      buffer = io.BytesIO(request.img)

      with Image.open(buffer) as image:
        return grpc_pb2.ImageReply(
          width = image.size[0],
          height = image.size[1]
        )

    except:
      return grpc_pb2.ImageReply(
        width = 0,
        height = 0
      )


  def DotProduct(self, request, context):
    a_len = len(request.a)
    b_len = len(request.b)

    if a_len != b_len:
      return grpc_pb2.DotProductReply(
        dotproduct = float("-inf")
      )

    dot_product = 0
    for i in range(a_len):
      dot_product += request.a[i] * request.b[i]

    return grpc_pb2.DotProductReply(
      dotproduct = dot_product
    )


  def JsonImage(self, request, context):
    try:
      buffer = io.BytesIO( base64.b64decode(request.img) ) 

      with Image.open(buffer) as image:
        return grpc_pb2.ImageReply(
          width = image.size[0],
          height = image.size[1]
        )

    except:
      return grpc_pb2.ImageReply(
        width = 0,
        height = 0
      )


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description = "gRPC server"
  )

  parser.add_argument(
    '-p', '--port',
    type = int,
    default = 5000,
    help = 'Port on which to run the server (default: 5000)'
  )

  args = parser.parse_args()

  server = grpc.server(
    futures.ThreadPoolExecutor(max_workers = 10)
  )

  grpc_pb2_grpc.add_GrpcServiceServicer_to_server(
    GrpcServiceServicer(),
    server
  )

  server.add_insecure_port(f"[::]:{args.port}")
  server.start()

  try:
    server.wait_for_termination()
  except KeyboardInterrupt:
    server.stop(grace = 10).wait()
