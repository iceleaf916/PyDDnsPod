#!/usr/bin/env python
# -*- coding: utf-8 -*-       

import urllib
import urllib2
import json

class DnspodApi():
    '''Dnspod API class'''
    def __init__(self, headers, email, password, format_type="json"):
        self.request_url = {
            'api_ver_url': 'https://dnsapi.cn/Info.Version',
            'user_info_url': 'https://dnsapi.cn/User.Info',
            'domain_list_url': 'https://dnsapi.cn/Domain.List',
            'record_list_url': 'https://dnsapi.cn/Record.List',
            'update_record_dns': 'https://dnsapi.cn/Record.Ddns',
            'domain_group_url': 'https://dnsapi.cn/Domaingroup.List',
        }
        self.values = {
            'login_email' : email,
            'login_password' : password,
            'format' : format_type,
        }
        self.headers = headers

    def __request_data(self, req_url_name, req_values):
        '''common request data method'''
        data = urllib.urlencode(req_values)
        ver_req = urllib2.Request(self.request_url[req_url_name], 
            data, self.headers)
        try:
            req_response = urllib2.urlopen(ver_req)
            js = req_response.read()
            return json.loads(js)
        except Exception, e:
            print e
            print "Oops! There is a problem with the network!"
            return False

    def getAPIVer(self):
        temp_values = self.values.copy()
        api_result = self.__request_data("api_ver_url", temp_values)
        return api_result

    def getUserInfo(self):
        temp_values = self.values.copy()
        user_info = self.__request_data("user_info_url", temp_values)
        return user_info
    
    def getDomainGroup(self):
        temp_values = self.values.copy()
        domain_group = self.__request_data("domain_group_url", temp_values)
        return domain_group

    def getDomainList(self, domain_type='all', offset='0', length='20', group_id = '1'):
        temp_values = self.values.copy()
        temp_values['type'] = domain_type
        temp_values['offset'] = offset
        temp_values['length'] = length
        temp_values['group_id'] = group_id
        domain_list = self.__request_data("domain_list_url", temp_values)
        return domain_list

    def getRecordList(self, domain_id, offset='0', length='20'):
        temp_values = self.values.copy()
        temp_values['domain_id'] = domain_id
        temp_values['offset'] = offset
        temp_values['length'] = length
        record_list = self.__request_data("record_list_url", temp_values)
        return record_list

    def updateRecordDns(self, domain_id, record_id, sub_domain, record_line):
        temp_values = self.values.copy()
        temp_values['domain_id'] = domain_id
        temp_values['record_id'] = record_id
        temp_values['sub_domain'] = sub_domain
        temp_values['record_line'] = record_line
        update_record_dns = self.__request_data("update_record_dns", temp_values)
        return update_record_dns
