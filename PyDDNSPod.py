#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import os
import json
import datetime
import threading
import sys

VERSION = "0.4"

# config file
conf_dir = os.path.dirname(__file__)
conf_file = os.path.join(conf_dir, 'pyddnspod.conf')

# global variables
user = ''
password = ''
domain_name = ''
sub_domain = ''
record_value = ''
user_id = ''
domain_id = ''
record_id =''
record_line = "默认"
second = 600 

# Pyddns's user agent
user_agent = 'PyDDNSPod/' + VERSION +' (iceleaf916@gmail.com)'
headers = { 'User-Agent' : user_agent }

# request urls
api_ver_url = 'https://dnsapi.cn/Info.Version'
user_info_url = 'https://dnsapi.cn/User.Info'
domain_list_url = 'https://dnsapi.cn/Domain.List'
domain_info_url = 'https://dnsapi.cn/Domain.Info'
record_type_url = 'https://dnsapi.cn/Record.Type'
record_line_url = 'https://dnsapi.cn/Record.Line'
record_list_url = 'https://dnsapi.cn/Record.List'
update_record_dns = "https://dnsapi.cn/Record.Ddns"

def readConf(fileopen):
    global user, password, domain_name, sub_domain, record_value
    # read config file
    try:
        fp = open(fileopen, 'r')
    except IOError:
        # use default parameters
        print 'cannt open the config file, use default parameters'
        return
    
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
                second = float(value)
            elif name == 'record_line':
                record_line = value
    fp.close()
    return

def getAPIVer():
    data = urllib.urlencode(values)
    ver_req = urllib2.Request(api_ver_url, data, headers)
    try:
        response = urllib2.urlopen(ver_req)
    except Exception, e:
        print e
        print "Oops! There is a problem with the network!"
        sys.exit(0)
    js = response.read()
    return json.loads(js)

def getUserInfo():
    data = urllib.urlencode(values)
    user_info_req = urllib2.Request(user_info_url, data, headers)
    try:
        response = urllib2.urlopen(user_info_req)
    except Exception, e:
        print e
        print "Oops! There is a problem with the network!"
        sys.exit(0)
    js = response.read()
    return json.loads(js)

def getDomainList():
    temp_values = values.copy()
    temp_values['type'] = 'mine'
    temp_values['offset'] = '0'
    temp_values['length'] = '20'
    data = urllib.urlencode(temp_values)
    domain_list_req = urllib2.Request(domain_list_url, data, headers)
    try:
        response = urllib2.urlopen(domain_list_req)
    except Exception, e:
        print e
        print "Oops! There is a problem with the network!"
        sys.exit(0)
    js = response.read()
    return json.loads(js)

def getRecordList(domain_id):
    temp_values = values.copy()
    temp_values['domain_id'] = domain_id
    temp_values['offset'] = '0'
    temp_values['length'] = '20'
    data = urllib.urlencode(temp_values)
    record_list_req = urllib2.Request(record_list_url, data, headers)
    try:
        response = urllib2.urlopen(record_list_req)
    except Exception, e:
        print e
        print "Oops! There is a problem with the network!"
        sys.exit(0)
    js = response.read()
    return json.loads(js)

def updateRecordDns(domain_id, record_id):
    temp_values = values.copy()
    temp_values['domain_id'] = domain_id
    temp_values['record_id'] = record_id
    temp_values['sub_domain'] = sub_domain
    temp_values['record_line'] = record_line
    data = urllib.urlencode(temp_values)
    update_record_dns_req = urllib2.Request(update_record_dns, data, headers)
    try:
        response = urllib2.urlopen(update_record_dns_req)
    except Exception, e:
        print e
        print "Oops! There is a problem with the network!"
        sys.exit(0)
    js = response.read()
    return json.loads(js)

def ddnsUpdate():
    api_ver = getAPIVer()
    if api_ver.get('status').get('code') == '1':
        print 'Getting API version : ' + api_ver.get('status').get('message')
    else:
        print 'Error : Fail to get API version!'
        print 'Error Code : ' + api_ver.get('status').get('code')
        print 'Error Message : '+ api_ver.get('status').get('message')
        print ''
        return

    user_info = getUserInfo()
    if user_info.get('status').get('code') == '1':
        print 'Getting user info : ' + user_info.get('user').get('email')
    else:
        print 'Error : Fail to get user info!'
        print 'Error Code : ' + user_info.get('status').get('code')
        print 'Error Message : '+ user_info.get('status').get('message')
        print ''
        return

    domain_list = getDomainList()
    if domain_list.get('status').get('code') == '1':
        print 'Getting domain list ...'
    else:
        print 'Error : Fail to get domain list!'
        print 'Error Code : ' + domain_list.get('status').get('code')
        print 'Error Message : '+ domain_list.get('status').get('message')
        return

    # get domain's id
    for x in domain_list.get('domains'):
        if x.get('name') == domain_name:
            domain_id = x.get('id')
            print 'OK. Domain name \"' + domain_name + '\" \'s ' + 'id is ' + str(domain_id) + '.'
            break
    else:
        print ''
        print 'Error : Domain name \"' + domain_name + '\" not found! Please check for your config file.'
        return
    
    record_list = getRecordList(domain_id)
    if record_list.get('status').get('code') == '1':
        print 'Getting record list ...'
    else:
        print 'Error : Fail to get record list!'
        print 'Error Code : ' + record_list.get('status').get('code')
        print 'Error Message : '+ record_list.get('status').get('message')
        return
    # get record's id
    for x in record_list.get('records'):
        if x.get('name') == sub_domain:
            record_id = x.get('id')
            print 'OK. Sub domain \"' + sub_domain + '\" \'s ' + 'record id is ' + str(record_id) + '.'
            break
    else:
        record_id == ''
        print 'Sub domain \"' + sub_domain + '\" not found.'

    # update record dns 
    if record_id:
        update_record_status = updateRecordDns(domain_id,record_id)
        if update_record_status.get("status").get("code") == '1' :
            record_value = update_record_status.get("record").get("value")
            now = datetime.datetime.now()
            print "Update ip to %s at %s" % (record_value, now)
            print "The record will be updated every %s seconds..." % second
            
            while 1:
                threading._sleep(second)
                update_record_status = updateRecordDns(domain_id, record_id)
                result_code = str(update_record_status.get("status").get("code"))
                if result_code != '1':
                    error_message = update_record_status.get("status").get("message")
                    now = datetime.datetime.now()
                    print "Fail to update the record at %s" % now
                    print "The error message is %s" % error_message
                    print "Wait %s seconds, the program will try to update again..." % second
                else:
                    ip = update_record_status.get("record").get("value")
                    now = datetime.datetime.now()
                    print "update ip to %s at %s" % (ip, now)
        else:
            print 'Error : Fail to update the record!'
            print 'Error message : ' + update_record_status.get('status').get('message')
    return
    
if __name__ == "__main__":
    readConf(conf_file)
    print 'user:%s' %user
    print 'You want to bind the domain \"' + sub_domain + '.' + domain_name + '\" to local server!'
    print 'start...'
    
    # reqest values
    values = {'login_email' : user,
              'login_password' : password,
              'format' : 'json' }
    
    # post request
    ddnsUpdate()
