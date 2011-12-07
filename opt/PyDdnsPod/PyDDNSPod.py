#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import sys
import time
from dnspodapi import DnspodApi

VERSION = "0.5"

# config file
conf_dir = os.path.dirname(__file__)
conf_file = os.path.join(conf_dir, 'pyddnspod.conf')

# global variables
user = ''
password = ''
domain_name = ''
sub_domain = ''
record_line = "默认"
seconds = 600
user_agent = 'PyDDNSPod/' + VERSION +' (iceleaf916@gmail.com)'
headers = { 'User-Agent' : user_agent }

def write_log(errors):
    try:
        f = open("/var/log/pyddnspod_error.log", "a")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        w = "[%s] %s" % (now, errors)
        f.write(w)
        f.close()
    except Exception, e:
        pass

def readConf(fileopen):
    global user, password, domain_name, sub_domain, seconds, record_line
    try:
        fp = open(fileopen, 'r')
    except IOError:
        errors = 'cannt open the config file, use default parameters'
        print errors
        sys.exit(0)
    c = fp.readlines()
    for line in c:
        line = line.strip()
        if line == "":
            continue
        elif line.startswith("#"):
            continue
        (name, sep, value) = line.partition('=')
        if sep == '=':
            name = name.strip().lower()
            value = value.strip()
            if name == 'user':
                 user = value
            elif name == 'password':
                password = value
            elif name == 'domain_name':
                domain_name = value
            elif name == 'sub_domain':
                sub_domain = value
            elif name == 'time':
                seconds = float(value)
            elif name == 'record_line':
                record_line = value
    fp.close()
    return

class DdnsUpdate():
    '''update dynamic DNS record thread'''

    def __init__(self):
        global user, password, headers
        self.dnspodapi_obj = DnspodApi(headers, user, password)
    
    def get_domain_id(self, domain):
        domain_id_dict = {}
        domain_list = self.dnspodapi_obj.getDomainList()
        if domain_list:
            if domain_list.get('status').get('code') == '1':
                for x in domain_list.get('domains'):
                    domain_id_dict[x.get('name')] = x.get('id')
                domain_id = domain_id_dict.get(domain)
                return domain_id
            else:
                print 'Error : Fail to get domain list!'
                print 'Error Code : ' + domain_list.get('status').get('code')
                print 'Error Message : '+ domain_list.get('status').get('message')
        return False
    
    def get_record_id(self, domain_id, sub_domain):
        record_id_dict = {}
        record_list = self.dnspodapi_obj.getRecordList(domain_id)
        if record_list:
            if record_list.get('status').get('code') == '1':
                for x in record_list.get('records'):
                    record_id_dict[x.get('name')] = x.get('id')
                record_id = record_id_dict.get(sub_domain)
                return record_id
            else:
                print 'Error : Fail to get record list!'
                print 'Error Code : ' + domain_list.get('status').get('code')
                print 'Error Message : '+ domain_list.get('status').get('message')
        return False
    
    def get_ids(self, domain, sub_domain):
        domain_id = self.get_domain_id(domain)
        if domain_id:
            print "domain_id: " + str(domain_id)
            record_id = self.get_record_id(domain_id, sub_domain)
            if record_id:
                print "record_id: " + str(record_id)
                return (domain_id, record_id)
        return False
        
    def update_record_dns(self, domain_id, record_id, sub_domain, record_line):
        return self.dnspodapi_obj.updateRecordDns(domain_id, record_id, sub_domain, record_line)

def update_loop(seconds):
    global domain_name, sub_domain, record_line
    app = DdnsUpdate()
    ids = app.get_ids(domain_name, sub_domain)
    while not ids:
        print 'Something is wrong with the network, wait %s seconds to try again...' % seconds 
        time.sleep(seconds)
        ids = app.get_ids(domain_name, sub_domain)
    domain_id, record_id = ids
    while 1:
        update_result = app.update_record_dns(domain_id, record_id, sub_domain, record_line)
        if update_result:
            if update_result.get("status").get("code") == "1":
                print "[%s] update %s.%s to %s successful" % (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    sub_domain, domain_name, 
                    update_result.get("record").get("value"),
                )
        else:
            print 'Something is wrong with the network'
        time.sleep(seconds)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        conf_file = sys.argv[1]
    readConf(conf_file)
    print 'user:%s' % user
    print 'You want to bind the domain \"' + sub_domain + '.' + domain_name + '\" to local server!'
    print 'start...'
    
    # post request
    update_loop(seconds)
