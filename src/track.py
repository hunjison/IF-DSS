#!/usr/bin/env python3

import base64, base58
import subprocess, json, os

# It should be added more for accurate tracking
Gateway_NodeID = ["QmQzqxhK82kAmKvARFZSkUVS6fo9sySaiogAnx5EnZ6ZmC", "Qma8ddFEQWEU8ijWvdxXm3nxU7oHsRtCykAaVz8WUYhiKn", "12D3KooWL4oguAYeRKYL6xv8S5wMwKjLgP78FoNDMECuHY6vAkYH", "QmcfJeB3Js1FG7T8YaZATEiaHqNKVdQfybYYkbT1knUswx", "12D3KooWPToGJ2YLfYRn6QKQcYT7dwNZD39w3KkMpWjDt8csr8Rf", "12D3KooWMkBZYybPgHMr7Se5P2qecu4oz34V1TMgsLPJbNeBCekz", "12D3KooWDfrUc9KWYphepLsoGvFYqmHaahjBAKj2iFmY2nFDY2Wy"]

def CIDv0_to_CIDv1(CIDv0):
    return (b"B"+base64.b32encode(b"\x01\x55"+base58.b58decode(CIDv0)).replace(b"=",b"")).decode().lower()

def URL_to_CID(fd):
    cid_list = []
    phishing_site = fd.readline()

    while phishing_site:
        if phishing_site.find("Qm") != -1:
            index = phishing_site.find("Qm")
            if len(phishing_site[index:index+46]) == 46:
                cid_list.append(f"{phishing_site[index:index+46]}")
        elif phishing_site.find("baf") != -1:
            index = phishing_site.find("baf")
            if len(phishing_site[index:index+59]) == 59:
                cid_list.append(f"{phishing_site[index:index+59]}")
        phishing_site = fd.readline()

    fd.close()

    return cid_list

def findprovs(ipfs_path, CID):
    try:    # Check collected phishing site errors
        args = [ipfs_path, 'dht', 'findprovs', CID]
        output = subprocess.check_output(args)
        output = output.decode('utf-8').split("\n")
        output = list(dict.fromkeys(output))
        output = output[:len(output)-1]
    except:
        output = []
    return output

def findpeer(ipfs_path, Node_ID):
    IP_LIST = []

    for NodeID in Node_ID:
        if NodeID in Gateway_NodeID:
            continue
        args = [ipfs_path, 'dht', 'findpeer', NodeID]
        output = subprocess.check_output(args)
        output = output.decode('utf-8').split('\n')

        for ip_data in output: # remove Virtual IP
            if "ip4" in ip_data:
                IP = ip_data.split('/')[2]
                check = IP.split('.')[0]
                if check not in ['10', '127', '172', '192']:
                    IP_LIST.append(IP)

    IP_LIST = list(dict.fromkeys(IP_LIST)) # remove duplicate IP

    return IP_LIST  

def node_track(file_path, ipfs, output):
    duplication = []
    result = {}
    CID_LIST = URL_to_CID(fd = open(file_path,"r"))
    CID_LIST = set(CID_LIST) # CID deduplicate
    ipfs_path = ipfs

    yn = input("Is your IPFS daemon running? (y/n): ")
    if yn.lower() != "y":
        return

    for CID in CID_LIST:
        if CID in duplication:
            continue
        NodeID = findprovs(ipfs_path, CID)
        if NodeID != []:
            result_IPs = findpeer(ipfs_path, NodeID)
            result_findpeer = {'IP' : result_IPs}
            result[CID] = result_findpeer
            print(CID, result_findpeer)
            duplication.append(CID)

            json.dump(result, open(os.path.join(output, "track.json"),"w"))
            # Save for preparing that ipfs daemon quit while collecting
            json.dump(duplication, open(os.path.join(output, "track_duplicate.json"),"w"))
        else:
            print(f"{CID}'s provider node is not founded. It may blocked in gateways or in pinning services")
