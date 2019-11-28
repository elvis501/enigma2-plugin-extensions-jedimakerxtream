#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import os
import re
from Components.config import *
from plugin import cfg, hdr, rytec_url, rytec_file, sat28_file, alias_file
import urllib2
import json
import socket
import jediglobals as jglob
import xml.etree.ElementTree as ET
from StringIO import StringIO
import gzip


def checkGZIP(url):
	response = None
	request = urllib2.Request(url, headers=hdr)

	try:
		response= urllib2.urlopen(request)
		
		if response.info().get('Content-Encoding') == 'gzip':
			buffer = StringIO( response.read())
			deflatedContent = gzip.GzipFile(fileobj=buffer)
			return deflatedContent.read()
		else:
			return response.read()
	except:
		pass
		return response
		

def downloadlivecategories(url):
	jglob.livecategories = []
	valid = False
	response = checkGZIP(url)

	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
		
	if response != None and 'category_id' in response:
		jglob.haslive = True
		try:
			jglob.livecategories = json.loads(response)
			valid = True
			
		except:
			print("\n ***** download live category error *****")
			jglob.haslive = False
			pass
		
		if valid:	
			if jglob.livecategories == [] or 'user_info' in jglob.livecategories or 'category_id' not in jglob.livecategories[0]:
				jglob.haslive = False
				jglob.livecategories == []
				
			if jglob.livecategories != []:
				jglob.livecategories.append({'category_id':'0','category_name':'Live Not Categorised','parent_id':0})
			
			if not jglob.haslive or jglob.livecategories == []:
				jglob.live = False
	
		
def downloadvodcategories(url):
	jglob.vodcategories = []
	valid = False
	response = checkGZIP(url)
	
	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
		
	if response != None and 'category_id' in response:
		jglob.hasvod = True
		try:
			jglob.vodcategories = json.loads(response)
			valid = True
			
		except:
			print("\n ***** download vod category error *****")
			jglob.hasvod = False
			pass
			
		if valid:			
			if jglob.vodcategories == [] or 'user_info' in jglob.vodcategories or 'category_id' not in jglob.vodcategories[0]:
				jglob.hasvod = False
				jglob.vodcategories == []
				
			if jglob.vodcategories != []:
				jglob.vodcategories.append({'category_id':'0','category_name':'VOD Not Categorised','parent_id':0})
			
			if not jglob.hasvod or jglob.vodcategories == []:
				jglob.vod = False
			

def downloadseriescategories(url):
	jglob.seriescategories = []
	valid = False
	response = checkGZIP(url)
	
	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
		
	if response != None and 'category_id' in response:
		
		jglob.hasseries = True
		try:
			jglob.seriescategories = json.loads(response)
			valid = True
			
		except:
			print("\n ***** download series category error *****")
			jglob.hasseries = False
			pass
			
		if valid:	
			if jglob.seriescategories == [] or 'user_info' in jglob.seriescategories or 'category_id' not in jglob.seriescategories[0]:
				jglob.hasseries = False
				jglob.seriescategories == []
				
			if jglob.seriescategories != []:
				jglob.seriescategories.append({'category_id':'0','category_name':'Series Not Categorised','parent_id':0})
			
			if not jglob.hasseries or jglob.seriescategories == []:
				jglob.series = False
		

def downloadlivestreams(url):
	jglob.livestreams = []
	valid = False
	response = checkGZIP(url)
	
	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
	
	if response != None and 'category_id' in response:
		jglob.haslive = True
		
		try:
			jglob.livestreams = json.loads(response)
			valid = True
				
		except:
			print("\n ***** download live streams error *****")
			jglob.haslive = False
			pass
			
	if valid:
		if jglob.livestreams == [] or 'user_info' in jglob.livestreams or 'category_id' not in jglob.livestreams[0]:
			jglob.haslive = False
			jglob.livestreams = []

		if jglob.haslive == False:
			jglob.live = False
		

