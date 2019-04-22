#coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

import os,time
import psutil
from os import system

import os
import ConfigParser
import InfluxDBQuery

mail_info = {
    "from": "470790151@qq.com",
    "to": "2432237441@qq.com",
    "hostname": "smtp.qq.com",
    "username": "470790151@qq.com",
    "password": "pshdaacpvtbdbibi",
    "mail_subject": "test",
    "mail_text": "hello, this is a test email, sended by py",
    "mail_encoding": "utf-8"
}

ConfigFile = '/home/k8s-master/monitor/monitor.ini'
config = ConfigParser.ConfigParser()
config.readfp(open(ConfigFile))

SleepTime = float(config.get("Monitor", "SleepTime"))
CLevel1 = int(config.get("Monitor", "cpu_level1"))
CLevel2 = int(config.get("Monitor", "cpu_level2"))
CLevel3 = int(config.get("Monitor", "cpu_level3"))
MLevel1 = int(config.get("Monitor", "memory_level1"))
MLevel2 = int(config.get("Monitor", "memory_level2"))
MLevel3 = int(config.get("Monitor", "memory_level3"))
DLevel1 = int(config.get("Monitor", "disk_level1"))
DLevel2 = int(config.get("Monitor", "disk_level2" ))
DLevel3 = int(config.get("Monitor", "disk_level3" ))

LogDir = config.get("Monitor", "log_dir")
CpuMonitorFile = config.get("Monitor", "cpu_log" )
MemoryMonitorFile = config.get("Monitor", "memory_log" )
FilesystemMonitorFile = config.get("Monitor", "filesystem_log" )
DiskMonitorFile = config.get("Monitor", "disk_log" )

hostname = config.get("BasicInfo", "hostname")
#Check File
def CheckFile(log_dir, log_file):
	if os.path.exists(log_dir) != True:
                os.makedirs(log_dir)
        if os.path.exists(log_file) != True:
                file = open(log_file, 'w')  
                file.close()  

#Monitor For Cpu
def CpuMonitor():
	#create a list to record 3 cpu status in 30 seconds(once per 10 seconds)
	#print title, handle the data, give its reaction
	CheckFile(LogDir + "/cpu", CpuMonitorFile)
	CpuStatus = []
	LogMessage = "Cpu/Usage_rate(%/s)\n"
	for index1 in range(3):
		Time1 = TempTime()
		CpuUsagerate = []
		for index2 in range(10):
			singlecp = psutil.cpu_percent(1)
			CpuUsagerate.append(singlecp)
		AveCpuIdle = sum(CpuUsagerate) / 10
		if AveCpuIdle < CLevel1: 
			CpuStatus.append('0')
		elif CLevel1 <= AveCpuIdle < CLevel2:
			CpuStatus.append('1')
		elif CLevel2 <= AveCpuIdle < CLevel3:
			CpuStatus.append('2')
		elif AveCpuIdle >= CLevel3:
			CpuStatus.append('3')
		Time2 = TempTime()
		LogMessage = LogMessage + "From " + Time1 + " To " + Time2 + "\n" + str(CpuUsagerate) + "\n" + "Average of Cpu/usage_rate:" + str(AveCpuIdle) + "\n"
	#When it comes to Dangerous, send E-mail with its log and top 10 processes and pods using most cpu 
	if '3' in CpuStatus:
		LogMessage += 'You have no cpu available sometimes in last 30 seconds!Please have a check!\n[Dangerous]\n\n'
		LogMessage += "\n\nHere Are Top 10 Processes Using Most Cpu\n" +  MachineCpuSort()
		LogMessage += "\n\n" + InfluxDBQuery.PrintCpuUsageRateSortWithLog()
		TempFileName = CpuMonitorFile + str(TempTime())
		LogWriting(TempFileName, LogMessage, 'w')
		SendEmail("Cpu Warning --- " + hostname, LogMessage)
	elif '2' in CpuStatus:
		LogMessage = LogMessage + 'Your almost have no cpu available sometimes in last 30 seconds.\n[Warning]\n\n'
	elif '1' in CpuStatus:
		LogMessage = LogMessage + 'Your Cpu/usage is at a high rate sometimes in last 30 seconds.\n[Healthy]\n\n'
	else:
		LogMessage = LogMessage + 'Your Cpu has been at a free status in last 15 seconds.\n[Healthy]\n\n'
	#Write Logs
	LogWriting(CpuMonitorFile, LogMessage, 'a')

