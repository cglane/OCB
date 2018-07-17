import os
from os import environ
dir_path = os.path.dirname(os.path.realpath(__file__))
path =  os.path.join(dir_path, 'sandbox')
preload_app = True
chdir = path
loglevel = 'error'