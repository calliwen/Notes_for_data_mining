# Spark Steaming 容错机制

参考：https://www.csdn.net/article/2015-03-03/2824081

Spark Streaming就支持从driver和worker故障中恢复。存在故障恢复以后丢失数据的情况。Spark 1.2对预写日志（journaling）。

Spark Streaming应用程序在计算上有一个内在的结构——在每段 micro-batch 数据周期性地执行同样的Spark计算。这种结构允许把应用的状态（亦称checkpoint）周期性地保存到可靠的存储空间中，并在 driver 重新启动时恢复该状态。 (driver 容错机制 )

对于文件这样的源数据，这个driver恢复机制足以做到 零数据丢失，因为所有的数据都保存在了像HDFS或S3这样的容错文件系统中了。
但对于像Kafka和Flume等其它数据源，有些接收到的数据还只缓存在内存中，尚未处理，有可能会丢失。

## WAL( write ahead log )
即，当 driver 失败时，所有 excutor 连同在内存中的数据也会被终止；    对于 kafka 和 flume 数据源接收的数据，在未处理之前，缓存在excutor内存中，即使driver 重启，这些数据也不能恢复。 spark 1.2版本中，加入了 write ahead log 功能来解决这种问题。

WAL(write ahead log）用来保证任何数据的持久性。 先将操作记录一个持久日志，然后才对数据施加这个操作。

对 kafka, flume，利用receiver 接收数据，其作为常驻任务在 excutor 中运行，负责接收数据，且负责确认接收数据（支持时）。
启用 WAL 后，所有接收到的数据都保存在了 容错文件系统的日志中。 且，接收数据的正确性只在数据被预写到日志以后接收器才会确认。 保证了数据零丢失。

## 配置

通过streamingContext.checkpoint(path-to-directory)设置检查点的目录。这个目录可以在任何与HadoopAPI口兼容的文件系统中设置，它既用作保存流检查点，又用作保存预写日志。

设置SparkConf的属性 spark.streaming.receiver.writeAheadLog.enable为真（默认值是假）

在日志被启用以后，所有接收器都获得了能够从可靠收到的数据中恢复的优势。我们建议禁止内存中的复制机制（in-memory replication）（通过在输入流中设置适当的持久等级(persistence level)），因为用于预写日志的容错文件系统很可能也复制了数据。

此外，如果希望可以恢复缓存的数据，就需要使用支持acking的数据源（就像Kafka，Flume和Kinesis一样），并且实现了一个可靠的接收器，它在数据可靠地保存到日志以后，才向数据源确认正确。内置的Kafka和Flume轮询接收器已经是可靠的了。

最后，请注意在启用了预写日志以后，数据接收吞吐率会有轻微的降低。由于所有数据都被写入容错文件系统，文件系统的写入吞吐率和用于数据复制的网络带宽，可能就是潜在的瓶颈了。在此情况下，最好创建更多的接收器增加接收的并行度，和/或使用更好的硬件以增加容错文件系统的吞吐率。










