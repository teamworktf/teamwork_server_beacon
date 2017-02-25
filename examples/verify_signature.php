<?php

require __DIR__ . '/SourceQuery/bootstrap.php';
use xPaw\SourceQuery\SourceQuery;

$config = [
	'public_key' => 'verification_key_teamwork.pem',
	'revocation_list' => 'https://teamwork.tf/community/beacon/revoked',
];

/**
  *		Retrieve the signature from a live server.
  */
function getServerSignature($ip, $port, $print_info = false) {
	$query = new SourceQuery();
	$beacon = null;
	
	try {
		$query -> Connect($ip, $port, 8, SourceQuery::SOURCE);

		$rules = $query->GetRules();
		if(isset($rules['tw_beacon'])) {
			$beacon = $rules['tw_beacon'];
		} else if(isset($rules['tw_version'])) {
			if($print_info)	echo "[retrieval] Server is running the plugin, but the beacon is not set.\n";
		} else {
			if($print_info)	echo "[retrieval] Server is not running the plugin\n";
		}
	} catch(Exception $e) {
		if($print_info)	echo $e->getMessage();
	} finally {
		$query->Disconnect();
		return $beacon;
	}
}

/**
  *		Verify that a signature is actually valid.
  */
function verifySignature($ip, $port, $signature, $print_info = false) {
	global $config;
	if($print_info)	echo "[validation] Validating signature $signature\n";

	$sigParts = explode(':', $signature);
	if($sigParts[0] == 'v1') {
		# tw_beacon : v1:<sequence id>:<community provider id>:<valid signature until>:<actual signature>
		$version = 1;
		$sequenceId = $sigParts[1];
		$providerId = $sigParts[2];
		$validUntil = $sigParts[3];
		$signedData = base64_decode($sigParts[4]);

		# <sequence id>:<ip>:<port>:<community provider id>:<valid signature until>
		$originalData = $sequenceId.':'.$ip.':'.$port.':'.$providerId.':'.$validUntil;

		$verify_key = openssl_pkey_get_public("file://".$config['public_key']);
		$validation = openssl_verify($originalData, $signature, $verify_key);
		if($validation == true) {
			# the signature is valid, but it might be expired. Be sure to always check the date!
			if(strtotime($validUntil) >= strtotime('now')) {
				try {
					$revoked = (array)json_decode(file_get_contents($config['revocation_list']));
					if (array_key_exists(($providerId.'-'.$sequenceId), $revoked) &&  $revoked[($providerId.'-'.$sequenceId)] == 'R') {
						if($print_info)	echo "[validation] INVALID SIGNATURE: revoked signature.\n";
						return false;
					} else {
						if($print_info)	echo "[validation] VALID SIGNATURE: for $ip:$port.\n";
						return true;
					}
				} catch(Exception $e) {
					# Soft fail for revocation list: we do not want a single point of failure
					if($print_info)	echo "[validation] VALID SIGNATURE: for $ip:$port (revocation lookup failed).\n";
					return true;
				}
			} else {
				if($print_info)	echo "[validation] INVALID SIGNATURE: expired signed date ($validUntil).\n";
				return false;
			}			
		} else {
			if($print_info)	echo "[validation] INVALID SIGNATURE: Mismatch between data.\n";
			return false;
		}
		
	} else {
		if($print_info)	echo "[validation] UNKNOWN: Not supported version / does not run the plugin.\n";
		return false;
	}
}

/**
  *		Get valid signature information based on IP, Port and the Signature you got from the server.
  */
function getSignatureInfo($ip, $port, $signature, $print_info = false) {
	if(verifySignature($ip, $port, $signature, $print_info)) {
		$sigParts = explode(':', $signature);
		if($sigParts[0] == 'v1') {
			$version = 1;
			$sequenceId = $sigParts[1];
			$providerId = $sigParts[2];
			$validUntil = $sigParts[3];

			return ['version' => $version, 
					'sequenceId' => $sequenceId, 
					'providerId' => $providerId, 
					'providerContext' => 'https://teamwork.tf/community/provider/'.$providerId.'.json', 
					'validUntil' => $validUntil];
		} else {
			return null;
		}
	} else {
		return null;
	}
}

// helper function, only used for this example
function requestInput($name) {
	if (PHP_OS == 'WINNT') {
		echo $name;
		return stream_get_line(STDIN, 1024, PHP_EOL);
	} else {
		return readline($name);
	}
}

// helper function, only used for this example
function printHeader($title) {
	echo "----------------------------------------------------------------------\n";
	echo $title."\n";
	echo "----------------------------------------------------------------------\n";
}

function printOptions($options) {
	echo "Choose one of the following options:\n";
	foreach ($options as $option => $desc) {
		echo $desc.str_repeat(' ', (60 - strlen($desc))).$option."\n";
	}
}

// helper function, only used for this example
function interactiveVerify() {
	$options = [
		'online' => 'Verify an online gameserver.',
		'offline' => 'Verify a signature offline without a gameserver.',
	];

	printHeader('teamwork beacon signature verifier');
	printOptions($options);
	$input = null;
	while(!array_key_exists($input, $options)) {
		$input = requestInput('I want to verify: ');
	}
	$ip = requestInput('IP of server: ');
	$port = requestInput('Port of server: ');
	if($input == 'online') {
		$signature = getServerSignature($ip, $port, true);
	} else {
		$signature = requestInput('Signature: ');
	}
	print_r(getSignatureInfo($ip, $port, $signature, true));
	echo str_repeat("\n", 2);;
}


interactiveVerify();
# Examples:
#echo getServerSignature('109.230.215.208', 27145, true);
#print_r(getSignatureInfo('109.230.215.208', 27145, 'v1:4:redsun:24-04-2018:MDwCHEP6WloptmfHX+ESBMpn38/hl1NJs4LfQtbX/BUCHGIhcUQbKKmNKMtk8/qvo1jPNpiEtwWbE9JZYA4=', true));