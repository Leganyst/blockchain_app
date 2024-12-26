# Мой адрес
ADDRESS = "0xec936f8b946a0baf7cfcf11b3b475a930c9ab396"
# Приватный ключ
PRIVATE_KEY = "4616de43be0c85458646327d280a19e7def44258e2237f0cb293d5d879a80bf2"

# Данные сети
NETWORK_URL = "http://127.0.0.1:8545"
NETWORK_ID = 1578


# Данные основного контракта
SMART_CONTRACT_ADDRESS = "0x655716A10B5A59c03efB64027dB34a3BC2dE5E3e"
SMART_CONTRACT_ABI = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "policyId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "policyHolder",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "ClaimPaid",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "message",
				"type": "string"
			}
		],
		"name": "Debug",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "policyId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "policyHolder",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "coverageAmount",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "endDate",
				"type": "uint256"
			}
		],
		"name": "PolicyCreated",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "policyId",
				"type": "uint256"
			}
		],
		"name": "claim",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "policyHolder",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "premium",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "coverageAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "durationType",
				"type": "uint256"
			}
		],
		"name": "createPolicy",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "getUserPolicies",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "policyId",
				"type": "uint256"
			}
		],
		"name": "getUserPolicyInfo",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "policyHolder",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "premium",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "coverageAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "endDate",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "isClaimed",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "insuranceToken",
		"outputs": [
			{
				"internalType": "contract ERC20",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "nextPolicyId",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "policies",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "policyHolder",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "premium",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "coverageAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "endDate",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "isClaimed",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]