from bottle import Bottle, run, route, static_file, request, response, template, redirect
from string import Template
import json

import ipfsapi

api = ipfsapi.connect('ipfs.infura.io', 5001)

app = Bottle(__name__)

@app.get('/')
def root():
	return 'Root'

@app.post('/send/<data_str>')
def sendIPFS(data_str):

    res = api.add_json({'data': data_str})

    return {'status': 'ok', 'ipfs_hash': res}

@app.get('/get/<ipfs_hash>')
def getIPFS(ipfs_hash):

	res = api.cat(ipfs_hash)

	return {'status': 'ok', 'data': res}