def downloadvodstreams(url):
	jglob.vodstreams = []
	valid = False
	response = checkGZIP(url)
	
	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
	
	if response != None and 'category_id' in response:
		jglob.hasvod = True
		
		try:
			jglob.vodstreams = json.loads(response)
			valid = True
			
		except:
			print("\n ***** download vod streams error *****")
			jglob.hasvod = False
			pass
			
	if valid:
		if jglob.vodstreams == [] or 'user_info' in jglob.vodstreams or 'category_id' not in jglob.vodstreams[0]:
			jglob.hasvod = False
			jglob.vodstreams = []

		if jglob.hasvod == False:
			jglob.vod = False


def downloadseriesstreams(url):
	jglob.seriesstreams = []
	valid = False
	response = checkGZIP(url)
	
	# try a second time if first attempt failed. 
	if response == None:
		response = checkGZIP(url)
	
	if response != None and 'category_id' in response:
		jglob.hasseries = True
		
		try:
			jglob.seriesstreams = json.loads(response)
			valid = True
		except:
			print("\n ***** download series streams error *****")
			jglob.hasseries = False
			pass

	if valid:
		if jglob.seriesstreams == [] or 'user_info' in jglob.seriesstreams or 'category_id' not in jglob.seriesstreams[0]:
			jglob.hasseries = False
			jglob.seriersstreams = []

		if jglob.hasseries == False:
			jglob.series = False

	
def getlivestreams(playlist):
	jglob.livestreams = []
	temp_channels1 = []
	valid = False
	
	if 'available_channels' in playlist:
		for channel in playlist['available_channels']:
			if 'stream_type' in playlist['available_channels'][channel]:
				if playlist['available_channels'][channel]['stream_type'] == "live":
					temp_channels1.append(playlist['available_channels'][channel])
			
		try:
			jglob.livestreams = temp_channels1
			valid = True			
		except:
			print("\n ***** get live streams error *****")
			jglob.haslive = False
			pass

	if valid:
		if jglob.livestreams == [] or 'user_info' in jglob.livestreams or 'category_id' not in jglob.livestreams[0]:
			jglob.haslive = False
			jglob.livestreams = []

		if jglob.haslive == False:
			jglob.live = False
	

def getvodstreams(playlist):
	jglob.vodstreams = []
	temp_channels2 = []
	valid = False
	
	if 'available_channels' in playlist:
		for channel in playlist['available_channels']:
			if 'stream_type' in playlist['available_channels'][channel]:
				if playlist['available_channels'][channel]['stream_type'] == "movie":
					temp_channels2.append(playlist['available_channels'][channel])
			
		try:
			jglob.vodstreams = temp_channels2
			valid = True			
		except:
			print("\n ***** get vod streams error *****")
			jglob.hasvod = False
			pass
		
	if valid:
		if jglob.vodstreams == [] or 'user_info' in jglob.vodstreams or 'category_id' not in jglob.vodstreams[0]:
			jglob.hasvod = False
			jglob.vodstreams = []

		if jglob.hasvod == False:
			jglob.vod = False
			
	

def getseriesstreams(playlist):
	jglob.seriesstreams = []
	temp_channels3 = []
	valid = False
	
	if 'available_channels' in playlist:
		for channel in playlist['available_channels']:
			if 'stream_type' in playlist['available_channels'][channel]:
				if playlist['available_channels'][channel]['stream_type'] == "series":
					temp_channels3.append(playlist['available_channels'][channel])
			
		try:
			jglob.seriesstreams = temp_channels3
			valid = True			
		except:
			print("\n ***** get series streams error *****")
			jglob.hasseries = False
			pass
			
	if valid:
		if jglob.seriesstreams == [] or 'user_info' in jglob.seriesstreams or 'category_id' not in jglob.seriesstreams[0]:
			jglob.hasseries = False
			jglob.seriersstreams = []

		if not jglob.hasseries:
			jglob.series = False
					
													
