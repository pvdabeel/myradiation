#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# <bitbar.title>MyRadiation</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>pvdabeel@mac.com</bitbar.author>
# <bitbar.author.github>pvdabeel</bitbar.author.github>
# <bitbar.desc>Display uRadmonitor radiation sensor data in the OS X menubar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# Licence: GPL v3


# Installation instructions: 
# -------------------------- 
# You need to have a uradmonitor and an API userid / userhash for uradmonitor.com
# Ensure you have bitbar installed https://github.com/matryer/bitbar/releases/latest
# Ensure your bitbar plugins directory does not have a space in the path (known bitbar bug)
# Copy this file to your bitbar plugins folder and chmod +x the file from your terminal in that folder
# Run bitbar


import ast
import json
import sys
import datetime
import calendar
import base64
import math
import time
import os
import subprocess
import requests
import keyring
import getpass
import time
import decimal
import awspricing

from datetime import date
from tinydb import TinyDB, Query

# Nice ANSI colors                                                              
CEND    = '\33[0m'                                                              
CRED    = '\33[31m'                                                             
CGREEN  = '\33[32m'                                                             
CYELLOW = '\33[33m'                                                             
CBLUE   = '\33[34m'                                                             
CGRAY   = '\33[30m'             

uradmonitor_url      = "https://data.uradmonitor.com/api/v1/devices"
uradmonitor_userid   = keyring.get_password("myradiation-bitbar","userid")                
uradmonitor_userhash = keyring.get_password("myradiation-bitbar","userhash")                


# Support for OS X Dark Mode
DARK_MODE=os.getenv('BitBarDarkMode',0)


# Logo for both dark mode and regular mode
def app_print_logo():
    print ('|image=iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABSElEQVQ4jZXTvStFcRgH8I/bzSCZdIebQcrLoLAoJpTZZnNJZPInmAwGk5TCZFA2g/+BPwAlAwbdLNa7eB3Oc/jd4yyeeup3ft+XzvPy6/A3hrCOOj7jroImjnGfkjuScxXb6MIh+jES2B2esIEWtvCuID7FDMbxiq9CvobhTHCrqcFOALnZdYnBVZQiuDtpzXuFPswVxB+YLHD2QmsXA/7GOR4jT0rwAexWZd1+KCEsoRbnlxL8AfWqbFQ19CVgK/I2vofRi+6CwWfeyUXsJ2ATU373AC7ib/PYJOtqRTbnNOpoYDCyURALTSXfsOeSOhfironZAvYSmia/Y1zTPrbpRDCKtwRfC81QRbbbLVlTDkJwhsvE4AZHcT4IbkvyLvJVnsOq9onk0YuV4Pyscr6a71jGPMbQWWLQg4ngLIem7TXm8a/n/A3hKlhJn+lvQwAAAABJRU5ErkJggg==')
    print('---')

def color_radiation(mSvph):                                                         
    if mSvph <  0.13:                                                      
        return CGREEN +  str(mSvph) + CEND                                
    if mSvph < 0.20:                                                      
        return CYELLOW + str(mSvph) + CEND                                  
    if mSvph >= 0.20:                                                      
        return CRED + str(mSvph) + CEND                           
    return str(mSvph)

# The init function: Called to store your userid and secret hash 
def init():
    # Here we do the setup                                                      
    # Store access_token in OS X keychain on first run                          
    print ('Enter your uradmonitor.com user id:')                                    
    init_userid = raw_input()                                                 
    print ('Enter your uradmonitor.com user hash:')                                    
    init_userhash = getpass.getpass()                                           
    keyring.set_password("myradiation-bitbar","userid",init_userid)             
    keyring.set_password("myradiation-bitbar","userhash",init_userhash)     


# The main function
def main(argv):

    # CASE 1: init was called 
    if 'init' in argv:
       init()
       return
 

    # CASE 2: nor init nor update were called, AWS not available
    if DARK_MODE:
        color = '#FFDEDEDE'
        info_color = '#808080'
    else:
        color = 'black' 
        info_color = '#808080'

    try: 
        url = "https://data.uradmonitor.com/api/v1/devices"
        headers = { 'X-User-id':uradmonitor_userid , 'X-User-hash':uradmonitor_userhash }
        sensors = requests.get(url,headers=headers).json()

    except: 
       app_print_logo()
       print ('Failed to get data from uradmonitor.com | refresh=true terminal=true bash="\'%s\'" param1="%s" color=%s' % (sys.argv[0], 'init', color))
       return

    # CASE 3: all ok, all other cases
    app_print_logo()
   
    # loop through images, list all instances and print menu for creating new vm from image
    for sensor in sensors: 
       print ('%s : \t %s μSv/h | color=%s' % (datetime.datetime.fromtimestamp(int(sensor['timelast'])).strftime('%Y-%m-%d %H:%M:%S'),color_radiation(float(sensor['avg_cpm'])*float(sensor['factor'])), color))

def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

if __name__ == '__main__':
    main(sys.argv)
