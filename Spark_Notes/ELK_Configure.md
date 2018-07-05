# ELK 环境搭配记录
（基于 JDK-1.8）
安装参考链接：https://caidezhi.gitbooks.io/elk-getting-started-guide/

ELK 总共包括 三个组件: Elasticsearch, Logstash, Kibana.

功能定位为：
1. Elasticsearch
基于 Lucence 的搜索服务器，提供 分布式 多用户的 全文搜索引擎。

2. Logstash
对 日志收集分析处理，并存储以供后期使用。

3. Kibana
汇总、分析和搜索重要数据日志并提供友好的web界面。为 Logstash 和 ElasticSearch 提供的日志分析的 Web 界面。


# 实际生产环境搭配。

由于业务需求是，需要通过sparK 实时监听 kafka 端口的消息队列，对消息队列的消息实时处理分析，然后将分析的结果，以页面的形式展示出来，供业务部门人员参考利用。故需要用到 Elasticsearch 和 Kibana 这两个。

## Elasticsearch 安装

下载对应的 *.tar.gz 包， 利用  tar -xvf *.tar.gz 解压安装；
配置 PATH 环境变量，以便后续启动指令。

## Kibana 安装
下载对应的 *.tar.gz 包， 利用 tar -xzf *.tar.gz 解压安装；
配置 PATH 环境变量。