def getM3uCategories(live,vod):
	
	lines = []
	
	address = jglob.current_playlist['playlist_info']['address']
	
	if jglob.current_playlist['playlist_info']['playlisttype'] == 'external':
		
		req = urllib2.Request(address, headers=hdr)
		try:
			response = urllib2.urlopen(req, timeout=cfg.timeout.value)
			lines = response.read().splitlines(True)
		except urllib2.URLError as e:
			print(e)
			pass
			
		except socket.timeout as e:
			print(e)
			pass
			
		except socket.error as e:
			print(e)
			pass
			
		except:
			print("\n ***** getM3uCategories unknown error")
			pass
		
			
	elif jglob.current_playlist['playlist_info']['playlisttype'] == 'local':
		with open(cfg.m3ulocation.value + address) as f:
			lines = f.readlines()
			
	channelnum = 0
	jglob.getm3ustreams = []
	group_title = 'Uncategorised'
	epg_name = ''
	name = ''
	source = ''
	
	for line in lines:
		
		if not line.startswith('#EXTINF') and not line.startswith('http'):
			continue
			
		if line.startswith('#EXTINF'):
				
			if re.search('group-title=\"(.*?)\"', line) is not None:
				group_title = re.search('group-title=\"(.*?)\"', line).group(1)
			else:
				group_title = ''
					
					
			if re.search('tvg-name=\"(.*?)\"', line) is not None:
				name = re.search('tvg-name=\"(.*?)\"', line).group(1).strip()
			else:
				if re.search('(?<=,).*$', line) is not None:
					name = re.search('(?<=,).*$', line).group().strip()
				else:
					name = ''
	
			if name == '':
				channelnum += 1
				name = 'Channel ' + str(channelnum)
				
		if line.startswith('http'):
			source = line.strip()
			
			stream = False
			
			if source.endswith('.ts') or source.endswith('.m3u8') or '/live' in source or '/m3u8' in source \
			or 'deviceUser' in source or 'deviceMac' in source or (source[-1].isdigit() and not source.endswith('.mp4') and not source.endswith('.mp3')):
				
				stream = True
				
				if live:
					if group_title == '':
						group_title = 'Uncategorised Live'
					jglob.getm3ustreams.append([group_title, epg_name, name, source, 'live'])
					
			if not stream:
				if vod:
					if group_title == '':
						group_title = 'Uncategorised'
					jglob.getm3ustreams.append([group_title, epg_name, name, source, 'vod'])

		
