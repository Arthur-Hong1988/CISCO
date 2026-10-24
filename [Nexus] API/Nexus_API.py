# Edit by Arthur 20201221
import os
import sys
import re
import IPy
import json
import requests


def command_api():
    command = "show hostname"
    username = "readonly"
    password = "Re@1hblsqt"

    url = "http://30.127.0.5/ins"
    myheaders = {'content-type': 'application/json-rpc'}
    payload = [{"jsonrpc": "2.0", "method": "cli", "params": {"cmd": command, "version": 1}, "id": 1}]
    response = requests.post(url, data=json.dump(payload), headers=myheaders, auth=(username, password)).json()
    """
    {u'jsonrpc': u'2.0', u'result': {u'body': {u'hostname': u'W-C01-SF-SW-001.lu.com'}}, u'id':1}
    """
    hostname = response["result"]["body"]["hostname"]

    """
    {u'jsonrpc': u'2.0', u'result': {u'body': {u'TABLE_interface': {u'ROW_interface': [u'duplex': 'auto', u'type':
    u'--', u'vlan': u'routed', u'state': u'xcvrAbsent', u'interface': u'Ethernet1/4', u'speed': 'auto'}]}}}, u'id': 1}
    """
    interface = response["result"]["body"]["TABLE_interface"]["ROW_interface"]

    """
    {u'jsonrpc': u'2.0', u'result': {u'body': 
    {u'TABLE_moddiaginfo':{u'ROW_moddiaginfo': [{u'diagstatus': u'pass', u'mode': 1}, {u'diagstatus': u'Pass', u'mode': 2}]}, 
    u'TABLE_modwwninfo':{u'ROW_modwwninfo': []}
    u'TABLE_modinfo': {u'ROW_modinfo': [{u'modtype': u'48x1/10G SFP+ 4*40G Ethernet Module', u'status': u'ok', u'model':
    u'N9K-x9464'PX, u'modinf':1, u'ports': 52},{}]}, u'id':1}
    """
    moduleinfo = response["result"]["body"]["TABLE_modinfo"]["ROW_modinfo"]


command_api()
