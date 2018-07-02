# Hbase 配置使用总结

整个配置从小白到入门，踩了无数坑，当然也学到了许多。

整个实习期间，需要熟悉 spark 框架(使用的 pyspark 开发环境(包括其支持的 kafka, Hbase借口类型的数据源 ))。 

## Hbase 基本用途定位 及 相关概念解释。（对于配置文件里面的配置项的理解有帮助）



## Hbase 配置
按照 教程配置的https://www.yiibai.com/hbase/hbase_installation.html

需要额外注意的是，版本对应的问题， 本次配置使用的是  hadoop-2.6.5; hbase-1.2.6

配置时，按照教程给出的，进行设置，需要注意， hadoop/etc/hadoop/下的 core-site.xml 配置：
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
        <>
    </property>
</configuration>

###  emmmm, 再三权衡，本来需要在另外一台机器上配置环境，于是打算重新写一个 详细版本的教程


> 注意包之间的 版本依赖关系；参考 官网 hbase:   https://hbase.apache.org/book.html 

如下：

1. JAVA 环境配置，需求 ( java-8 )  jdk-1.8.0_151
安装 jdk-1.8时，出现一点小插曲，由于我是直接从原服务器上拷贝的 jdk，拷贝到新机器上时，配置好环境变量后，执行 java -version 验证，出现 permission denied 报错。
查验得知，文件夹权限受限； 执行 chmod 命令；chmod 777 jdk1.8.0_151/bin/java   ;然后执行 java -version  解决。



注：
此块参考教程： https://www.yiibai.com/hbase/hbase_installation.html  
不过具体配置，路径有些不一样；


安装之前，先建立和使用 Linux SSH(安全 shell )。 

新建一个用户（可选，用作隔离 hadoop 文件系统，可以的话，推荐；）
sudo useradd username(用户名)
passwd username(用户名)


SSH设置和 密钥生成；
切换到新建用户；(未新建用户，则不用切换)
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys




2. hadoop 安装； 选用的 hadoop-2.6.5

在配置 hadoop 文件之前，先配置下 hadoop 的环境变量；
修改 .bashrc 文件

// hadoop 
export HADOOP_HOME=/home/logkit/hadoop-2.6.5
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME

export HADOOP_OPTS='-Djava.library.path=${HADOOP_HOME}/lib/native'
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_INSTALL=$HADOOP_HOME

修改完配置文件后，source .bashrc 使配置文件立即生效；

Linux 命令行下：
hadoop version  // 验证 hadoop 指令；
hadoop-2.6.5等 诸如 hadoop 版本信息，即配置正确；


hadoop 解压后，进入 /hadoop-2.6.5/etc/hadoop/ 下， 对配置文件进行配置；

配置 hadoop-env.sh 文件中的 JAVA_HOME环境变量；
export JAVA_HOME=/home/logkit/jdk1.8.0_151

先配置 core-site.xml

// 这块定义了 hdfs 文件系统的运行路径；  这个路径要和  hbase 中配置的 一致；
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>

然后配置 hdfs-site.xml
// 这块 就是配置 上面 hdfs 的在本机上的物理地址块的设置
<configuration>
    <property>
        <name>dfs.replication</name >
        <value>1</value>  // 块备份 数量；  分布式容错；
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>file:///home/logkit/hadoopinfra/hdfs/namenode</value>
    </property>  // 配置 hdfs 存储中，namenode 节点的存储地址；
    <property>
        <name>dfs.data.dir</name>
        <value>file:///logkit/hadoop/hadoopinfra/hdfs/datanode</value>
    </property>  // 配置 hdfs 存储中， datanode 节点的存储地址；
</configuration>

配置完上述文件后，在命令行中 输入 start-dfs.sh 执行 dfs启动命令；
若出现，Starting namenodes on [localhost], 然后要求输入 localhost 密码，说明，没有配置 SSH 密钥，按上述 SSH密钥设置。
若出现， localhost: Error： JAVA_HOME is not set and could not be found. 则说明需要配置 hadoop-env.sh 文件中配置 JAVA_HOME环境变量路径；

