#!/usr/bin/env python3

import json
import geocoder
import folium as g
import os

def create_ip_list(fd):
	ip_list = []
	json_data = json.load(fd)

	for key in json_data.keys():
		for ip in json_data[key]['IP']:
			ip_list.append(ip)

	ip_list = list(dict.fromkeys(ip_list))
	fd.close()

	return ip_list
	
def create_map(file_path, output):
	ip_list = create_ip_list(fd = open(file_path,"r"))
	data = {}

	for i in range(len(ip_list)):
		l = str(geocoder.ip(ip_list[i]).latlng)
		
		try:
			data[l] = data[l]+' '+ip_list[i]
		except KeyError:
			data[l] = ip_list[i]

	json_data = json.loads(json.dumps(data))

	location = []
	for key in json_data.keys():
		location.append(key) 

	map_html = g.Map(location=[12, 12], zoom_start=3)

	for i in range(len(location)):
		if location[i] == '[]': # Except bogon ip
			continue
		popup_ = g.Popup('<br>'.join(data[location[i]].split(" ")))
		marker = g.Marker(location=list(map(float, location[i][1:-1].split(", "))), popup=popup_, icon=g.Icon(color='blue'))
		marker.add_to(map_html)

	map_html.save(os.path.join(output, "IPMAP_result.html"))
