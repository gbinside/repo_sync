#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# (c) Roberto Gambuzzi
# Creato:          07/01/2014 12:07:30
# Ultima Modifica: 08/01/2014 17:33:14
#
# v 0.0.1.1
#
# file: G:\repo GIT sparsi in giro\github\_sync_\__main__.py
# auth: Roberto Gambuzzi <gambuzzi@gmail.com>
# desc:
#
# $Id: __main__.py 08/01/2014 17:33:14 Roberto $
# --------------

from pprint import pprint
import ConfigParser
import subprocess
import urllib2
import base64
import json
import sys
import os

#http://stackoverflow.com/questions/2407126/python-urllib2-basic-auth-problem

# request = urllib2.Request("http://api.foursquare.com/v1/user")
# base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
# request.add_header("Authorization", "Basic %s" % base64string)
# result = urllib2.urlopen(request)


def do_work(working_dir, ssh_url, name):
    print "do_work", working_dir, ssh_url, name
    os.chdir(working_dir)
    ret = subprocess.call(['git', 'clone', ssh_url])
    if ret == 128:  # already exists
        print "\nGIT PULL\n"
        try:
            os.chdir(os.path.join(working_dir, name))
        except:
            return ret
        ret = [subprocess.call(['git', 'fetch', '--all'])]
        ret.append(subprocess.call(['git', 'pull']))
    return ret


if __name__ == "__main__":
    #clone all git repos of a user
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    config = ConfigParser.ConfigParser()
    if os.path.exists('users.ini'):
        config.readfp(open('users.ini'))
    pprint(config.sections())
    for k in config.sections():
        print k, '>>>'
        pprint(config.items(k))

    for service in config.sections():
        try:
            skip = config.get(service, 'skip').split(',')
        except ConfigParser.NoOptionError, e:
            skip = []
        for k, v in config.items(service):
            if k.startswith('user'):
                user, passwd = v.split(':')
                auth_key = base64.encodestring(v).replace('\n', '')
                working_dir = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])), service, user)
                try:
                    os.makedirs(working_dir)
                except:
                    pass

                if service == 'github':
                    #_json = urllib.urlopen("https://api.github.com/users/%s/repos" % user)
                    request = urllib2.Request("https://api.github.com/user/repos")
                    request.add_header("Authorization", "Basic %s" % auth_key)
                    _json = urllib2.urlopen(request)
                    for row in json.load(_json):
                        ssh_url = row['ssh_url']
                        if row['name'] not in skip:
                            do_work(working_dir, ssh_url, row['name'])

                elif service == 'bitbucket':
                    request = urllib2.Request("https://bitbucket.org/api/1.0/user/repositories")
                    request.add_header("Authorization", "Basic %s" % auth_key)
                    _json = urllib2.urlopen(request)
                    for row in json.load(_json):
                        #git clone git@bitbucket.org:
                        if row['owner'] == user:
                            #https://gambuzzi@bitbucket.org/webgriffe/drupal_sarchio.git
                            ssh_url = row["resource_uri"].replace('/1.0/repositories/',
                                                                  'https://%s@bitbucket.org/' % v) + '.git'
                            if row['name'] not in skip:
                                do_work(working_dir, ssh_url, row['name'])

