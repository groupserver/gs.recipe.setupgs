# coding=utf-8
import sys, transaction, os
from glob import glob
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.GroupServer.groupserver import manage_addGroupserverSite
import commands

import Products.XWFMailingListManager, Products.XWFChat,\
    Products.GSAuditTrail, Products.GSGroupMember, Products.GSSearch,\
    Products.CustomUserFolder

def get_sql_filenames_from_module(module):
  path = os.path.join(os.path.join(*module.__path__), 'sql')
  retval = glob(os.path.join(path, '*sql'))
  assert type(retval) == list
  return retval
    
def execute_createuser(admin, user, host, port):
    cmd = 'createuser -d -r -l -S -U %s -h %s -p %s %s' %\
        (admin, host, port, user)
    commands.getoutput(cmd)
    
def execute_createdb(user, host, port, database):
    createdbcmd = 'createdb -E UTF8 -U %s -h %s -p %s %s' % \
        (user, host, port, database)
    commands.getoutput(createdbcmd)
    createlangcmd = 'createlang -U %s -h %s -p %s plpgsql %s' % \
        (user, host, port, database)
    commands.getoutput(createlangcmd)

def execute_psql_with_file(user, host, port, database, filename):
    cmd = 'psql -U %s -h %s -p %s -d %s -f %s' % (user, host, port,
        database, filename)
    status, output = commands.getstatusoutput(cmd)
    return (status, output)

class SetupGS(object):
    """ Setup GroupServer.
    
    """
    def __init__(self, app, zope_admin_name=''):
        admin = app.acl_users.acl_users.getUserById(zope_admin_name)
        admin = admin.__of__(app.acl_users)
        newSecurityManager(None, admin)
        self.app = makerequest.makerequest(app)
    
    def create_database_user(self, admin,user, host, port):
        execute_createuser(admin, user, host, port)
        
    def create_database(self, user, host, port, database):
        execute_createdb(user, host, port, database)
        
    def setup_database(self, user, host, port, sql_base, database):
        modules = (Products.XWFMailingListManager, Products.XWFChat, 
            Products.GSAuditTrail, Products.GSGroupMember,
            Products.GSSearch, Products.CustomUserFolder)            
        for module in modules:
            for fname in get_sql_filenames_from_module(module):
                s,o = execute_psql_with_file(user, host, port, database, 
                    fname)
                print ((o and o) or '.')
       
    def create_site(self, id, title, initial_user, initial_password,
        support_email, timezone, canonicalHost, databaseHost,
        databasePort, databaseUsername, databasePassword, databaseName):
        
        manage_addGroupserverSite(self.app, id, title, initial_user, 
            initial_password, support_email, timezone, canonicalHost,
            databaseHost, databasePort, databaseUsername,
            databasePassword, databaseName)

