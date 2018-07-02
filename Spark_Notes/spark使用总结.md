# spark 使用小结

> 第一次整大数据框架，配环境就花了不少时间。 转眼间，实习时间已过半。就总结下这段时间所关注的问题吧。也算为秋招打基础。

## 使用 spark 的目的

业务需求：需要一个实时监听流数据处理平台，hadoop框架有点复杂，且不是很合适本次业务目的；按照leader的想法，spark刚好契合本次目的；

## spark 环境搭建 

编程平台选定的 python;所以后续工作都是用python写的。下载对应的 pyspark 包安装即可。可能需要手动安装 py4j 依赖包。
(由于当时配环境是随便找了个教程配的，现在也没有重新验证网上的方案，就先不放教程链接，日后有时间再补上。 )

前期，安装包，配环境，比较容易，没出啥大问题。就是由于服务器是内网，访问外网各种限制。搞这个就搞了好久。还是实践少了，多操作多实践，就不至于卡在一个点卡好久了。

## spark 框架简介 ( 和 hadoop 的区别就不介绍了，主要讲 主要模块 和 操作流程 )

1. RDD, Accumulators, Broadcasts Vars

2. SQL, DataFrames, DataSets

3. Structured, Streaming

4. Spark Streaming

5. MLib(machine learning)

6. GraphX

7. Spark R


## Resilient Distributed Datasets (RDDs)  弹性分布式数据集

两种创造 RDDs的方法： (需要通过 SparkContext 对象来配置连接的数据源，或者其他配置参数。)

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

(1)直接通过现有数据集合创造(parallelize); 

Parallelized Collections:

    data = [1, 2, 3, 4, 5]
    distData = sc.parallelize(data)

(2)通过从文件系统获取(HDFS, Hbase或通过Hadoop输入格式的数据源)。
可以通过 URI for the file (本地机的文件路径, or a hdfs://, s3a://, etc URI) 
读成 line 的集合。
    
    distFile = sc.textFile("data.txt")

创建之后，distFile 就可以当做 dataset 对象进行操作了。例如，利用 map, reduce 统计所有行的总长度： 

    distFile.map(lambda s: len(s)).reduce(lambda a, b: a + b)

>注：在分布式时，每个机器上，在相同路径下，都需要能够连接上同一个文件。通过复制，或者network-mounted shared file system。

Spark的基于文件的输入方法（包括textFile）都支持在目录，压缩文件和通配符上运行。可以使用textFile（“/ my / directory”），textFile（“/ my / directory / *。txt”）和textFile（“/ my / directory / *。gz”）。

textFile 可以接收第二个参数，用于并行化分片。

python API 还支持

    SparkContext.wholeTextFiles  可以指定目录，读取目录下多个文件。 返回 (filename, content) 形式的数据。
    RDD.saveAsPickleFile 和 SparkContext.pickleFile 支持 pickle 对象数据。

## RDDs Operation

RDDs 有两种类型的操作，transformations 和 Actions；
Transformations 用来在分布式时，由每个work node创造(计算一个新的dataset). Actions 用来最终将计算后的数据，返回给 驱动程序，driver program. 实际环境中，可能会重复利用Action结果,而造成重复计算, 可以通过 persist或catch 来持久化到内存，甚至disk.

> 注： spark分布式时，会分 driver program 和 work node， 可以理解为，一个奴隶主(driver program)，多个工作的奴隶(work node). driver 负责分发任务，汇总结果。 work node 负责真正的分布式计算。

### Transformations
1. map( func )  # func对分布式数据操作。
2. filter( func )   # 过滤数据集，按 func return true的条件过滤。
3. flatMap( func )  # 类似于 map, 但是对返回的结果 做压平处理。比方说 map 操作后结果为[ [1, 2, 3], [2, 4, 3] ]， 那么flatMap对应操作返回[1, 2, 3, 2, 4, 3]
4. mapPartitions( func )  # 分别在每个数据块上运行 map, 实际操作还未用到，不清楚具体应用场景。
5. mapPartitionsWithIndex( func )   # 与 mapPartitions( func ) 类似，多了一个索引值，用以指引。
6. sample( withReplacement, fraction, seed )   # 采样
7. union( otherDataset )   # union, 合并RDD
8. intersection( otherDataset )   # RDD 取交集。
9. distinct( [numPartitions]) )   # 
10. groupByKey( [numPartitions] )  # 聚合RDD
11. reduceByKey( func, [numPartitions] )  # 对键值对操作，按键操作.第二个 参数 设置分片数。
12. aggregateByKey( zeroValue )(seqOp, combOp, [numPartitions] )  #  未使用过，待续。。。
13. sortByKey( [ascending], [numPartitions] )  # 按键排序。
14. join( otherDataset, [numPartitions] ) # 连接操作。 当对 (k,v) (k,w) 两种数据集操作时，得到( k, (v,w) )
15. cogroup( otherDataset, [numPartitions] )  #  type (K, V) and (K, W), returns (K, (Iterable<V>, Iterable<W>)) tuples.
16. cartesian( otherDataset )   # T and U, returns (T, U) pairs (all pairs of elements).
17. pipe( command, [envVars] )  # 未使用过。
18. coalesce( numPartitions )   # 减少分片数，通常用在 filter 过滤掉大量数据后，减少分片数，提高效率。
19. repartition( numPartitions )   # shuffle data, 然后重新分片。
20. repartitionAndSortWithinPartitions( partitioner )   # 重新分片后sort, 比单独分片，然后sort，效率高。


