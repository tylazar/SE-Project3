#! /usr/bin/python

import sys
import os
# print(sys.path, os.getcwd())
sys.path.append("/var/www/html/WebsiteDocker")
# print(sys.path, os.getcwd())

from app import app as application
