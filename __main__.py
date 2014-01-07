#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# (c) Roberto Gambuzzi
# Creato:          07/01/2014 12:07:30
# Ultima Modifica: 07/01/2014 12:07:41
#
# v 0.0.1.0
#
# file: G:\repo GIT sparsi in giro\github\_sync_\__main__.py
# auth: Roberto Gambuzzi <gambuzzi@gmail.com>
# desc:
#
# $Id: __main__.py 07/01/2014 12:07:41 Roberto $
# --------------

from pprint import pprint
import ConfigParser
import subprocess
import urllib
import json
import sys
import os

if __name__ == "__main__":
    #clone all git repos of a user
    os.chdir(os.path.dirname(sys.argv[0]))
    config = ConfigParser.ConfigParser()
    if os.path.exists('users.ini'):
        config.readfp(open('users.ini'))
    pprint(config.sections())
    for k in config.sections():
        print k, '>>>'
        pprint(config.items(k))

    for service in config.sections():
        if service == 'github':
            for k, v in config.items(service):
                if k.startswith('user'):
                    user, passwd = v.split(':')
                    working_dir = os.path.join(os.path.dirname(sys.argv[0]), '../%s/%s' % (service, user))
                    try:
                        os.makedirs(working_dir)
                    except:
                        pass
                    _json = urllib.urlopen("https://api.github.com/users/%s/repos" % user)
                    for row in json.load(_json):
                        ssh_url = row['ssh_url']
                        print ssh_url,
                        os.chdir(working_dir)
                        ret = subprocess.call(['git', 'clone', ssh_url])
                        if ret == 128: #already exists
                            print "\nGIT PULL\n"
                            os.chdir(os.path.join(working_dir, row['name']))
                            print subprocess.call(['git', 'fetch', '--all'])
                            print subprocess.call(['git', 'pull'])
