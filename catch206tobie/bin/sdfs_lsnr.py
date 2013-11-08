#!/usr/bin/env python
import datetime
import time
import os
import urllib
import urllib2
import subprocess
import sys
import re
import socket
from mimetypes import MimeTypes
from keepalive import HTTPHandler

keepalive_handler = HTTPHandler()
opener = urllib2.build_opener(keepalive_handler)
urllib2.install_opener(opener)

log_filename = '/home/dfs/trafficserver-3.2.0/var/log/trafficserver/squid.log'

print "%s:starlsn:sdfs:%s" % (datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'),log_filename)
lsning = subprocess.Popen(['tail','-F',log_filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    line = lsning.stdout.readline().rstrip()
    if line:
            if 'TCP_MISS/206' in line :
                s_line = line.split(' ')[6]
                s_line = re.sub('http://.*?/','',s_line)
                f_url = "http://127.0.0.1:8080/"+s_line
                decode_url = urllib2.unquote(f_url)
		print "decode_url = %s\n" % (decode_url)
		
                try :
                    source_req = urllib2.Request(decode_url)
                    source_req.add_header("Host","fs-4.photo.163.org")
                    source_req.add_header("Connection","keep-alive")
	            print "then range = %s\n" % (source_req.get_header("Range")) 
                    start_getfile_time = time.time()
                    source_file = urllib2.urlopen(source_req)
                    len_content = source_file.info().getheader('Content-length')
                    content = source_file.read()
                    source_file.close()
                    stop_getfile_time = time.time()
                    print "%s:getfile:tobie:%s:%sms:%s\n" % (datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'),len_content,str(round((stop_getfile_time-start_getfile_time)*1000,4)),s_line)

                except Exception, e:
                    print e
