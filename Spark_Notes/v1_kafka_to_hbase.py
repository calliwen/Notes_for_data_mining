# coding:utf-8


from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession, Row
from pyspark.sql import SparkSession
from pyspark.sql.function import explode, split

import sys
import time
import json
import re

import gc
import happybase

class HB_conn():
    def __init__(self):
        self.conn = happybase.Connection( host='', port=9090, protocol='compact' )
        self.conn.open()
        # print( self.conn.tables() ) # 打印 hbase 数据库中的表
    def get_tables(self):
        if not self.conn:
            self.conn.open()
        tables_list = self.conn.tables()
        return tables_list
    def create_table(self, table_name='min_test', cf={ 'content':dict(), 'summary':dict() } ):
        if not self.conn:
            self.conn.open()
        if table_name not in self.conn.tables():
            self.conn.create_table( table_name, cf )
        return
    def get_table(self, table_name='min_test'):
        if not self.conn:
            self.conn.open()
        table = self.conn.table( table_name )
        return table
    def put_data(self, table, raw_key, data_dict ):
        table.put( row=raw_key, data=data_dict )
        return

# lazily instantiated global instance of SparkSession
def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingleletonInstance" not in globals() ):
        globals()['sparkSessionSingleletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingleletonInstance']
# DataFrame
def process(time, rdd, table_name):
    print("*********{}**{}***********".format( str(time), table_name ))
    try:
        spark = getSparkSessionInstance( rdd.context.getConf() )
        rowRdd = rdd.coalesce(1).map( lambda w: Row( ProductType=w['ProductType'],
                                                     Version=w['Version'],
                                                     FaultID=w['FaultID'],
                                                     QuesID=w['QuesID'],
                                                     Timestamps=w['Timestamps'] ) )
        try:
            TyepProduct_count = spark.createDataFrame( rowRdd )
        except:
            print( "Error: RDD is None !!! " )
        try:
            TypeProduct_count = createOrReplaceTempView('TypeProduct_count')
            print( "df type: ", type(TypeProduct_count) )
            TypeProduct_count.show()

            res = TyepProduct_count.groupby( ['FaultID', 'ProductType'] ).agg( { "*":"count" } ).collect()
            FaultID_count = TypeProduct_count.grouby('FaultID').agg( {"*":"count"} ).collect()
            ProdType_count = TypeProduct_count.groupby('ProductType').agg( {"*":"count"} ).collect()
            # 总数统计
            all_count = TypeProduct_count.count()
        except:
            print( "Error: statistics df error !!! " )
        try:
            conn = HB_conn()
            conn.create_table( table_name )
            table = conn.get_table( table_name )
            for raw in res:
                data_dict = { bytes( "content:"+bytes(raw['FaultID'])+bytes(raw['ProductType']) ): bytes(raw['count(1)']) }
                table.put( row=bytes(time), data=data_dict )
                print( str(time), raw['FaultID'], raw['ProductType'], raw['count(1)'] )
            for raw in FaultID_count:
                data_dict = { bytes( "summary:"+"FaultID_"+bytes(raw['FaultID']) ):bytes(raw['count(1)']) }
                table.put( row=bytes(time), data=data_dict )
                print( str(time), raw['FaultID'], raw['count(1)'] )
            for raw in ProdType_count:
                data_dict = { bytes("summary:"+"ProductID_"+bytes(raw['ProductType'])): bytes(raw['count(1)']) }
                table.put( row=bytes(time), data=data_dict )
                print( str(time), raw['ProductType'], raw['count(1)'] )
            data_dict = { bytes("summary:Total_Count"):bytes(all_count) }
            table.put( row=bytes(time), data=data_dict )    
            del conn
            gc.collect()
            print( "get done !!! " )
        except:
            print( "Error: operat hbase error !!! " )
    except:
        print( "Warnning: process is None !!! " )
        pass

def ragexMatch_split_msg( msg ):
    def regex_match(pattern, test_str):
        res = re.compile( pattern ).findall( test_str )
        if len(res) >=1:
            return res[0]
        else:
            return "--None_Match--"
    # HIM-AL00_HIM-ALOO 8.0.0.31(SP1C00D37R1P37log)_ID101_QUES73521027_D3H7N17818000330_20180620100929_BetaClub.zip
    ProVer_pattern = r'-[A-Z]+[0-9]+_'
    VerNum_pattern = r'_.+\)_'
    FaultID_pattern = r'_ID[0-9]+_'

    QuesID_pattern = r'_QUES[0-9]+_'
    MSG_pattern = r'[0-9]+_[A-Z0-9]+_[0-9]'
    TIME_pattern = r'_[0-9]+_'
    ZIP_pattern = r'_[a-zA-Z]+.zip'

    datas = {
        "ProductType" : msg.split('-')[0],
            "Version" : msg.split('_ID')[0],
            "FaultID" : regex_match( FaultID_pattern, msg)[1:-1],
             "QuesID" : regex_match( QuesID_pattern, msg )[1:-1],
         "Timestamps" : regex_match( TIME_pattern, msg )[1:-1]
    }
    return datas

if __name__ == "__main__":
    sc_conf = SparkConf()
    sc_conf = setAppName( "finance-similarity-app" )
    sc_conf.set( "spark.driver.memory", '16g' )
    # sc_conf.set( "spark.executor.memroy", '8g' )
    # sc_conf.set( "spark.executor.cores", '2' )
    # sc_conf.set( "spark.cores.max", '40' )
    sc_conf.set( "spark.logConf", True )
    sc_conf.set( "spark.default.parallelism", '2' ) 
    sc = SparkContext( conf=sc_conf )
    sc.setLogLevel('WARN')

    checkpointDirectory = str("./checkPoint_dir")
    ssc.checkpoint( checkpointDirectory )

    zk_server = ''
    broker_list = ''
    topic = ''

    # kvs = KafkaUtils.createStream( ssc, zkQuorum=zk_server, groupID='consumer_name', topics={topic:1} )
    kvs = KafkaUtils.createDirectStream( ssc, [ topic ], { "metadata.broker.list", broker_list} )
    filename_lines = kvs.map( lambda x: json.loads( x[1] ) ).map(  lambda x: x['filename'] )\
                        .filter( lambda x: x['filename'].count("BetaClub.zip")==1 )\
                        .filter( lambda x: x['filename'].count("ID")==1 )
    FileName_dict = filename_lines.map( ragexMatch_split_msg )

    one_min_windows = FileName_dict.window( 60, 60 )
    two_min_windows = one_min_windows.window( 120, 120 )
    print( "one_min_windows type: ", type(one_min_windows) )

    one_min_windows.foreachRDD( lambda time, rdd: process( time, rdd, table_name='test_one_min' ) )    
    two_min_windows.foreachRDD( lambda time, rdd: process( time, rdd, table_name='test_two_min' ) )    

    ssc.start()
    ssc.awaitTermination()
    
