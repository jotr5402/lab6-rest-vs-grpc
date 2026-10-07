
|  Method           | Local | Same-Zone | Different Region |
|---                |---    |---        |---               |
|   REST add        |2.767  |3.144      |341.973           |
|   gRPC add        |0.798  |1.031      |166.097           |
|   REST rawimg     |5.102  |7.744      |1380.629          |
|   gRPC rawimg     |9.227  |13.166     |208.119           |
|   REST dotproduct |3.339  |4.089      |322.662           |
|   gRPC dotproduct |1.028  |1.382      |161.847           |
|   REST jsonimg    |39.110 |41.000     |1506.841          |
|   gRPC jsonimg    |29.451 |29.853     |205.394           |
|   PING            |0.056  |0.400      |178.944           |

Generally, gRPC performed much better than REST. In the Local and Same-Zone VMs tests, it took less time per operation in all operations except the raw image, although when testing locally (not in cloud) gRPC was also faster in this (~3 ms). In the Different Region test gRPC took much less time than REST, having a much larger improvement than the Local and Same-Zone tests. The improved performance of gRPC is partly due to the lower overall network latency of gRPC. Because REST creates a new TCP connection for each request, it must complete the TCP handshake every time, which adds latency between each operation, whereas gRPC only creates one TCP connection, and so only performs one handshake. This also explains why the Different Region test shows such a large disparity; the high latency makes TCP handshakes take much longer, making it dominate the time each operation takes.

<!-- You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead. -->
<!---->
<!-- You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries. -->