def downloadrytec():
		
	haslzma = False

	try:
		import lzma
		print('\nlzma success')
		haslzma = True
		
	except ImportError:
		
		try:
			from backports import lzma
			print("\nbackports lzma success")
			haslzma = True
			
		except ImportError:
			print("\nlzma failed")
			pass
			
		except:
			print("\n ***** downloadrytec lzma unknown error")
			pass
			
	
	
	req = urllib2.Request(rytec_url, headers=hdr)
	try:
		response = urllib2.urlopen(req)
		with open(rytec_file,'wb') as output:
			output.write(response.read())
			
	except urllib2.URLError as e:
		print(e)
		pass
		
	except socket.timeout as e:
		print(e)
		pass   
		
	except socket.error as e:
		print(e)
		pass
		
	except:
		print("\n ***** downloadrytec download unknown error")
		pass
	
	if os.path.isfile(rytec_file) and os.stat(rytec_file).st_size > 0 and haslzma:
		with lzma.open(rytec_file, 'rb') as fd:

			with open(sat28_file, 'w') as outfile:
				for line in fd:
					
					if "<!-- 28.2E -->" in line and "0000FFFF" not in line:
						 jglob.rytecnames.append(line)
					# get all 28.2e but ignore bad epg importer refs 
					if '28.2E' in line \
					and '1:0:1:C7A7:817:2:11A0000:0:0:0:' not in line \
					and '1:0:1:2EEF:7EF:2:11A0000:0:0:0:' not in line :
						outfile.write(line)		
						
		###################################################################################################
		# process all rytec refs
		
		rytec_allrefs = {}
		
		for line in jglob.rytecnames:
			serviceref = ''
			epg_channel_id = ''
			channelname = ''
		
			if re.search('(?<=<\/channel><!-- ).*(?= --)', line) is not None:
				channelname = re.search('(?<=<\/channel><!-- ).*(?= --)', line).group()
				
			if re.search('(?<=\">1).*(?=<\/)', line) is not None:
				serviceref = re.search('(?<=\">1).*(?=<\/)', line).group()
				
			if re.search('(?<=id=\")[a-zA-Z0-9\.]+', line) is not None:
				epg_channel_id = re.search('(?<=id=\")[a-zA-Z0-9\.]+', line).group() 

			rytec_allrefs[channelname.lower()] = [serviceref, epg_channel_id, channelname]
		
				
							
		###################################################################################################
		# read rytec 28.2e file
		
		with open(sat28_file, 'r') as outfile:
			rytec_sat28 = outfile.readlines();
		rytec_ref = {}
		
		for line in rytec_sat28:
			
			serviceref = ''
			epg_channel_id = ''
			channelname = ''
			
			if re.search('(?<=<\/channel><!-- ).*(?= --)', line) is not None:
				channelname = re.search('(?<=<\/channel><!-- ).*(?= --)', line).group()
				
			if re.search('(?<=\">1).*(?=<\/)', line) is not None:
				serviceref = re.search('(?<=\">1).*(?=<\/)', line).group()
				
			if re.search('(?<=id=\")[a-zA-Z0-9\.]+', line) is not None:
				epg_channel_id = re.search('(?<=id=\")[a-zA-Z0-9\.]+', line).group() 

			rytec_ref[channelname.lower()] = [serviceref, epg_channel_id, channelname]


		###################################################################################################
		# read iptv name file
		
		epg_alias_names = []

		if os.path.isfile(alias_file) and os.stat(alias_file).st_size > 0:
			with open(alias_file) as f:
				try:
					epg_alias_names = json.load(f)
				except ValueError as e:
					print("%s\n******** broken alias.txt file ***********" % e)
					print('\n******** check alias.txt file with https://jsonlint.com ********')
				 
		###################################################################################################
		
		return rytec_ref, epg_alias_names, rytec_allrefs
		

		
def downloadgetfile(url):
	valid = False
	response = checkGZIP(url)
	channelnum = 0
	m3uValues = {}
	series_group_title = 'Uncategorised'
	series_name = ''
	series_container_extension = ''
	series_url = ''
	count = 0
	
	if response != None:
		for line in response.splitlines():
			
			line = line.decode('utf-8')

			if not line.startswith('#EXTINF') and not line.startswith('http'):
				continue
		
			if line.startswith('#EXTINF'):

				if re.search('group-title=\"(.*?)\"', line) is not None:
					series_group_title = re.search('group-title=\"(.*?)\"', line).group(1)
				else:
					series_group_title = 'Uncategorised'
						
				if re.search('tvg-name=\"(.*?)\"', line) is not None:
					series_name = re.search('tvg-name=\"(.*?)\"', line).group(1).strip()
				else:
					if re.search('(?<=,).*$', line) is not None:
						series_name = re.search('(?<=,).*$', line).group().strip()
					else:
						series_name = ''

				if series_name == '':
					channelnum += 1
					series_name = 'Channel ' + str(channelnum)

			elif line.startswith('http'):
				series_url = line.strip()
			
				if '/series/' in series_url:
					
					if series_group_title not in m3uValues:
						m3uValues[series_group_title] = [{'name': series_name, 'url': series_url}]
					else:
						m3uValues[series_group_title].append({'name': series_name, 'url': series_url})
	
				else:
					continue

	return m3uValues
