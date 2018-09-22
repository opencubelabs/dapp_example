from bottle import Bottle, run, route, static_file, request, response, template, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from string import Template
import json
import pymongo
import requests
import datetime
import time
import math
import hashlib as hl
import os
import smtplib
import boto3
import uuid
import base64

from Crypto import Random
from Crypto.Cipher import AES

import ipfsapi

api = ipfsapi.connect('localhost', 5001)

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]


class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

app = Bottle(__name__)

cipher = AESCipher('mysecretpassword')

# client = MongoClient('mongodb://kg:kg@54.160.234.161/kg_beta')
# db = client.kg_beta

@app.get('/')
def root():
	return static_file('index.html', root='templates/')

@app.get('/get')
def root():
	return static_file('view_file.html', root='templates/')

@app.post('/sendIPFS')
def sendIPFS():

	img_data = request.forms.get('img_data')

	encrypted = cipher.encrypt(img_data)

	res = api.add_json({'data': encrypted})

	return {'status': 'ok', 'ipfs_hash': res}

@app.get('/getIPFS/<ipfs_hash>')
def getIPFS(ipfs_hash):

	res = json.loads(api.cat(ipfs_hash))

	decrypted = cipher.decrypt(res['data'])

	return {'status': 'ok', 'data': decrypted}