# coding=utf-8
import time  #
from os import system
from influxdb import InfluxDBClient  # 导入python-influxdb库
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('/home/k8s-master/monitor/monitor.ini'))
hostname = config.get("BasicInfo", "hostname")
masterip = config.get("BasicInfo", "masterip")
influxdb_port = config.get("Monitor", "influxdb_port")
influxdb_username = config.get("Monitor", "influxdb_username")
influxdb_dbname = config.get("Monitor", "influxdb_dbname")

client = InfluxDBClient(masterip, influxdb_port, influxdb_username, '', influxdb_dbname)  # 连接数据库。

#查询所有的Pod
def GetAllPods():
    Sql_AllPods = 'show tag values from "uptime" with key = "pod_name"'  # uptime意为运行时间，所有要查询的对象都有这个指标，所以以它来查询集群内所有的pods、nodes得到的数据更为可靠，Sql保存查询语句
    AllPods = client.query(Sql_AllPods)  # 利用Sql查询数据库
    AllPods = list(AllPods.get_points())  # 将AllPods转为list结构，其保存的内容为dict结构对象
    return AllPods

#查询当前节点Pod
def GetLocalPods():
    Sql_LocalPods = 'show tag values from "uptime" with key = "pod_name" where "nodename" = ' + "'" + hostname + "'"
    LocalPods = client.query(Sql_LocalPods)
    LocalPods = list(LocalPods.get_points())
    return LocalPods

#查询所有的Node
def GetAllNodes():
    Sql_AllNodes = 'show tag values from "uptime" with key = "nodename"'
    AllNodes = client.query(Sql_AllNodes)
    AllNodes = list(AllNodes.get_points())
    return AllNodes

#单Pod单Measurement查询
def EasyPodQuery(PodName, Measurement):
    Easy_sql = 'select "value"::field from "' + Measurement + '" where "pod_name" = ' + "'" + PodName + "'" +  ' order by time desc limit 1'
    Result = client.query(Easy_sql)
    Result = list(Result.get_points())
    return Result

#单Node单Measurement查询
def EasyNodeQuery(NodeName, Measurement):
    Easy_sql = 'select "value"::field from "' + Measurement + '" where "nodename" = ' + "'" + NodeName + "'" + ' order by time desc limit 1'
    Result = client.query(Easy_sql)
    Result = list(Result.get_points())
    return Result

#彩色高亮输出
def Coprint(type,co, str):
    print "\033[%d;%dm%s\033[0m" % (type, co, str)

# 时间转换函数-将零时区的时间转换到八时区
def TimeAdjust(a):
    # 传入的类型为unicode，格式为%Y-%m-%dT%H:%M:%SZ先转类型，字符串处理，转为时间戳，增加8个市区的时间差值，再转回来
    a = a.encode('unicode-escape').decode('string_escape')
    a = a.replace("T", " ").replace("Z", "")
    a = time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S'))
    a = int(a) + 28800
    format = '%Y-%m-%d %H:%M:%S'
    a = time.localtime(a)
    a = time.strftime(format, a)
    return a

#######################################################################################################################################################################################################
## 查询包括所有在InfluxDB中k8s数据库可得到的measurement，主要针对POD层。若某个measurement无需或无法对pod层查询，则相应改为node层查询（如对于cpu/odeallocatable这一measurement，则对node层进行查询）。##
## 若对某measurement的查询有特定需求则进行相应更改                                                                                                                                                   ##
## 查询函数的命名格式为Print+查询具体measurement名字，以“/”、“_”作为分界的单词首字母大写，如cpu/usage_rate的查询函数为PrintCpuUsageRate().                                                           ##
#######################################################################################################################################################################################################

AllPods = GetAllPods()
LocalPods = GetLocalPods()
AllNodes = GetAllNodes()

# Fast Query

# CPU部分包括以下6种measurement可供查询
# cpu/usage_rate        		CPU usage on all cores in millicores.
# cpu/usage             		Cumulative CPU usage on all cores.
# cpu/limit             		CPU hard limit in millicores.
# cpu/request           		CPU request (the guaranteed amount of resources) in millicores.
# cpu/nodeallocatable   		Cpu allocatable of a node.
# cpu/nodecapacity      		Cpu capacity of a node.
# cpu/nodereservation   		Share of cpu that is reserved on the node allocatable.
# cpu/nodeutilization   		CPU utilization as a share of node allocatable.

