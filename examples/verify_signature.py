#!/usr/bin/python3
import valve.source.a2s
from OpenSSL import crypto
from datetime import datetime
import urllib.request
import json
import base64

config = {
	'public_key' : 'verification_key_teamwork.pem',
	'revocation_list' : 'https://teamwork.tf/community/beacon/revoked',
}
		
#
#		Retrieve the signature from a live server.
#
def getServerSignature(ip, port, print_info = False):
	server = valve.source.a2s.ServerQuerier((ip, port), timeout=8.0)
	rules = server.rules()
	if 'tw_beacon' in rules["rules"]:
		signature = rules["rules"]['tw_beacon']
		return signature
	elif 'tw_version' in rules["rules"]:
		if print_info == True:
			print('The beacon plugin seems to be loaded on the server, but no signature was found.')
		return None
	else:
		if print_info == True:
			print('No beacon nor plugin version was found. This server does not seem to run the beacon plugin.')
		return None

#
#		Verify that a signature is actually valid.
#
def verifySignature(ip, port, signature, check_revoked = True, print_info = False):
	if print_info == True:
		print('[validation] Validating signature: ' + signature)
	sigParts = signature.split(':')
	if(sigParts[0] == 'v1'):
		# tw_beacon : v1:<sequence id>:<community provider id>:<valid signature until>:<actual signature>
		version = 1
		sequenceId = sigParts[1]
		providerId = sigParts[2]
		validUntil = sigParts[3]
		signedData = base64.b64decode(sigParts[4])

		# <sequence id>:<ip>:<port>:<community provider id>:<valid signature until>
		originalData = sequenceId+':'+ip+':'+str(port)+':'+providerId+':'+validUntil

		pkey = crypto.load_publickey(crypto.FILETYPE_PEM, open(config['public_key'], "r").read())
		x509 = crypto.X509()
		x509.set_pubkey(pkey)
		try:
			crypto.verify(x509, signedData, originalData, 'sha1')
			# the signature is valid, but it might be expired. Be sure to always check the date!
			if datetime.strptime(validUntil, "%d-%m-%Y") >= datetime.now():
				try:
					revoked = json.loads(urllib.request.urlopen(config['revocation_list']+'?v='+str(version), timeout=4.0).read().decode('utf-8'))
					if (providerId+'-'+str(sequenceId)) in revoked and revoked[(providerId+'-'+str(sequenceId))] == 'R':
						if print_info == True:
							print('[validation] INVALID SIGNATURE: revoked signature.')
						return False
					else:
						if print_info == True:
							print('[validation] VALID SIGNATURE: for '+ip+':'+str(port)+'.')
						return True
				except Exception as e:
					# Soft fail for revocation list: we do not want a single point of failure
					if print_info == True:
						print('[validation] VALID SIGNATURE: for '+ip+':'+str(port)+' (revocation lookup failed).')
					return True
			else:
				if print_info == True:
					print('[validation] INVALID SIGNATURE: expired signed date ('+validUntil+').')
				return False
		except Exception as e:
			if print_info == True:
				print('[validation] INVALID SIGNATURE: Mismatch between data.')
			return False
	elif signature == None or signature == '':
		if print_info == True:
			print('[validation] UNKNOWN: Server does not run the plugin.')
		return False
	else:
		if print_info == True:
			print('[validation] UNKNOWN: Not supported version.')
		return False


#
#		Get valid signature information based on IP, Port and the Signature you got from the server.
#
def getSignatureInfo(ip, port, signature, check_revoked = True, print_info = False):
	if verifySignature(ip, port, signature, check_revoked, print_info) == True:
		sigParts = signature.split(':')
		if(sigParts[0] == 'v1'):
			version = 1
			sequenceId = sigParts[1]
			providerId = sigParts[2]
			validUntil = sigParts[3]

			return {'version' : version, 
					'sequenceId' : sequenceId, 
					'providerId' : providerId, 
					'providerContext' : 'https://teamwork.tf/community/provider/'+providerId+'.json', 
					'validUntil' : validUntil};
		else:
			return None;
	else:
		return None

def printHeader(title):
	print('------------------------------------------------')
	print(title)
	print('------------------------------------------------')

def printOptions(options):
	print('Choose one of the following options:')
	for option in options:
		print(options[option] + ' ' * (60 - len(options[option])) + option)

def interactiveVerify():
	printHeader('teamwork beacon signature verifier')
	options = {
		'online' : 'Verify an online gameserver.', 
		'offline' : 'Verify a signature offline without a gameserver.'
		};
	printOptions(options)
	chosenOption = None
	while chosenOption not in options:
		chosenOption = input('I want to verify: ')

	chosenIpPort = ''
	while len(chosenIpPort.split(':')) != 2:
		chosenIpPort = input('Provide ip:port: ')
	addrParts = chosenIpPort.split(':')
	chosenSignature = None
	if chosenOption == 'online':
		chosenSignature = getServerSignature(addrParts[0], int(addrParts[1]))
	else:
		chosenSignature = input('Enter the full signature: ')
	
	print(getSignatureInfo(addrParts[0], int(addrParts[1]), chosenSignature, print_info = True))



if __name__ == '__main__':
	# Example:
	#verifySignature('109.230.215.208', 27145, 'v1:4:redsun:24-04-2018:MDwCHEP6WloptmfHX+ESBMpn38/hl1NJs4LfQtbX/BUCHGIhcUQbKKmNKMtk8/qvo1jPNpiEtwWbE9JZYA4=', print_info = True)
	interactiveVerify()