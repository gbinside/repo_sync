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

import ConfigParser

if __name__=="__main__":
    #clone all git repos of a user
    config = ConfigParser.ConfigParser()
    config.readfp(open('users.ini'))
    
