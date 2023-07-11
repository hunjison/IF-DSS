#!/usr/bin/env python3

import json, subprocess, os

def URL_to_dnslink(fd):
    return_list = []
    _dnslink_site = fd.readline()

    while _dnslink_site:
        return_list.append(f"_dnslink.{_dnslink_site.split('/')[2]}")
        _dnslink_site = fd.readline()
    
    return_list = list(dict.fromkeys(return_list))

    return return_list

def dnslink_query(file_path, dig, output_path):
    result = {}
    _dnslink_site_list = URL_to_dnslink(fd = open(file_path,"r"))

    for _dnslink in _dnslink_site_list:
        args = [dig, '+noall', '+answer', 'TXT', _dnslink]
        output = subprocess.check_output(args)
        output = output.decode('utf-8').split('\n')[0].split('dnslink=/ipfs/')
        if output != [''] and output[1][:2] == "Qm":
            result[_dnslink] = output[1][:-1]
            json.dump(result, open(os.path.join(output_path, "dnslink_result.json"),"w"))