### Actions
1. reduce(func)   # 聚合 数据集
2. collect()  # Return all the elements of the dataset as an array at the driver program. 此方法慎用，数据量大时，对 driver 内存要求很高。容易爆内存错。
3. count() # 对 dataset 中元素 计数。
4. first()  # 取 dataset 中第一个元素
5. take(n)  # 取 前 n 个元素。
6. takeSample(withReplacement, num, [seed])   # 采样，设置是否替换(这里不懂，具体的替换指的啥？替换什么，替换源数据么？)
7. takeOrdered(n, [ordering])   # 按 dataset 的自然顺序 或者 某个指定 比较函数 的 顺序取 前 n 个样本。
8. saveAsTextFile(path)    # 
9. saveAsSequenceFile(path) (Java and Scala)
10. saveAsObjectFile(path)  (Java and Scala)
11. countByKey()
12. foreach(func)  # Run a function func on each element of the dataset. 

> 注意： shuffle 操作 代价很大。 spark 中某些操作涉及到 shuffle 操作。 导致shuffle的操作,例如,重新分区: repartition 和 coalesce, ByKey 操作(除了 counting) like groupByKey and reduceByKey, and join operations like cogroup and join.

### Shuffle operations

Shuffle 操作在 spark分布式 中涉及 到 跨进程，甚至跨机器的 copy 数据进行打乱，开销巨大。


> RDDs持久化。前面提到一个操作  persist 和 catch 是将RDDs存储在 内存中，以备后续使用。避免重新计算。  RDDs持久化，还可以通过配置其他参数，来实现不同层级的持久化。

***

local 设置项，表示本地运行 one thread. local[n] 表示 本地运行 n threads

                          Quick Start: a quick introduction to the Spark API; start here!
                RDD Programming Guide: overview of Spark basics - RDDs (core but old API), accumulators, and broadcast variables
  Spark SQL, Datasets, and DataFrames: processing structured data with relational queries (newer API than RDDs)
                 Structured Streaming: processing structured data streams with relation queries (using Datasets and DataFrames, newer API than DStreams)
                      Spark Streaming: processing data streams using DStreams (old API)
                                
                                MLlib: applying machine learning algorithms
                               GraphX: processing graphs

RDDs 最基础，最核心的 API(也是最早的，old的API)；
Spark SQL, Datasets, DataFrames, 比 RDDs 要新的 API，用来处理结构化查询（ relational queries ）

Spark Streaming 处理数据流(data streams )利用 DStreams( old API )
Structured Streaming, 处理 结构化数据流( structured data streams )利用 ( relation queries ( 基于 Datasets, DataFrames, 比 DStream API要新 ) )

MLlib 和 GraphX 是两个计算库； 处理机器学习 和 图计算相关的。

> 小结：比较有趣的一点是，RDDs 和 Spark SQL， Datasets, DataFrames,  与  Spark Streaming 和 Structured Streaming 一样，都是由基础的 数据，到 结构化数据 的区别，类似的操作。

***

## Spark SQL, DataFrames, Datasets

spark 数据入口：  通过 SparkSession class 来接入数据。  
spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()



数据接入有两种方式:   create DataFrames from an existing RDD, from a Hive table, or from Spark data sources.
1. From an existing RDD.  

        from pyspark.sql import Row
        sc = spark.sparkContext
        lines = sc.textFile("examples/src/main/resources/people.txt")
        parts = lines.map(lambda l: l.split(","))
        people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))
        schemaPeople = spark.createDataFrame(people)
        schemaPeople.createOrReplaceTempView("people")

2. From Spark data sources.