#Monitor For Memory	
def MemoryMonitor():
	CheckFile(LogDir + "/memory", MemoryMonitorFile)
	MemoryStatus = []
	LogMessage = "Memory/Usage_rate"
	for index in range(3):
		Time1 = TempTime()
		MemoryUsagerate = []
		for index2 in range(5):
			singlemp = psutil.virtual_memory().percent
			MemoryUsagerate.append(singlemp)
			time.sleep(SleepTime)
		AveMemoryUsagerate = sum(MemoryUsagerate) / 5
		if AveMemoryUsagerate < MLevel1:
			MemoryStatus.append('0')
		elif MLevel1 <= AveMemoryUsagerate < MLevel2:
			MemoryStatus.append('1')
		elif MLevel2 <= AveMemoryUsagerate < MLevel3:
			MemoryStatus.append('2')
		elif AveMemoryUsagerate >= MLevel3:
			MemoryStatus.append('3')
		Time2 = TempTime()
		LogMessage = LogMessage + "From " + Time1 + " To " + Time2 + "\n" + str(MemoryUsagerate) + "\n" + "Average of Memory/usage_rate:" + str(AveMemoryUsagerate) + "\n"
	if '3' in MemoryStatus:
		LogMessage += 'You almost have no memory available sometimes in last 15 seconds!Please have a check!\n[Dangerous]\n\n'
		LogMessage += "\n\nHere Are Top 10 Processes Using Most Memory\n" +  MachineMemorySort()
		LogMessage += "\n\n" + InfluxDBQuery.PrintMemoryUsageSortWithLog() + "\n" + InfluxDBQuery.PrintMemoryMPFSortWithLog()
		TempFileName = MemoryMonitorFile + str(TempTime())
		LogWriting(TempFileName, LogMessage, 'w')
		SendEmail("Memory Warning --- " + hostname, LogMessage)
	elif '2' in MemoryStatus:
		LogMessage = LogMessage + 'Your almost have no memory available sometimes in last 15 seconds.\n[Warning]\n\n'
	elif '1' in MemoryStatus:
		LogMessage = LogMessage + 'Your Memory/usage_rate has been at a high rate sometimes in last 15 seconds.\n[Healthy]\n\n'
	else:
		LogMessage = LogMessage + 'Your Memory has been at a free status in last 15 seconds.\n[Healthy]\n\n'
	LogWriting(MemoryMonitorFile, LogMessage, 'a')
		
	

#Monitor For Disk
def DiskMonitor():
	CheckFile(LogDir + "/disk", DiskMonitorFile)
	DiskStatus = []
	DiskUsagerate = []
        LogMessage = "Disk/Usage_rate(%/s)\n"
        Time = TempTime()
        singledp = psutil.disk_usage('/').percent
	DiskUsagerate.append(singledp)
	DiskStatusNow = sum(DiskUsagerate) / 1
        if DiskStatusNow < DLevel1:
		DiskStatus.append('0')
        elif DLevel1 <= DiskStatusNow < DLevel2:
                Diskstatus.append('1')
        elif DLevel2 <= DiskStatusNow < DLevel3:
                DiskStatus.append('2')
        elif DiskStatusNow >= DLevel3:
                DiskStatus.append('3')
        LogMessage = LogMessage + Time + "\n" + str(DiskUsagerate) + "\n"
        #When it comes to Dangerous, send E-mail with its log and top 10 processes and pods using most cpu 
        if '3' in DiskStatus:
                LogMessage += 'You have no Disk available!Please have a check!\n[Dangerous]\n\n'
               # LogMessage += "\n\n" + InfluxDBQuery.PrintCpuUsageRateSortWithLog()
                TempFileName = DiskMonitorFile + str(TempTime())
                LogWriting(TempFileName, LogMessage, 'w')
                SendEmail("Disk Warning --- " + hostname, LogMessage)
        elif '2' in DiskStatus:
                LogMessage = LogMessage + 'Your almost have no Disk available.\n[Warning]\n\n'
        elif '1' in DiskStatus:
                LogMessage = LogMessage + 'Your disk are highly usesd.\n[Healthy]\n\n'
        else:
                LogMessage = LogMessage + 'Your disk has been at a free status.\n[Healthy]\n\n'
        #Write Logs
        LogWriting(DiskMonitorFile, LogMessage, 'a')

#Geting Temporal Time
def TempTime():
	TimeStamp = time.time()
	TimeLocal = time.localtime(TimeStamp)
	FormatTime = time.strftime("%Y-%m-%d %H:%M:%S", TimeLocal)
	return FormatTime

#Writing Monitor Logs
def LogWriting(FileName, Content, Method):
	with open(FileName, Method) as f:
		f.write(Content)


#Sending E-mail
def SendEmail(Subject, Context):
	mail_info["mail_subject"] = Subject
	mail_info["mail_text"] = Context
	smtp = SMTP_SSL(mail_info["hostname"])
	#smtp.set_debuglevel(1)

	smtp.ehlo(mail_info["hostname"])
	smtp.login(mail_info["username"], mail_info["password"])

	msg = MIMEText(mail_info["mail_text"], "plain", mail_info["mail_encoding"])
	msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
	msg["from"] = mail_info["from"]
	msg["to"] = mail_info["to"]

	smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())

	smtp.quit()

def MachineCpuSort():
	Time =str(TempTime())
	Time = Time.split(" ")
	FileNameCR = "MachineCpuSort" + Time[0] + "-" + Time[1]
	system("ps aux|head -1 >> /home/k8s-master/monitor/log/cpu/" + FileNameCR)
	system("ps aux|grep -v PID|sort -rn -k +3|head >> /home/k8s-master/monitor/log/cpu/" + FileNameCR)
	ReadFile = open("/home/k8s-master/monitor/log/cpu/" + FileNameCR).read().decode("utf-8")
	return ReadFile
	
def MachineMemorySort():
        Time =str(TempTime())
        Time = Time.split(" ")
        FileNameCR = "MachineMemorySort" + Time[0] + "-" + Time[1]
        system("ps aux|head -1 >> /home/k8s-master/monitor/log/memory/" + FileNameCR)
        system("ps aux|grep -v PID|sort -rn -k +4|head >> /home/k8s-master/monitor/log/memory/" + FileNameCR)
        ReadFile = open("/home/k8s-master/monitor/log/memory/" + FileNameCR).read().decode("utf-8")
        return ReadFile


#MachineCpuSort()
#MemoryMonitor()
#CpuMonitor()

