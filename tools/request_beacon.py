#!/usr/bin/python3
from datetime import datetime
import urllib.request
import json
from valve.rcon import RCON
import logging
import sys
import os 

#
#		Config
#
dir_path = os.path.dirname(os.path.realpath(__file__))

def structUserConfig():
	try:
		return json.load(open(dir_path + '/user_config.json'))
	except:
		return {'api_key' : None, 'servers' : {}}


config = {
	'api_endpoint' : 'https://teamwork.tf/community/beacon',
	'user_config' : structUserConfig(),
}

logging.disable(logging.CRITICAL)

#
#		Helper functions
#

def saveUserConfig():
	with open(dir_path + '/user_config.json', "w") as storage_file:
		storage_file.write(json.dumps(config['user_config']))

def checkAPIKey():
	if config['user_config']['api_key'] == None:
		print('[!] You do not have an API key set yet. Copy this from your community provider page on teamwork.tf.')
		config['user_config']['api_key'] = input('[!] Enter API key: ').strip()
		saveUserConfig()

def setSignatureViaRCON(ip, port, signature, rcon_pass = None):
	addr = ip+':'+port
	if rcon_pass == None:
		serverConfig = config['user_config']['servers'][addr]
	else:
		serverConfig = {'rcon' : rcon_pass}
	try:
		with RCON((ip, int(port)), serverConfig['rcon']) as rcon:
			rcon('tw_beacon "'+signature+'"')
			print('Beacon set via RCON for '+addr)
	except:
		return

def setSignatureViaFile(file_location, signature):
	lines = []
	isSet = False
	with open(file_location) as infile:
		for line in infile:
			if 'tw_beacon' in line:
				line = 'tw_beacon "'+signature+'"'
				isSet = True
			lines.append(line)

	if isSet == False:
		lines.append('tw_beacon "'+signature+'"')

	with open(file_location, 'w') as outfile:
		for line in lines:
			outfile.write(line)

	print('Beacon set in config file '+file_location+' for '+addr)
	return

def requestBeacon(ip, port, rcon_set = False, rcon_pass = None, file_set = False, file_location = None):
	data = bytes(urllib.parse.urlencode({
		'api_key' : config['user_config']['api_key'],
		'port' : port,
		'ip' : ip,
	}).encode())
	api_response = json.loads(urllib.request.urlopen(config['api_endpoint'], data).read().decode('utf-8'))
	if api_response['error'] == False:
		addr = ip+':'+port
		print('Congratulations! You\'ve created the signature for '+addr+':')
		print('tw_beacon "'+api_response['signature']+'"')
		if rcon_set == True:
			if addr not in config['user_config']['servers'] and rcon_pass == None:
				print('[!] This server has not been stored yet.')
				print('[!] Enter the RCON password to let this script automatically set the tw_beacon.')
				rcon_pass = input('[!] RCON Password for '+addr+': ').strip()
				config['user_config']['servers'][addr] = {'rcon' : rcon_pass}
				saveUserConfig()
			setSignatureViaRCON(ip, port, api_response['signature'], rcon_pass = rcon_pass)
		elif file_set == True:
			if addr not in config['user_config']['servers'] and file_location == None:
				print('[!] This server has not been stored yet.')
				print('[!] Enter the .cfg location to let this script automatically set the tw_beacon.')
				file_location = input('[!] Config file location for '+addr+' (specify full path): ').strip()
				config['user_config']['servers'][addr] = {'file' : file_location}
				saveUserConfig()
			setSignatureViaFile(file_location, api_response['signature'])
		else:
			print('(copy this line and paste this in your server.cfg)')
			print('(make sure you restart the gameserver after setting it)')
	else:
		print('teamwork.tf responded with an error:')
		print(api_response['message'])


def printHeader(title):
	print('-' * 48)
	print(' '+title)
	print('-' * 48)

def printOptions(options):
	print('Choose one of the following options:')
	for option in options:
		print(options[option] + ' ' * (60 - len(options[option])) + option)

def interactiveBeaconRequest(chosenOption = None):
	checkAPIKey()
	if chosenOption == None:
		printHeader('main menu'.upper())
		options = {
			'request' : 'Request a new beacon for a server.', 
			'request-rcon' : 'Request a beacon and automaticly set this value via RCON.', 
			'request-file' : 'Request a beacon and add this cvar to a .cfg file.', 
			'refresh-all' : 'Refresh all beacons via RCON/File ('+str(len(config['user_config']['servers']))+' server(s) stored).',
		}
		printOptions(options)
		while chosenOption not in options:
			chosenOption = input('I choose: ')

	if chosenOption == 'request':
		chosenIp = input('Specify the IP for the gameserver you want a beacon for: ')
		chosenPort = input('Specify the port for the gameserver you want a beacon for: ')
		requestBeacon(chosenIp, chosenPort, rcon_set = False, rcon_pass = None, file_set = False, file_location = None)
	elif chosenOption == 'request-rcon':
		chosenIp = input('Specify the IP for the gameserver you want a beacon for: ')
		chosenPort = input('Specify the port for the gameserver you want a beacon for: ')
		requestBeacon(chosenIp, chosenPort, rcon_set = True, rcon_pass = None, file_set = False, file_location = None)
	elif chosenOption == 'request-file':
		chosenIp = input('Specify the IP for the gameserver you want a beacon for: ')
		chosenPort = input('Specify the port for the gameserver you want a beacon for: ')
		requestBeacon(chosenIp, chosenPort, rcon_set = False, rcon_pass = None, file_set = True, file_location = None)
	else:
		for server in config['user_config']['servers']:
			print('-' * 48)
			addrParts = server.split(':')
			print('Requesting new beacon for '+server+'.')
			rcon_set = False
			rcon_pass = None
			file_set = False
			file_location = None
			if 'rcon' in config['user_config']['servers'][server]:
				rcon_set = True
				rcon_pass = config['user_config']['servers'][server]['rcon']
			else:
				file_set = True
				file_location = config['user_config']['servers'][server]['file']
			requestBeacon(addrParts[0], addrParts[1], rcon_set, rcon_pass, file_set, file_location)

	

if __name__ == '__main__':
	if len(sys.argv) == 2:
		# ./request_beacon.py refresh-all
		# Will refresh all servers automaticlly.
		interactiveBeaconRequest(str(sys.argv[1]))
	elif len(sys.argv) == 5:
		if str(sys.argv[4]) == 'rcon':
			# ./request_beacon.py <IP> <PORT> rcon <RCON_PASS>.
			requestBeacon(str(sys.argv[1]), str(sys.argv[2]), rcon_set = True, rcon_pass = str(sys.argv[4]))
		else:
			# ./request_beacon.py <IP> <PORT> file <CONFIG_LOCATION>.
			requestBeacon(str(sys.argv[1]), str(sys.argv[2]), file_set = True, file_location = str(sys.argv[4]))
	else:
		interactiveBeaconRequest()