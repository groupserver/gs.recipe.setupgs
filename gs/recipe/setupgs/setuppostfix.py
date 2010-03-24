#!/bin/python
from os import mkdir, chmod
from os.path import exists, join, abspath, split
from glob import glob
import stat
import Products.XWFMailingListManager

class SetupPostfix(object):
    def __init__(self, domainName, adminName):
        self.__pathToGroupServer = None
        self.domainName = domainName
        self.adminName = adminName
    
    @property
    def pathToGroupServer(self):
        if self.__pathToGroupServer == None:
            self.__pathToGroupServer = abspath('.')
        return self.__pathToGroupServer
    
    def copy_utils(self):
        utilsName = 'utils'
        scriptName = 'smtp2zope*py'
        
        moduleDir = join(*Products.XWFMailingListManager.__path__)
        utilsSrc = moduleDir
        
        utilsDest = join(self.pathToGroupServer, utilsName)
        if not exists(utilsDest):
            mkdir(utilsDest)
            
        # --=mpj17=-- Yes, Richard, this is a hack.
        for util in glob(join(utilsSrc, scriptName)):
            infile = file(util, 'r')
            utilName = split(util)[-1]
            outfile = file(join(utilsDest, utilName), 'w')
            for line in infile.readlines():
                if line == "AUTHORIZATION='admin:foobar'\n":
                    line = "AUTHORIZATION='%s'\n" % self.adminName
                outfile.write(line)
            infile.close()
            outfile.close()
            
        perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
            stat.S_IRGRP | stat.S_IXGRP
        for util in glob(join(utilsDest, scriptName)):
            chmod(util, perms)
    
    def create_postfix_config(self):
        configDest = join(self.pathToGroupServer, 'postfix_config')
        if not exists(configDest):
            mkdir(configDest)
        
        subs = {
            'gsPath': self.pathToGroupServer,
            'domain': self.domainName}
            
        verifyAddress = 'verify-address:   '\
            '"|%(gsPath)s/utils/smtp2zope-nonautomatic.py '\
            'http://%(domain)s/acl_users/verify_address"\n' % subs
        groupAutomatic = 'group-automagic:  '\
            '"|%(gsPath)s/utils/smtp2zope.py  '\
            'http://%(domain)s/ListManager"\n' % subs
        fileName = join(configDest, 'groupserver.aliases')
        gsAliases = file(fileName, 'w')
        gsAliases.write(verifyAddress)
        gsAliases.write(groupAutomatic)
        gsAliases.close()
        
        gsVirtualContents = '%(domain)s\tvirtual\n'\
            'verify@%(domain)s\tverify-address\n'\
            '@%(domain)s\tgroup-automagic\n' % subs
        fileName = join(configDest, 'groupserver.virtual')
        gsVirtual = file(fileName, 'w')
        gsVirtual.write(gsVirtualContents)
        gsVirtual.close()

