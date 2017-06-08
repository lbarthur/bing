#!/usr/local/bin/python3.6
import datetime
import psutil
import time
import csv
import fileinput
import http.server
import socketserver
import os
from apscheduler.schedulers.blocking import BlockingScheduler


title_line=['Time', 'CPU usage(%)', 'Total CPU cores', 'Memory usage', 'Total memory', 'IO/sec in', 'IO/sec out',
 'Network IO in', 'Network IO in', 'Swap total', 'Swap used']
currentdate = ''
#loglocation = "/home/issclike/logs/"
loglocation = '/reboot/logs/'
def perfcollection():
    yyyymmdd = datetime.datetime.now().date().isoformat()
    hh = str(datetime.datetime.now().hour)
    with open(loglocation+'runtime-'+yyyymmdd+'-'+hh+'.csv', "a+")as f:
        csvwriter = csv.writer(f)
        currentdate = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
        cpu_usage = psutil.cpu_percent()
        cpu_cores = psutil.cpu_count()
        mem_usage = psutil.virtual_memory().used//1024
        mem_total = psutil.virtual_memory().total//1024//1024
        io_in_before = psutil.disk_io_counters().write_bytes//1024
        io_out_before = psutil.disk_io_counters().read_bytes // 1024
        net_io_in_before = psutil.net_io_counters().bytes_recv // 1024
        net_io_out_before = psutil.net_io_counters().bytes_sent // 1024
        time.sleep(1)
        io_in_after = psutil.disk_io_counters().write_bytes//1024
        io_out_after = psutil.disk_io_counters().read_bytes // 1024
        net_io_in_after = psutil.net_io_counters().bytes_recv // 1024
        net_io_out_after = psutil.net_io_counters().bytes_sent // 1024
        io_in = io_in_after - io_in_before
        io_out = io_out_after - io_out_before
        net_io_in = net_io_in_after - net_io_in_before
        net_io_out = net_io_out_after - net_io_out_before
        swap_total = psutil.swap_memory().total//1024//1024
        swap_usage = psutil.swap_memory().used//1024
        #psutil.net_io_counters(pernic=True)['lo'].bytes_sent // 1024
        #psutil.net_io_counters(pernic=True)['lo'].bytes_recv // 1024
        #psutil.net_io_counters(pernic=True)['eth0'].bytes_sent // 1024
        #psutil.net_io_counters(pernic=True)['eth0'].bytes_recv // 1024
        data = [
            currentdate, cpu_usage,cpu_cores ,mem_usage,mem_total,io_in,io_out,net_io_in,net_io_out,swap_total,swap_usage
        ]

        f.seek(0)  # go to the firstline
        first_line = f.readline()  #read the first line content
        if not first_line:  # if the first line is null
            csvwriter.writerow(title_line)
            csvwriter.writerow(data)
        else:    # if the first line is not null
            csvwriter.writerow(data)

sched = BlockingScheduler()
sched.add_job(perfcollection, 'cron', second='00,10,20,30,40,50')
sched.start()

'''
timelist=['18:03:20','18:03:25']
currentdate = ''
#currentday = datetime.datetime.strftime(currenttime,'%d')
#currentmonth = datetime.datetime.strftime(currenttime,'%m')
#currentyear = datetime.datetime.strftime(currenttime,'%Y')
#open(datetime.datetime.now().date().isoformat()+'.csv', 'a+').close()
#print (currentdate)


def perfcollection(timearry):
    while True:
        f = open("/reboot/logs/" + datetime.datetime.now().date().isoformat() + '.csv', "a+")
        currentdate = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
        if(currentdate in timearry):
            print  ("yeah")
            f.write("%s,%s\n" %(currentdate,psutil.virtual_memory().percent))
            time.sleep(1)
            f.close()
        else:
            time.sleep(1)


perfcollection(timelist)
'''