# cpu/usage_rate查询
def PrintCpuUsageRate():
    print 'Cpu/Usage_Rate Of Each pod'
    Coprint(1, 30,'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):  # 逐个读取pod及其相应指标，正确转换时间并输出
        CpuUsageRate = EasyPodQuery(AllPods[index]['value'], "cpu/usage_rate")
        CpuUsageRate[0]['time'] = TimeAdjust(CpuUsageRate[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], CpuUsageRate[0]['time'], CpuUsageRate[0]['value'])
    return


# cpu/usage查询
def PrintCpuUsage():
    print 'Cpu/Usage Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        CpuUsage = EasyPodQuery(AllPods[index]['value'], "cpu/usage")
        CpuUsage[0]['time'] = TimeAdjust(CpuUsage[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], CpuUsage[0]['time'], CpuUsage[0]['value'])
    return


# cpu/limit查询
def PrintCpuLimit():
    print 'Cpu/Limit Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        CpuLimit = EasyPodQuery(AllPods[index]['value'], "cpu/limit")
        CpuLimit[0]['time'] = TimeAdjust(CpuLimit[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], CpuLimit[0]['time'], CpuLimit[0]['value'])
    return


# cpu/request查询
def PrintCpuRequest():
    print 'Cpu/Request Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        CpuRequest = EasyPodQuery(AllPods[index]['value'], "cpu/request")
        CpuRequest[0]['time'] = TimeAdjust(CpuRequest[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], CpuRequest[0]['time'], CpuRequest[0]['value'])
    return

#EasyNodeQuery
# cpu/nodeallocatable查询
def PrintCpuNodeAllocatable():
    print 'Cpu/NodeAllocatable of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):  # 逐个读取node及其相应指标并输出
        CpuNodeAllocatable = EasyNodeQuery(AllNodes[index]['value'], "cpu/node_allocatable")
        CpuNodeAllocatable[0]['time'] = TimeAdjust(CpuNodeAllocatable[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], CpuNodeAllocatable[0]['time'], CpuNodeAllocatable[0]['value'])
    return


# cpu/nodecapacity查询
def PrintCpuNodeCapacity():
    print 'Cpu/NodeCapacity of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        CpuNodeCapacity = EasyNodeQuery(AllNodes[index]['value'], "cpu/node_capacity")
        CpuNodeCapacity[0]['time'] = TimeAdjust(CpuNodeCapacity[0]['time'])
        print "%-31s %-24s %-4d" % (AllNodes[index]['value'], CpuNodeCapacity[0]['time'], CpuNodeCapacity[0]['value'])
    return


# cpu/nodereservation查询
def PrintCpuNodeReservation():
    print 'Cpu/NodeReservation of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        CpuNodeReservation = EasyNodeQuery(AllNodes[index]['value'], "cpu/node_reservation")
        CpuNodeReservation[0]['time'] = TimeAdjust(CpuNodeReservation[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], CpuNodeReservation[0]['time'], CpuNodeReservation[0]['value'])
    return


# cpu/nodeutilization查询
def PrintCpuNodeUtilization():
    print 'Cpu/NodeUtilization of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        CpuNodeUtilization = EasyNodeQuery(AllNodes[index]['value'], "cpu/node_utilization")
        CpuNodeUtilization[0]['time'] = TimeAdjust(CpuNodeUtilization[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], CpuNodeUtilization[0]['time'], CpuNodeUtilization[0]['value'])
    return


# Filesystem部分包括以下4种measurement可供查询
# filesystem/inodes              The number of available inodes in a the filesystem
# filesystem/inodesFree   		The number of free inodes remaining in a the filesystem.
# filesystem/limit               The total size of filesystem in bytes.
# filesystem/usage 	            Total number of bytes consumed on a filesystem.

# filesystem/inodes查询
def PrintFilesystemInodes():
    print 'Filesystem/Inodes of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        FilesystemInodes = EasyNodeQuery(AllNodes[index]['value'], "filesystem/inodes")
        FilesystemInodes[0]['time'] = TimeAdjust(FilesystemInodes[0]['time'])
        print "%-31s %-24s %-4d" % (AllNodes[index]['value'], FilesystemInodes[0]['time'], FilesystemInodes[0]['value'])
    return


# filesystem/inodesFree查询
def PrintFilesystemInodesFree():
    print 'Filesystem/InodesFree of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        FilesystemInodesFree = EasyNodeQuery(AllNodes[index]['value'], "filesystem/inodes_free")
        FilesystemInodesFree[0]['time'] = TimeAdjust(FilesystemInodesFree[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], FilesystemInodesFree[0]['time'], FilesystemInodesFree[0]['value'])
    return


# filesystem/limit查询
def PrintFilesystemLimit():
    print 'Filesystem/Limit of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        FilesystemLimit = EasyPodQuery(AllPods[index]['value'], "filesystem/limit")
        FilesystemLimit[0]['time'] = TimeAdjust(FilesystemLimit[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], FilesystemLimit[0]['time'], FilesystemLimit[0]['value'])
    return


# filesystem/usage查询
def PrintFilesystemUsage():
    print 'Filesystem/Usage of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        FilesystemUsage = EasyPodQuery(AllPods[index]['value'], "filesystem/usage")
        FilesystemUsage[0]['time'] = TimeAdjust(FilesystemUsage[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], FilesystemUsage[0]['time'], FilesystemUsage[0]['value'])
    return


# Memory部分包括以下14种measurement可供查询
# memory/cache                           Cache memory usage.
# memory/limit                           Memory hard limit in bytes.
# memory/major_page_faults               Number of major page faults.
# memory/major_page_faults_rate          Number of major page faults per second.
# memory/node_allocatable                Memory allocatable of a node.
# memory/node_capacity                   Memory capacity of a node.
# memory/node_reservation                Share of memory that is reserved on the node allocatable.
# memory/node_utilization                Memory utilization as a share of memory allocatable.
# memory/page_faults                     Number of page faults.
# memory/page_faults_rate                Number of page faults per second.
# memory/request                         Memory request (the guaranteed amount of resources) in bytes.
# memory/rss                             RSS memory usage.
# memory/usage                           Total memory usage.
# memory/working_set                     Total working set usage. Working set is the memory being used and not easily dropped by the kernel.

# memory/cache查询
def PrintMemoryCache():
    print 'Memory/Cache Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryCache = EasyPodQuery(AllPods[index]['value'], "memory/cache")
        MemoryCache[0]['time'] = TimeAdjust(MemoryCache[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryCache[0]['time'], MemoryCache[0]['value'])
    return


# memory/limit查询
def PrintMemoryLimit():
    print 'Memory/Limit Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryLimit = EasyPodQuery(AllPods[index]['value'], "memory/limit")
        MemoryLimit[0]['time'] = TimeAdjust(MemoryLimit[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryLimit[0]['time'], MemoryLimit[0]['value'])
    return


# memory/major_page_faults查询
def PrintMemoryMajorPageFaults():
    print 'Memory/MajorPageFaults Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryMajorPageFaults = EasyPodQuery(AllPods[index]['value'], "memory/major_page_faults")
        MemoryMajorPageFaults[0]['time'] = TimeAdjust(MemoryMajorPageFaults[0]['time'])
        print "%-41s %-23s %-3d" % (
        AllPods[index]['value'], MemoryMajorPageFaults[0]['time'], MemoryMajorPageFaults[0]['value'])
    return


# memory/major_page_faults_rate查询
def PrintMemoryMajorPageFaultsRate():
    print 'Memory/MajorPageFaultsRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryMajorPageFaultsRate = EasyPodQuery(AllPods[index]['value'], "memory/major_page_faults_rate")
        MemoryMajorPageFaultsRate[0]['time'] = TimeAdjust(MemoryMajorPageFaultsRate[0]['time'])
        print "%-41s %-23s %-3d" % (
        AllPods[index]['value'], MemoryMajorPageFaultsRate[0]['time'], MemoryMajorPageFaultsRate[0]['value'])
    return


# memory/node_allocatable查询
def PrintMemoryNodeAllocatable():
    print 'Memory/NodeAllocatable of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        MemoryNodeAllocatable = EasyNodeQuery(AllNodes[index]['value'], "memory/node_allocatable")
        MemoryNodeAllocatable[0]['time'] = TimeAdjust(MemoryNodeAllocatable[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], MemoryNodeAllocatable[0]['time'], MemoryNodeAllocatable[0]['value'])
    return


# memory/node_capacity查询
def PrintMemoryNodeCapacity():
    print 'Memory/NodeCapacity of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        MemoryNodeCapacity = EasyNodeQuery(AllNodes[index]['value'], "memory/node_capacity")
        MemoryNodeCapacity[0]['time'] = TimeAdjust(MemoryNodeCapacity[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], MemoryNodeCapacity[0]['time'], MemoryNodeCapacity[0]['value'])
    return


# memory/node_reservation查询
def PrintMemoryNodeReservation():
    print 'Memory/NodeReservation of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        MemoryNodeReservation = EasyNodeQuery(AllNodes[index]['value'], "memory/node_reservation")
        MemoryNodeReservation[0]['time'] = TimeAdjust(MemoryNodeReservation[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], MemoryNodeReservation[0]['time'], MemoryNodeReservation[0]['value'])
    return


# memory/node_utilization查询
def PrintMemoryNodeUtilization():
    print 'Memory/NodeUtilization of Each Node'
    Coprint(1, 30, 'NodeName\t\t\tLastUpdateTime\t\tValue')
    for index in range(len(AllNodes)):
        MemoryNodeUtilization = EasyNodeQuery(AllNodes[index]['value'], "memory/node_utilization")
        MemoryNodeUtilization[0]['time'] = TimeAdjust(MemoryNodeUtilization[0]['time'])
        print "%-31s %-24s %-4d" % (
        AllNodes[index]['value'], MemoryNodeUtilization[0]['time'], MemoryNodeUtilization[0]['value'])
    return


# memory/page_faults查询
def PrintMemoryPageFaults():
    print 'Memory/PageFaults Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryPageFaults = EasyPodQuery(AllPods[index]['value'], "memory/page_faults")
        MemoryPageFaults[0]['time'] = TimeAdjust(MemoryPageFaults[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryPageFaults[0]['time'], MemoryPageFaults[0]['value'])
    return


# memory/page_faults_rate查询
def PrintMemoryPageFaultsRate():
    print 'Memory/PageFaultsRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryPageFaultsRate = EasyPodQuery(AllPods[index]['value'], "memory/page_faults_rate")
        MemoryPageFaultsRate[0]['time'] = TimeAdjust(MemoryPageFaultsRate[0]['time'])
        print "%-41s %-23s %-3d" % (
        AllPods[index]['value'], MemoryPageFaultsRate[0]['time'], MemoryPageFaultsRate[0]['value'])
    return


# memory/request查询
def PrintMemoryRequest():
    print 'Memory/Request Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryRequest = EasyPodQuery(AllPods[index]['value'], "memory/request")
        MemoryRequest[0]['time'] = TimeAdjust(MemoryRequest[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryRequest[0]['time'], MemoryRequest[0]['value'])
    return


# memory/rss查询
def PrintMemoryRss():
    print 'Memory/Rss Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryRss = EasyPodQuery(AllPods[index]['value'], "memory/rss")
        MemoryRss[0]['time'] = TimeAdjust(MemoryRss[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryRss[0]['time'], MemoryRss[0]['value'])
    return


# memory/usage查询
def PrintMemoryUsage():
    print 'Memory/Usage Of Each Pod 单位为字节'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryUsage = EasyPodQuery(AllPods[index]['value'], "memory/usage")
        MemoryUsage[0]['time'] = TimeAdjust(MemoryUsage[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryUsage[0]['time'], MemoryUsage[0]['value'])
    return


# memory/working_set查询
def PrintMemoryWorkingSet():
    print 'Memory/WorkingSet Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        MemoryWorkingSet = EasyPodQuery(AllPods[index]['value'], "memory/working_set")
        MemoryWorkingSet[0]['time'] = TimeAdjust(MemoryWorkingSet[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], MemoryWorkingSet[0]['time'], MemoryWorkingSet[0]['value'])
    return


# network部分包括以下8种measurement可供查询
# network/rx                         Cumulative number of bytes received over the network.
# network/rx_errors                  Cumulative number of errors while receiving over the network.
# network/rx_errors_rate   	        Number of errors while receiving over the network per second.
# network/rx_rate                    Number of bytes received over the network per second.
# network/tx                         Cumulative number of bytes sent over the network.
# network/tx_errors                  Cumulative number of errors while sending over the network.
# network/tx_errors_rate             Number of errors while sending over the network.
# network/tx_rate                    Number of bytes sent over the network per second.

# network/rx查询
def PrintNetworkRx():
    print 'Network/Rx Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkRx = EasyPodQuery(AllPods[index]['value'], "network/rx")
        NetworkRx[0]['time'] = TimeAdjust(NetworkRx[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkRx[0]['time'], NetworkRx[0]['value'])
    return


# network/rx_errors查询
def PrintNetworkRxErrors():
    print 'Network/RxErrors Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkRxErrors = EasyPodQuery(AllPods[index]['value'], "network/rx_errors")
        NetworkRxErrors[0]['time'] = TimeAdjust(NetworkRxErrors[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkRxErrors[0]['time'], NetworkRxErrors[0]['value'])
    return


# network/rx_errors_rate
def PrintNetworkRxErrorsRate():
    print 'Network/RxErrorsRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkRxErrorsRate = EasyPodQuery(AllPods[index]['value'], "network/rx_errors_rate")
        NetworkRxErrorsRate[0]['time'] = TimeAdjust(NetworkRxErrorsRate[0]['time'])
        print "%-41s %-23s %-3d" % (
        AllPods[index]['value'], NetworkRxErrorsRate[0]['time'], NetworkRxErrorsRate[0]['value'])
    return


# network/rx_rate
def PrintNetworkRxRate():
    print 'Network/RxRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkRxRate = EasyPodQuery(AllPods[index]['value'], "network/rx_rate")
        NetworkRxRate[0]['time'] = TimeAdjust(NetworkRxRate[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkRxRate[0]['time'], NetworkRxRate[0]['value'])
    return


# network/tx
def PrintNetworkTx():
    print 'Network/Tx Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkTx = EasyPodQuery(AllPods[index]['value'], "network/tx")
        NetworkTx[0]['time'] = TimeAdjust(NetworkTx[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkTx[0]['time'], NetworkTx[0]['value'])
    return


# network/tx_errors
def PrintNetworkTxErrors():
    print 'Network/TxErrors Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkTxErrors = EasyPodQuery(AllPods[index]['value'], "network/tx_errors")
        NetworkTxErrors[0]['time'] = TimeAdjust(NetworkTxErrors[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkTxErrors[0]['time'], NetworkTxErrors[0]['value'])
    return


# network/tx_errors_rate
def PrintNetworkTxErrorsRate():
    print 'Network/TxErrorsRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkTxErrorsRate = EasyPodQuery(AllPods[index]['value'], "network/tx_errors_rate")
        NetworkTxErrorsRate[0]['time'] = TimeAdjust(NetworkTxErrorsRate[0]['time'])
        print "%-41s %-23s %-3d" % (
        AllPods[index]['value'], NetworkTxErrorsRate[0]['time'], NetworkTxErrorsRate[0]['value'])
    return


# network/tx_rate
def PrintNetworkTxRate():
    print 'Network/TxRate Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        NetworkTxRate = EasyPodQuery(AllPods[index]['value'], "network/tx_rate")
        NetworkTxRate[0]['time'] = TimeAdjust(NetworkTxRate[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], NetworkTxRate[0]['time'], NetworkTxRate[0]['value'])
    return


# uptime measurement
# uptime Number of milliseconds since the container was started.

# uptime查询
def PrintUptime():
    print 'Uptime Of Each Pod'
    Coprint(1, 30, 'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    for index in range(len(AllPods)):
        Uptime = EasyPodQuery(AllPods[index]['value'], "uptime")
        Uptime[0]['time'] = TimeAdjust(Uptime[0]['time'])
        print "%-41s %-23s %-3d" % (AllPods[index]['value'], Uptime[0]['time'], Uptime[0]['value'])
    return

#2018/4/15
# Single Pod Query

#单Pod详尽查询
def PrintSinglePodInfoo(PodName):
    Sql_PodBasicInfo = 'show tag values from "uptime" with key in ("namespace_name", "nodename", "") where "pod_name" = ' + "'" + PodName + "'"
    PodBasicInfo = client.query(Sql_PodBasicInfo)
    PodBasicInfo = list(PodBasicInfo.get_points())
    PodValueList = ComprehensiveQueryOnPod(PodName)
    FormatPrint(PodBasicInfo[0]['value'], PodName, PodBasicInfo[1]['value'], PodValueList)

#单Pod全面Measurement查询
def ComprehensiveQueryOnPod(Podname):
    TagList = ["cpu/limit", "cpu/request", "cpu/usage_rate", "cpu/usage","filesystem/limit", "filesystem/usage","memory/cache", "memory/limit", "memory/major_page_faults", "memory/major_page_faults_rate", "memory/page_faults", "memory/page_faults_rate", "memory/request", "memory/rss", "memory/usage", "memory/working_set", "network/rx", "network/rx_errors", "network/rx_errors_rate", "network/rx_rate", "network/tx", "network/tx_errors", "network/tx_errors_rate", "network/tx_rate", "uptime"]
    TagValue = []
    for index in range(len(TagList)):
        Temp = EasyPodQuery(Podname, TagList[index])
        TagValue.append(Temp[0]['value'])

    return TagValue

#格式化输出
def FormatPrint(Namespace_name,Pod_name, Nodename, PodValueList):
    Coprint(1, 30, 'PodName')
    Coprint(0, 32, "%s" %(Pod_name))
    print ''
    Coprint(1, 30, 'Namespace\tName\t\t\t\t\tNode\t\tUptime')
    Coprint(0, 30, "%-15s %-39s %-15s %-15d" % (Namespace_name, Pod_name, Nodename, PodValueList[24]))
    print("-----------")
    Coprint(1, 30, 'Cpu/limit\tCpu/request\tCpu/usage_rate\tCpu/usage')
    Coprint(0, 30, "%-15d %-15d %-15d %-15d" % (PodValueList[0], PodValueList[1], PodValueList[2], PodValueList[3]))
    print("-----------")
    Coprint(1, 30, 'Filesystem/limit\tFilesystem/usage')
    Coprint(0, 30, "%-23d %-15d" % (PodValueList[4], PodValueList[5]))
    print("-----------")
    Coprint(1, 30, 'Memory/limit\tMemory/request\tMemory/usage\tMemory/cache\tMemory/rss\tMemory/working_set')
    Coprint(0, 30, "%-15d %-15d %-15d %-15d %-15d %-15d" % (PodValueList[7], PodValueList[12], PodValueList[14], PodValueList[6], PodValueList[13], PodValueList[15]))
    Coprint(1, 30, 'Memory/major_page_faults\tMemory/major_page_faults_rate\tMemory/page_faults\tMemory/page_faults_rate')
    Coprint(0, 30, "%-31d %-31f %-23d %-20f" %(PodValueList[8], PodValueList[9], PodValueList[10], PodValueList[11]))
    print("-----------")
    Coprint(1, 30, 'Network/rx\tNetwork/rx_rate\tNetwork/rx_errors\tNetwork/rx_errors_rate')
    Coprint(0, 30, "%-15d %-15f %-23d %-15f" % (PodValueList[16], PodValueList[19], PodValueList[17], PodValueList[18]))
    Coprint(1, 30, ('Network/tx\tNetwork/tx_rate\tNetwork/tx_errors\tNetwork/tx_errors_rate'))
    Coprint(0, 30, "%-15d %-15f %-23d %-15f" % (PodValueList[20], PodValueList[23], PodValueList[21], PodValueList[22]))

    return

#2018/4/23

#Cpu/usage_rate sort
def PrintCpuUsageRateSort():
    Sql_LocalPods = 'show tag values from "uptime" with key = "pod_name" where "nodename" = ' + "'" + hostname + "'" 
    LocalPods = client.query(Sql_LocalPods)
    LocalPods = list(LocalPods.get_points())
    print 'Cpu/Usage_Rate Of Each Pod In ' + hostname
    Coprint(1, 30,'PodName\t\t\t\t\t  LastUpdateTime\t  Value')
    CpuUsageRateVSort = {}
    CpuUsageRateTSort = {}
    for index in range(len(LocalPods)):  # 逐个读取pod及其相应指标，正确转换时间并输出
        CpuUsageRate = EasyPodQuery(LocalPods[index]['value'], "cpu/usage_rate")
        CpuUsageRate[0]['time'] = TimeAdjust(CpuUsageRate[0]['time'])
	CpuUsageRateVSort[LocalPods[index]['value']] = CpuUsageRate[0]['value']
	CpuUsageRateTSort[LocalPods[index]['value']] = CpuUsageRate[0]['time']
    CpuUsageRateVSorted = SortByValue(CpuUsageRateVSort)
    if len(LocalPods) >= 5 :
	length = 5
    else:
	length = len(LocalPods)
    for index in range(length):
	print "%-41s %-23s %-3d" % (CpuUsageRateVSorted[index], CpuUsageRateTSort[CpuUsageRateVSorted[index]],CpuUsageRateVSort[CpuUsageRateVSorted[index]])
    return

def PrintCpuUsageRateSortWithLog():
    Log = 'Cpu/Usage_Rate Of Each Pod In ' + hostname + '\nPodName\t\t\t\t\t  LastUpdateTime\t  Value\n'
    CpuUsageRateVSort = {}
    CpuUsageRateTSort = {}
    for index in range(len(LocalPods)):  # 逐个读取pod及其相应指标，正确转换时间并输出
        CpuUsageRate = EasyPodQuery(LocalPods[index]['value'], "cpu/usage_rate")
        CpuUsageRate[0]['time'] = TimeAdjust(CpuUsageRate[0]['time'])
        CpuUsageRateVSort[LocalPods[index]['value']] = CpuUsageRate[0]['value']
        CpuUsageRateTSort[LocalPods[index]['value']] = CpuUsageRate[0]['time']
    CpuUsageRateVSorted = SortByValue(CpuUsageRateVSort)
    if len(LocalPods) >= 5 :
        length = 5
    else: 
        length = len(LocalPods)
    for index in range(length):
        Log += "%-41s %-23s %-3d\n" % (CpuUsageRateVSorted[index], CpuUsageRateTSort[CpuUsageRateVSorted[index]],CpuUsageRateVSort[CpuUsageRateVSorted[index]])
    return Log

def PrintMemoryUsageSortWithLog():
    Log = 'Memory/Usage Of Each Pod In ' + hostname + '\nPodName\t\t\t\t\t  LastUpdateTime\t  Value\n'
    MemoryUsageRateVSort = {}
    MemoryUsageRateTSort = {}
    for index in range(len(LocalPods)):  # 逐个读取pod及其相应指标，正确转换时间并输出
        MemoryUsageRate = EasyPodQuery(LocalPods[index]['value'], "memory/usage")
        MemoryUsageRate[0]['time'] = TimeAdjust(MemoryUsageRate[0]['time'])
        MemoryUsageRateVSort[LocalPods[index]['value']] = MemoryUsageRate[0]['value']
        MemoryUsageRateTSort[LocalPods[index]['value']] = MemoryUsageRate[0]['time']
    MemoryUsageRateVSorted = SortByValue(MemoryUsageRateVSort)
    if len(LocalPods) >= 5 :
        length = 5
    else:
        length = len(LocalPods)
    for index in range(length):
        Log +=  "%-41s %-23s %-3d\n" % (MemoryUsageRateVSorted[index], MemoryUsageRateTSort[MemoryUsageRateVSorted[index]],MemoryUsageRateVSort[MemoryUsageRateVSorted[index]])
    return Log

def PrintMemoryMPFSortWithLog():
    Log = 'Memory/major_page_faults Of Each Pod In ' + hostname + '\nPodName\t\t\t\t\t  LastUpdateTime\t  Value\n'
    MemoryMPFVSort = {}
    MemoryMPFTSort = {}
    for index in range(len(LocalPods)):  # 逐个读取pod及其相应指标，正确转换时间并输出
        MemoryMPF = EasyPodQuery(LocalPods[index]['value'], "memory/major_page_faults")
        MemoryMPF[0]['time'] = TimeAdjust(MemoryMPF[0]['time'])
        MemoryMPFVSort[LocalPods[index]['value']] = MemoryMPF[0]['value']
        MemoryMPFTSort[LocalPods[index]['value']] = MemoryMPF[0]['time']
    MemoryMPFVSorted = SortByValue(MemoryMPFVSort)
    if len(LocalPods) >= 5 :
        length = 5
    else:
        length = len(LocalPods)
    for index in range(length):
        Log +=  "%-41s %-23s %-3d\n" % (MemoryMPFVSorted[index], MemoryMPFTSort[MemoryMPFVSorted[index]],MemoryMPFVSort[MemoryMPFVSorted[index]])
    return Log

def SortByValue(d): 
    items=d.items() 
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort(reverse = True) 
    return [ backitems[i][1] for i in range(0,len(backitems))]  
