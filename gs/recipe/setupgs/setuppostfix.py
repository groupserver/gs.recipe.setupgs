#!/bin/python
from os import mkdir, chmod
from os.path import exists, join
from shutil import copy
from glob import glob
import stat
import Products.XWFMailingListManager

class SetupPostfix(object):
    def __init__(self, postfixConfigPath, postfixUser, 
                    postfixUserGroup, domainName):
        self.__postfixConfigPath = postfixConfigPath
        self.__postfixUser = postfixUser
        self.__postfixUserGroup = postfixUserGroup
        self.__pathToGroupServer = None
        self.__domainName = domainName
    
    @property
    def pathToGroupServer(self):
        if self.__pathToGroupServer == None:
            self.__pathToGroupServer = '.'
        return self.__pathToGroupServer
            
    def copy_utils(self):
        utilsName = 'utils'
        scriptName = 'smtp2zope*py'
        
        moduleDir = join(*Products.XWFMailingListManager.__path__)
        utilsSrc = join(moduleDir, utilsName)
        
        utilsDest = join(self.pathToGroupServer, utilsName)
        assert not(exists(utilsDest)), '%s already eists.' % utilsDest
        mkdir(utilsDest)
        
        for util in glob(join(utilsSrc, scriptName)):
            copy(util, utilsDest)
        
        perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
            stat.S_IRGRP | stat.S_IXGRP
        for util in glob(join(utilsDest, scriptName)):
            chmod(util, perms)

