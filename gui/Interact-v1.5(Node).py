#!/usr/bin/env python  
# -*- coding: UTF-8 -*-
   
from os import system  
import curses  
from curses import wrapper
import InfluxDBQuery

import ConfigParser

ConfigFile = '/home/k8s-master/monitor/monitor.ini'
config = ConfigParser.ConfigParser()
config.readfp(open(ConfigFile))

def del_cron(str):
    cronfile = config.get("Monitor", "monitor_cron" )
    with open(cronfile,"r") as f:
        lines = f.readlines()
    with open(cronfile,"w") as f_w:
        for line in lines:
            if str in line:
                continue
            f_w.write(line)
    system("crontab /home/k8s-master/monitor/k8s-monitor.cron")

def add_cron(str):
    cronfile = config.get("Monitor", "monitor_cron" )
    f = open(cronfile,'a')
    f.write(str)
    f.close()
    system("crontab /home/k8s-master/monitor/k8s-monitor.cron")

def get_param(screen,prompt_string):
    screen.clear()  
    screen.border(0)  
    screen.addstr(2, 2, prompt_string)  
    screen.refresh()  
    input = screen.getstr(10, 10, 60)  
    return int(input)
   
def execute_cmd(cmd_string):  
    system("clear")  
    curses.noecho()
    a = system(cmd_string)  
    print ""  
    if a == 0:
        print "Command executed correctly"  
    else:  
        print "Command terminated with error"  
    raw_input("Press enter to continue...")  
    curses.noecho()
    print ""

def NewPyFile(podname):
    filename ="/home/k8s-master/sql/" + "sql_"+ podname + ".py"
    with open(filename,'w') as f:
        f.write("import InfluxDBQuery\n\n")
        f.write("InfluxDBQuery.PrintSinglePodInfoo(\"" + podname + "\")")
    