然后执行 start-dfs.sh ；

正确信息如下：
Starting namenodes on [localhost]
localhost: starting namenode, logging to /home/logkit/....
localhost: starting datanode, logging to /home/lotkit/....
Starting secondary namenodes [0.0.0.0]
0.0.0.0 starting secondarynamenode, logging to /home/logkit/....

然后，命令行运行   
jps   // 查看当前启动进程；
显示：
21958   DataNode
22472   Jps
22174   SeondaryNameNode
(进程号， 名称)




3. hbase 安装； 选用的 hbase-1.2.6

先配置 hbase 环境变量

打开 .bashrc  文件， 添加如下信息：
export PATH=$PATH:/home/logkit/hbase-1.2.6/bin
命令行执行： 
hbase   // 不报错，而是显示 hbase 指令用法即正确；

然后配置 hbase-site.xml 文件
<configuration>
    <property>
        <name>hbase.tmp.dir</name>
        <value>/home/logkit/hbase_tmp/hbaseData</value>  // hbnase 临时文件目录，默认的路径是 系统的 tmp 文件夹，重启系统会丢失文件；
    </property>
    //Here you have to set the path where you want HBase to store its files.
    <property>
        <name>hbase.rootdir</name>
        // 以下 value 按需求只保存一个 
        <value>file:/home/logkit/HBase/HFiles</value>  //  本地文件系统
        <value>hdfs://localhost:9000/hbase</value>   //  hadoop 文件系统，与上述 配置的 hadoop 的 fs.default.name 要一致；后面接一个 /hbase 表示在hadoop 文件系统下的 hbase文件夹下
    </property>
    //Here you have to set the path where you want HBase to store its built in zookeeper files.
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/logkit/zookeeper_property</value>  // zookeeper 管理属性目录
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.regionserver.thrift.compact</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.zookeeper.quorum</name>
        <value>localhost</value>  // zookeeper 管理程序的 ip 端口号，貌似暂时用不到；
    </property>
</configuration>

配置完上述设置后，可以 在命令行运行：
start-hbase.sh  // 因为之前 已经配置 了 habse 的环境变量； 可以直接运行；

create 'test', 'f1'  // 测试 hbase 指令；
若 出现 Error: can't get master address from Zookeeper, znode data == null;
参考：https://blog.csdn.net/hqwang4/article/details/55211555
未初始化  dfs 或者 ，zookeeper 路径问题，搜索对应错误；尝试各种处理方式，即可解决问题。
可以通过查看 jps 启动了哪些，检查是否有进程未启动，然后查看对应的 log 去排错；

一般启动如下两个命令即可；
start-dfs.sh   // 第一次，启动 dfs 后，需要用命令 hdfs namenode -format  初始化 namenode 用以初始化节点。
start-hbase.sh

期间，可以通过jps 查看 启动的进程是否都正确启动。 有报错的，去查看对应的log 信息。


至此，若启动 dfs  hbase 后，进入 hbase shell。
habse shell   // 进入hbase shell  
create 'test', 'f1'  // 如果正确执行该条指令，则说明，本地配置的 hbase 已无问题。

然后，测试本地利用 happybase 访问本地 localhost:9090 的 hbase.

一般只需要如下代码即可验证是否能够正确访问：

import happybase

conn = happybase.Connection( host='localhost', port=9090, protocol='compact' )   // 注意，这里的 port 指代的是 thrift server 运行的端口号。
conn.open()
print( "availbale tables: ", conn.tables() )

若报错  TTrasportException( TSocket read 0 bytes, type=4 )；
则有可能是，port 端口号并非指向的 thrift server 运行的端口号。
执行命令： hbase thrift start -p 9090   // 表示 thrift 命令在 端口 9090 运行；
然后再运行代码。

若报错  TProtocolException() 之类的，则是协议错误，改变 protocol='binary' 或者 protocol='compact' 来测试，再根据错误进一步排错。应该能解决问题。


配置远程访问 设置；https://blog.csdn.net/m0_37138008/article/details/77771582
可以理解为，端口映射的设置； 比较简单；有啥问题，google, 一般也能找到解决方案~