def main(screen):
#layer_0
    x_0 = 0  
    curses.beep()
    while x_0 != ord('0'):
        screen_0 = curses.initscr()  
        screen_0.clear()  
        screen_0.border(0)  
        screen_0.addstr(2, 2, "Welcome to use K8S Monitor")  
        screen_0.addstr(4, 4, "1 - Fast Query")  
        screen_0.addstr(5, 4, "2 - SinglePod Query") 
        screen_0.addstr(6, 4, "3 - Monitor Setting")
        screen_0.addstr(11, 4, "0 - Exit")
        screen_0.refresh()  
   
        x_0 = screen_0.getch()
        #layer_1
        if x_0 == ord('1'):
            curses.endwin()
            x_1 = 0
            while x_1 != ord('0'):
                screen_1 = curses.initscr()
                screen_1.clear()
                screen_1.border(0)
                screen_1.addstr(2, 2, "Pod Level or Node Level")
                screen_1.addstr(4, 4, "1 - Pod Level")
                screen_1.addstr(5, 4, "2 - Node Level")
                screen_1.addstr(8, 4, "0 - Exit")   
                screen_1.refresh()

                x_1 = screen_1.getch()
                #layer_1_1
                if x_1 == ord('1'):
                    curses.endwin()
                   
	            x_1_1 = 0
	            while x_1_1 != ord('0'):
                        screen_1_1 = curses.initscr()
                        screen_1_1.clear()
                        screen_1_1.border(0)
                        screen_1_1.addstr(2, 2, "Choose a type | Pod")
                        screen_1_1.addstr(4, 4, "1 - Cpu")
                        screen_1_1.addstr(5, 4, "2 - Filesystem")
                        screen_1_1.addstr(6, 4, "3 - Memory")
                        screen_1_1.addstr(7, 4, "4 - Network")
                        screen_1_1.addstr(8, 4, "5 - Uptime")
                        screen_1_1.addstr(11, 4, "0 - Exit")
                        screen_1_1.refresh()

                        x_1_1 = screen_1_1.getch()
                        #layer_1_1_1
                        if x_1_1 == ord('1'):
                            curses.endwin()

                            x_1_1_1 = 0
                            while x_1_1_1 != ord('0'):
                                screen_1_1_1 = curses.initscr()
                                screen_1_1_1.clear()
                                screen_1_1_1.border(0)
                                screen_1_1_1.addstr(2, 2, "Choose a measurement - Pod - Cpu")
                                screen_1_1_1.addstr(4, 4, "1 - Usage_rate")
                                screen_1_1_1.addstr(5, 4, "2 - Usage")
                                screen_1_1_1.addstr(6, 4, "3 - Limit")
                                screen_1_1_1.addstr(7, 4, "4 - Request")
                                screen_1_1_1.addstr(10, 4, "0 - Exit")
                                screen_1_1_1.refresh()

                                x_1_1_1 = screen_1_1_1.getch()
                                #layer_1_1_1_*
                                if x_1_1_1 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c usagerate")
                                elif x_1_1_1 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c usage")
                                elif x_1_1_1 == ord('3'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c limit")
                                elif x_1_1_1 == ord('4'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c request")

                            curses.endwin()
                        #layer_1_1_2   
                        if x_1_1 == ord('2'):
                            curses.endwin()

                            x_1_1_2 = 0
                            while x_1_1_2 != ord('0'):
                                screen_1_1_2 = curses.initscr()
                                screen_1_1_2.clear()
                                screen_1_1_2.border(0)
                                screen_1_1_2.addstr(2, 2, "Choose a measurement - Pod - Filesystem")
                                screen_1_1_2.addstr(4, 4, "1 - Limit")
                                screen_1_1_2.addstr(5, 4, "2 - Usage")
                                screen_1_1_2.addstr(8, 4, "0 - Exit")
                                screen_1_1_2.refresh()

                                x_1_1_2 = screen_1_1_2.getch()
                                #layer_1_1_2_*
                                if x_1_1_2 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -f limit")
                                elif x_1_1_2 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -f usage")
                                    
                            curses.endwin()
                        #layer_1_1_3                     
                        if x_1_1 == ord('3'):
                            curses.endwin()

                            x_1_1_3 = 0
                            while x_1_1_3 != ord('0'):
                                screen_1_1_3 = curses.initscr()
                                screen_1_1_3.clear()
                                screen_1_1_3.border(0)
                                screen_1_1_3.addstr(2, 2, "Choose a measurement - Pod - Memory")
                                screen_1_1_3.addstr(4, 4, "1 - Cache")
                                screen_1_1_3.addstr(5, 4, "2 - Limit")
                                screen_1_1_3.addstr(6, 4, "3 - Major_page_faults")
                                screen_1_1_3.addstr(7, 4, "4 - Major_page_faults_rate")
                                screen_1_1_3.addstr(8, 4, "5 - Page_faults")
                                screen_1_1_3.addstr(9, 4, "6 - Page_faults_rate")
                                screen_1_1_3.addstr(10, 4, "7 - Request")
                                screen_1_1_3.addstr(11, 4, "8 - Rss")
                                screen_1_1_3.addstr(12, 4, "9 - Usage")
                                screen_1_1_3.addstr(13, 4, "a - Working_set")
                                screen_1_1_3.addstr(16, 4, "0 - Exit")
                                screen_1_1_3.refresh()

                                x_1_1_3 = screen_1_1_3.getch()
                                #layer_1_1_3_*
                                if x_1_1_3 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m cache")
                                elif x_1_1_3 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m limit")
                                elif x_1_1_3 == ord('3'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m majorpagefaults")
                                elif x_1_1_3 == ord('4'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m majorpagefaultsrate")
                                elif x_1_1_3 == ord('5'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m pagefaults")
                                elif x_1_1_3 == ord('6'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m pagefaultsrate")
                                elif x_1_1_3 == ord('7'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m request")
                                elif x_1_1_3 == ord('8'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m rss")
                                elif x_1_1_3 == ord('9'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m usage")
                                elif x_1_1_3 == ord('a'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m workingset")

                            curses.endwin()
                        #layer_1_1_4                         
                        if x_1_1 == ord('4'):
                            curses.endwin()

                            x_1_1_4 = 0
                            while x_1_1_4 != ord('0'):

                                screen_1_1_4 = curses.initscr()
                                screen_1_1_4.clear()
                                screen_1_1_4.border(0)
                                screen_1_1_4.addstr(2, 2, "Choose a measurement - Pod - Network")
                                screen_1_1_4.addstr(4, 4, "1 - Rx")
                                screen_1_1_4.addstr(5, 4, "2 - Rxerrors")
                                screen_1_1_4.addstr(6, 4, "3 - Rxerrorsrate")
                                screen_1_1_4.addstr(7, 4, "4 - Rxrate")
                                screen_1_1_4.addstr(8, 4, "5 - Tx")
                                screen_1_1_4.addstr(9, 4, "6 - Txerrors")
                                screen_1_1_4.addstr(10, 4, "7 - Txerrorsrate")
                                screen_1_1_4.addstr(11, 4, "8 - Txrate")
                                screen_1_1_4.addstr(14, 4, "0 - Exit")
                                screen_1_1_4.refresh()

                                x_1_1_4 = screen_1_1_4.getch()
                                #layer_1_1_4_*
                                if x_1_1_4 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n rx")
                                elif x_1_1_4 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n rxerrors")
                                elif x_1_1_4 == ord('3'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n rxerrorsrate")
                                elif x_1_1_4 == ord('4'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n rxrate")
                                elif x_1_1_4 == ord('5'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n tx")
                                elif x_1_1_4 == ord('6'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n txerrors")
                                elif x_1_1_4 == ord('7'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n txerrorsrate")
                                elif x_1_1_4 == ord('8'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -n txrate")

                            curses.endwin()
                        #layer_1_1_5                       
                        if x_1_1 == ord('5'):
                            curses.endwin()
                            execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -u")
                            
                    curses.endwin()
                    
                if x_1 == ord('2'):
                    curses.endwin()
                   
	            x_1_2 = 0
	            while x_1_2 != ord('0'):
                        screen_1_2 = curses.initscr()
                        screen_1_2.clear()
                        screen_1_2.border(0)
                        screen_1_2.addstr(2, 2, "Choose a type - Node")
                        screen_1_2.addstr(4, 4, "1 - Cpu")
                        screen_1_2.addstr(5, 4, "2 - Filesystem")
                        screen_1_2.addstr(6, 4, "3 - Memory")
                        screen_1_2.addstr(9, 4, "0 - Exit")
                        screen_1_2.refresh()

                        x_1_2 = screen_1_2.getch()
                        #layer_1_2_1
                        if x_1_2 == ord('1'):
                            curses.endwin()

                            x_1_2_1 = 0
                            while x_1_2_1 != ord('0'):
                                screen_1_2_1 = curses.initscr()
                                screen_1_2_1.clear()
                                screen_1_2_1.border(0)
                                screen_1_2_1.addstr(2, 2, "Choose a measurement - Node - Cpu")
                                screen_1_2_1.addstr(4, 4, "1 - Node_allocatable")
                                screen_1_2_1.addstr(5, 4, "2 - Node_capacity")
                                screen_1_2_1.addstr(6, 4, "3 - Node_reservation")
                                screen_1_2_1.addstr(7, 4, "4 - Node_utilization")
                                screen_1_2_1.addstr(10, 4, "0 - Exit")
                                screen_1_2_1.refresh()

                                x_1_2_1 = screen_1_2_1.getch()
                                #layer_1_2_1_*
                                if x_1_2_1 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c nodeallocatable")
                                elif x_1_2_1 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c nodecapacity")
                                elif x_1_2_1 == ord('3'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c nodereservation")
                                elif x_1_2_1 == ord('4'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -c nodeutilization")

                            curses.endwin()
                        #layer_1_2_2    
                        if x_1_2 == ord('2'):
                            curses.endwin()

                            x_1_2_2 = 0
                            while x_1_2_2 != ord('0'):
                                screen_1_2_2 = curses.initscr()
                                screen_1_2_2.clear()
                                screen_1_2_2.border(0)
                                screen_1_2_2.addstr(2, 2, "Choose a measurement - Node - Filesystem")
                                screen_1_2_2.addstr(4, 4, "1 - Inodes")
                                screen_1_2_2.addstr(5, 4, "2 - Inodesfree")
                                screen_1_2_2.addstr(8, 4, "0 - Exit")
                                screen_1_2_2.refresh()

                                x_1_2_2 = screen_1_2_2.getch()
                                #layer_1_2_2_*
                                if x_1_2_2 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -f inodes")
                                elif x_1_2_2 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -f inodesfree")
                                    
                            curses.endwin()
                        #layer_1_2_3                        
                        if x_1_2 == ord('3'):
                            curses.endwin()

                            x_1_2_3 = 0
                            while x_1_2_3 != ord('0'):
                                screen_1_2_3 = curses.initscr()
                                screen_1_2_3.clear()
                                screen_1_2_3.border(0)
                                screen_1_2_3.addstr(2, 2, "Choose a measurement - Memory")
                                screen_1_2_3.addstr(4, 4, "1 - Node_allocatable")
                                screen_1_2_3.addstr(5, 4, "2 - Node_capacity")
                                screen_1_2_3.addstr(6, 4, "3 - Node_reservation")
                                screen_1_2_3.addstr(7, 4, "4 - Node_utilization")
                                screen_1_2_3.addstr(10, 4, "0 - Exit")
                                screen_1_2_3.refresh()

                                x_1_2_3 = screen_1_2_3.getch()
                                #layer_1_2_3_*
                                if x_1_2_3 == ord('1'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m nodeallocatable")
                                elif x_1_2_3 == ord('2'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m nodecapacity")
                                elif x_1_2_3 == ord('3'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m nodereservation")
                                elif x_1_2_3 == ord('4'):
                                    curses.endwin()
                                    execute_cmd("sh /home/k8s-master/sql/k8smonitor.sh -m nodeutilization")

                            curses.endwin()

                    curses.endwin()        

        #layer_2
	if x_0 == ord('2'):
	    curses.endwin()
	    
	    x_2 = 999
	    while x_2 != 0 :
		x_2 = 1
		AllPods = InfluxDBQuery.GetAllPods()
		screen_2 = curses.initscr()
		curses.echo()
                screen_2.clear()
                screen_2.border(0)
                screen_2.addstr(2, 2, "Which pod would you like to query: ")
		AllPods = InfluxDBQuery.GetAllPods()
		for index in range(len(AllPods)):
		    if index < 30:
			breadth = 0
		    else:
			breadth = 60
		    num = str(index + 1) +  " - "
		    podname = AllPods[index]['value']
		  #  NewPyFile(podname)
		    screen_2.addstr(index + 4, breadth + 4, num+podname)
                screen_2.addstr(index + 7, 4, "0 - Exit")
                screen_2.refresh()

                x_2 = screen_2.getstr(2,36,2)
		try:
		    x_2 = int(x_2)
		except:
 		    screen_2.addstr(2,40,"Wrong Input")
		if 0 < x_2 <= (index+1):
		    curses.endwin()
		    execute_cmd("watch -c -n 60 -t python /home/k8s-master/sql/sql_" + AllPods[x_2-1]['value'] + ".py")
		else:
		    continue
			
	    curses.endwin()


	if x_0 == ord('0'):
	    curses.beep()
	    curses.endwin()
	
	if x_0 == ord('3'):
	    curses.endwin()
	    
	    x_4 = 0
	    while x_4 != ord('0'):
		#CpuStatus = config.get("Monitor", "cpu_status")
		#MemoryStatus = config.get("Monitor", "memory_status")
		#DiskStatus = config.get("Monitor", "disk_status")
		screen_4 = curses.initscr()
                screen_4.clear()
                screen_4.border(0)
		screen_4.addstr(2, 2, "Monitor Setting")
		screen_4.addstr(4, 4, "1 - Cpu Monitor")
		screen_4.addstr(5, 4, "2 - Memory Monitor")
		screen_4.addstr(6, 4, "3 - Disk Monitor")
		screen_4.addstr(9, 4, "0 - Exit")
		#screen_4.addstr(4, 4, "Cpu Monitor Status: " + CpuStatus)
		#screen_4.addstr(5, 4, "Memory Monitor Status: " + MemoryStatus)
		#screen_4.addstr(6, 4, "Disk Monitor Status: " + DiskStatus)
		#screen_4.addstr(8, 4, "1 - Change Cpu Monitor Status")
		#screen_4.addstr(9, 4, "2 - Change Memory Monitor Status")
		#screen_4.addstr(10, 4, "3 - Change Disk Monitor Status") 
		#screen_4.addstr(13, 4, "0 - Exit")
		screen_4.refresh()
	
		x_4 = screen_4.getch()
		if x_4 == ord('1'):
		    #layer_4_1
		    curses.endwin()
		    
		    x_4_1 = 0
		    while x_4_1 != ord('0'):
			CpuStatus = config.get("Monitor", "cpu_status")
			CLevel1 = config.get("Monitor", "cpu_level1")
			CLevel2 = config.get("Monitor", "cpu_level2")
			CLevel3 = config.get("Monitor", "cpu_level3")
			screen_4_1 = curses.initscr()
			screen_4_1.clear()
	                screen_4_1.border(0)
        	        screen_4_1.addstr(2, 2, "Cpu Monitor")
			screen_4_1.addstr(4, 4, "Cpu Alert Level 1 : " + CLevel1)
			screen_4_1.addstr(5, 4, "Cpu Alert Level 2 : " + CLevel2)
			screen_4_1.addstr(6, 4, "Cpu Alert Level 3 : " + CLevel3)
			screen_4_1.addstr(7, 4, "Cpu Monitor Status: " + CpuStatus)
			screen_4_1.addstr(9, 4, "1 - Change Cpu Alert Level1")
			screen_4_1.addstr(10, 4, "2 - Change Cpu Alert Level2")
			screen_4_1.addstr(11, 4, "3 - Change Cpu Alert Level3")
			screen_4_1.addstr(12, 4, "4 - Change Cpu Monitor Status")
			screen_4_1.addstr(15, 4, "0 - Exit")
			screen_4_1.refresh()

			x_4_1 = screen_4_1.getch()
			if x_4_1 == ord('1'):
			    curses.endwin()

			    x_4_1_1 = CLevel1
			    while x_4_1_1 != 0:
				screen_4_1_1 = curses.initscr()
				curses.echo()
				CLevel1 = config.get("Monitor", "cpu_level1")
	                        screen_4_1_1.clear()
	                        screen_4_1_1.border(0)
	                        screen_4_1_1.addstr(2, 2, "Cpu Alert Level 1: " + CLevel1)
	                        screen_4_1_1.addstr(4, 4, "Input New Cpu Alert Level 1(1-100): ")
				screen_4_1_1.addstr(7, 4, "0 - Exit")
				screen_4_1_1.refresh()

				x_4_1_1 = screen_4_1_1.getstr(4,40,3)
                		try:
                		    x_4_1_1 = int(x_4_1_1)
                		except:
                		    screen_4_1_1.addstr(8,40,"Wrong Input")
                		if 0 < x_4_1_1 <= 100:
                    		    config.set("Monitor", "cpu_level1", str(x_4_1_1))
				    with open(ConfigFile, 'w') as fw:
	                                config.write(fw)
				else:
				    continue
			
			if x_4_1 == ord('2'):
                            curses.endwin()

                            x_4_1_2 = CLevel2
                            while x_4_1_2 != 0:
                                screen_4_1_2 = curses.initscr()
                                curses.echo()
                                CLevel2 = config.get("Monitor", "cpu_level2")
                                screen_4_1_2.clear()
                                screen_4_1_2.border(0)
                                screen_4_1_2.addstr(2, 2, "Cpu Alert Level 2: " + CLevel2)
                                screen_4_1_2.addstr(4, 4, "Input New Cpu Alert Level 2(1-100): ")
                                screen_4_1_2.addstr(7, 4, "0 - Exit")
                                screen_4_1_2.refresh()

                                x_4_1_2 = screen_4_1_2.getstr(4,40,3)
                                try:
                                    x_4_1_2 = int(x_4_1_2)
                                except:
                                    screen_4_1_2.addstr(8,40,"Wrong Input")
                                if 0 < x_4_1_2 <= 100:
                                    config.set("Monitor", "cpu_level2", str(x_4_1_2))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue
			
			if x_4_1 == ord('3'):
                            curses.endwin()

                            x_4_1_3 = CLevel3
                            while x_4_1_3 != 0:
                                screen_4_1_3 = curses.initscr()
                                curses.echo()
                                CLevel3 = config.get("Monitor", "cpu_level3")
                                screen_4_1_3.clear()
                                screen_4_1_3.border(0)
                                screen_4_1_3.addstr(2, 2, "Cpu Alert Level 3: " + CLevel3)
                                screen_4_1_3.addstr(4, 4, "Input New Cpu Alert Level 3(1-100): ")
                                screen_4_1_3.addstr(7, 4, "0 - Exit")
                                screen_4_1_3.refresh()

                                x_4_1_3 = screen_4_1_3.getstr(4,40,3)
                                try:
                                    x_4_1_3 = int(x_4_1_3)
                                except:
                                    screen_4_1_3.addstr(8,40,"Wrong Input")
                                if 0 < x_4_1_3 <= 100:
                                    config.set("Monitor", "cpu_level3", str(x_4_1_3))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue

			if x_4_1 == ord('4'):
			    if CpuStatus == "on":
	                        config.set("Monitor", "cpu_status", "off")
	                        with open(ConfigFile, 'w') as fw:
	                            config.write(fw)
	                        del_cron("monitor_cpu.py")
	                        curses.beep()
	                    elif CpuStatus == "off":
	                        config.set("Monitor", "cpu_status", "on")
	                        with open(ConfigFile, 'w') as fw:
	                            config.write(fw)
	                        add_cron("*/5 * * * * python /home/k8s-master/monitor/monitor_cpu.py\n")
	                        curses.beep()
                
                if x_4 == ord('2'):
                    #layer_4_2
                    curses.endwin()

                    x_4_2 = 0
                    while x_4_2 != ord('0'):
                        MemoryStatus = config.get("Monitor", "memory_status")
                        MLevel1 = config.get("Monitor", "memory_level1")
                        MLevel2 = config.get("Monitor", "memory_level2")
                        MLevel3 = config.get("Monitor", "memory_level3")
                        screen_4_2 = curses.initscr()
                        screen_4_2.clear()
                        screen_4_2.border(0)
                        screen_4_2.addstr(2, 2, "Memory Monitor")
                        screen_4_2.addstr(4, 4, "Memory Alert Level 1 : " + MLevel1)
                        screen_4_2.addstr(5, 4, "Memory Alert Level 2 : " + MLevel2)
                        screen_4_2.addstr(6, 4, "Memory Alert Level 3 : " + MLevel3)
                        screen_4_2.addstr(7, 4, "Memory Monitor Status: " + MemoryStatus)
                        screen_4_2.addstr(9, 4, "1 - Change Memory Alert Level1")
                        screen_4_2.addstr(10, 4, "2 - Change Memory Alert Level2")
                        screen_4_2.addstr(11, 4, "3 - Change Memory Alert Level3")
                        screen_4_2.addstr(12, 4, "4 - Change Memory Monitor Status")
                        screen_4_2.addstr(15, 4, "0 - Exit")
                        screen_4_2.refresh()

                        x_4_2 = screen_4_2.getch()
                        if x_4_2 == ord('1'):
                            curses.endwin()

                            x_4_2_1 = MLevel1
                            while x_4_2_1 != 0:
                                screen_4_2_1 = curses.initscr()
                                curses.echo()
                                MLevel1 = config.get("Monitor", "memory_level1")
                                screen_4_2_1.clear()
                                screen_4_2_1.border(0)
                                screen_4_2_1.addstr(2, 2, "Memory Alert Level 1: " + MLevel1)
                                screen_4_2_1.addstr(4, 4, "Input New Memory Alert Level 1(1-100): ")
                                screen_4_2_1.addstr(7, 4, "0 - Exit")
                                screen_4_2_1.refresh()

                                x_4_2_1 = screen_4_2_1.getstr(4,43,3)
                                try:
                                    x_4_2_1 = int(x_4_2_1)
                                except:
                                    screen_4_2_1.addstr(8,40,"Wrong Input")
                                if 0 < x_4_2_1 <= 100:
                                    config.set("Monitor", "memory_level1", str(x_4_2_1))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue
                        
                        if x_4_2 == ord('2'):
                            curses.endwin()

                            x_4_2_2 = MLevel2
                            while x_4_2_2 != 0:
                                screen_4_2_2 = curses.initscr()
                                curses.echo()
                                MLevel2 = config.get("Monitor", "memory_level2")
                                screen_4_2_2.clear()
                                screen_4_2_2.border(0)
                                screen_4_2_2.addstr(2, 2, "Memory Alert Level 2: " + MLevel2)
                                screen_4_2_2.addstr(4, 4, "Input New Memory Alert Level 2(1-100): ")
                                screen_4_2_2.addstr(7, 4, "0 - Exit")
                                screen_4_2_2.refresh()

                                x_4_2_2 = screen_4_2_2.getstr(4,43,3)
                                try:
                                    x_4_2_2 = int(x_4_2_2)
                                except:
                                    screen_4_2_2.addstr(8,40,"Wrong Input")
                                if 0 < x_4_2_2 <= 100:
                                    config.set("Monitor", "memory_level2", str(x_4_2_2))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue

                        if x_4_2 == ord('3'):
                            curses.endwin()

                            x_4_2_3 = MLevel3
                            while x_4_2_3 != 0:
                                screen_4_2_3 = curses.initscr()
                                curses.echo()
                                MLevel3 = config.get("Monitor", "memory_level3")
                                screen_4_2_3.clear()
                                screen_4_2_3.border(0)
                                screen_4_2_3.addstr(2, 2, "Memory Alert Level 3: " + MLevel3)
                                screen_4_2_3.addstr(4, 4, "Input New Memory Alert Level 3(1-100): ")
                                screen_4_2_3.addstr(7, 4, "0 - Exit")
                                screen_4_2_3.refresh()

                                x_4_2_3 = screen_4_2_3.getstr(4,43,3)
                                try:
                                    x_4_2_3 = int(x_4_2_3)
                                except:
                                    screen_4_2_3.addstr(8,40,"Wrong Input")
                                if 0 < x_4_2_3 <= 100:
                                    config.set("Monitor", "memory_level3", str(x_4_2_3))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue

                        if x_4_2 == ord('4'):
                            if MemoryStatus == "on":
                                config.set("Monitor", "memory_status", "off")
                                with open(ConfigFile, 'w') as fw:
                                    config.write(fw)
                                del_cron("monitor_memory.py")
                                curses.beep()
                            elif MemoryStatus == "off":
                                config.set("Monitor", "memory_status", "on")
                                with open(ConfigFile, 'w') as fw:
                                    config.write(fw)
                                add_cron("*/3 * * * * python /home/k8s-master/monitor/monitor_memory.py\n")
                                curses.beep()

                    curses.endwin()

                if x_4 == ord('3'):
                    #layer_4_3
                    curses.endwin()

                    x_4_3 = 0
                    while x_4_3 != ord('0'):
                        DiskStatus = config.get("Monitor", "disk_status")
                        DLevel1 = config.get("Monitor", "disk_level1")
                        DLevel2 = config.get("Monitor", "disk_level2")
                        DLevel3 = config.get("Monitor", "disk_level3")
                        screen_4_3 = curses.initscr()
                        screen_4_3.clear()
                        screen_4_3.border(0)
                        screen_4_3.addstr(2, 2, "Disk Monitor")
                        screen_4_3.addstr(4, 4, "Disk Alert Level 1 : " + DLevel1)
                        screen_4_3.addstr(5, 4, "Disk Alert Level 2 : " + DLevel2)
                        screen_4_3.addstr(6, 4, "Disk Alert Level 3 : " + DLevel3)
                        screen_4_3.addstr(7, 4, "Disk Monitor Status: " + DiskStatus)
                        screen_4_3.addstr(9, 4, "1 - Change Disk Alert Level1")
                        screen_4_3.addstr(10, 4, "2 - Change Disk Alert Level2")
                        screen_4_3.addstr(11, 4, "3 - Change Disk Alert Level3")
                        screen_4_3.addstr(12, 4, "4 - Change Disk Monitor Status")
                        screen_4_3.addstr(15, 4, "0 - Exit")
                        screen_4_3.refresh()

                        x_4_3 = screen_4_3.getch()
                        if x_4_3 == ord('1'):
                            curses.endwin()

                            x_4_3_1 = DLevel1
                            while x_4_3_1 != 0:
                                screen_4_3_1 = curses.initscr()
                                curses.echo()
                                DLevel1 = config.get("Monitor", "disk_level1")
                                screen_4_3_1.clear()
                                screen_4_3_1.border(0)
                                screen_4_3_1.addstr(2, 2, "Disk Alert Level 1: " + DLevel1)
                                screen_4_3_1.addstr(4, 4, "Input New Disk Alert Level 1(1-100): ")
                                screen_4_3_1.addstr(7, 4, "0 - Exit")
                                screen_4_3_1.refresh()

                                x_4_3_1 = screen_4_3_1.getstr(4,40,3)
                                try:
                                    x_4_3_1 = int(x_4_3_1)
                                except:
                                    screen_4_3_1.addstr(8,40,"Wrong Input")
                                if 0 < x_4_3_1 <= 100:
                                    config.set("Monitor", "disk_level1", str(x_4_3_1))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue
                            curses.endwin()

                        if x_4_3 == ord('2'):
                            curses.endwin()

                            x_4_3_2 = DLevel2
                            while x_4_3_2 != 0:
                                screen_4_3_2 = curses.initscr()
                                curses.echo()
                                DLevel2 = config.get("Monitor", "disk_level2")
                                screen_4_3_2.clear()
                                screen_4_3_2.border(0)
                                screen_4_3_2.addstr(2, 2, "Disk Alert Level 2: " + DLevel2)
                                screen_4_3_2.addstr(4, 4, "Input New Disk Alert Level 2(1-100): ")
                                screen_4_3_2.addstr(7, 4, "0 - Exit")
                                screen_4_3_2.refresh()

                                x_4_3_2 = screen_4_3_2.getstr(4,40,3)
                                try:
                                    x_4_3_2 = int(x_4_3_2)
                                except:
                                    screen_4_3_2.addstr(8,40,"Wrong Input")
                                if 0 < x_4_3_2 <= 100:
                                    config.set("Monitor", "disk_level2", str(x_4_3_2))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue
                            curses.endwin()

                        if x_4_3 == ord('3'):
                            curses.endwin()

                            x_4_3_3 = DLevel3
                            while x_4_3_3 != 0:
                                screen_4_3_3 = curses.initscr()
                                curses.echo()
                                DLevel3 = config.get("Monitor", "disk_level3")
                                screen_4_3_3.clear()
                                screen_4_3_3.border(0)
                                screen_4_3_3.addstr(2, 2, "Disk Alert Level 3: " + DLevel3)
                                screen_4_3_3.addstr(4, 4, "Input New Disk Alert Level 3(1-100): ")
                                screen_4_3_3.addstr(7, 4, "0 - Exit")
                                screen_4_3_3.refresh()

                                x_4_3_3 = screen_4_3_3.getstr(4,40,3)
                                try:
                                    x_4_3_3 = int(x_4_3_3)
                                except:
                                    screen_4_3_3.addstr(8,40,"Wrong Input")
                                if 0 < x_4_3_3 <= 100:
                                    config.set("Monitor", "disk_level3", str(x_4_3_3))
                                    with open(ConfigFile, 'w') as fw:
                                        config.write(fw)
                                else:
                                    continue
                            curses.endwin()

                        if x_4_3 == ord('4'):
                            if DiskStatus == "on":
                                config.set("Monitor", "disk_status", "off")
                                with open(ConfigFile, 'w') as fw:
                                    config.write(fw)
                                del_cron("monitor_disk.py")
                                curses.beep()
                            elif DiskStatus == "off":
                                config.set("Monitor", "disk_status", "on")
                                with open(ConfigFile, 'w') as fw:
                                    config.write(fw)
                                add_cron("0 */1 * * * python /home/k8s-master/monitor/monitor_disk.py\n")
                                curses.beep()

                    curses.endwin()


    curses.endwin()
wrapper(main)
