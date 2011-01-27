# coding=utf-8
import transaction, os
from glob import glob
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.GroupServer.groupserver import manage_addGroupserverSite
import commands

import Products.CustomUserFolder, Products.XWFMailingListManager,\
    Products.GSAuditTrail, add gs.profile.email.base,
    gs.group.member.invite, gs.profile.invite,\
    gs.profile.password, gs.profile.email.verify, Products.GSSearch, \
    Products.GSGroupMember, Products.XWFChat

def get_sql_filenames_from_module(module):
    path = os.path.join(os.path.join(*module.__path__), 'sql')
    retval = glob(os.path.join(path, '*sql'))
    retval.sort()
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
        
    def setup_database(self, user, host, port, database):
        # TODO: add gs.profile.email.base
        modules = (Products.CustomUserFolder, 
                    Products.XWFMailingListManager, Products.GSAuditTrail, 
                    gs.profile.email.base, gs.group.member.invite,
                    gs.profile.invite, gs.profile.password,
                    gs.profile.email.verify, Products.GSSearch,
                    Products.GSGroupMember, Products.XWFChat)
        for module in modules:
            for fname in get_sql_filenames_from_module(module):
                s,o = execute_psql_with_file(user, host, port, database, 
                    fname)
                print ((o and o) or '.')
       
    def create_site(self, id, title, admin_email, admin_password,
        user_email, user_password, zope_admin_id, support_email, 
        timezone, canonicalHost, canonicalPort, 
        smtp_host, smtp_port, smtp_user, smtp_password,
        databaseHost, databasePort, databaseUsername, databasePassword, 
        databaseName):
        
        manage_addGroupserverSite(self.app, id, title, admin_email, 
            admin_password, user_email, user_password, zope_admin_id, 
            support_email, timezone,  canonicalHost, canonicalPort, 
            smtp_host, smtp_port, smtp_user, smtp_password,
            databaseHost, databasePort, databaseUsername, 
            databasePassword, databaseName)
        assert hasattr(self.app, id), '%s not found'
        assert hasattr(getattr(self.app, id), 'Content'), 'Content not found'
        assert hasattr(getattr(getattr(self.app, id), 'Content'), 'example_site'), 'example_site not found'

        # --=mpj17=-- A useless attempt at setting the virtual host 
        #   mapping automatically. No matter what I do something
        #   always blanks the mapping, making it impossible to set up
        #   a GroupServer instance and site automatically.
        vhm = getattr(self.app, 'virtual_hosting', None)
        assert vhm, 'Could not find the VHM in %s' % self.app
        #'++skin++skin_gs_ogn' does not work during install
        mappingD = {'host': canonicalHost,
                    'id': id,
                    'site': 'example_site',
                    'skin': ''} 
        mapping = '%(host)s/%(id)s/Content/%(site)s/%(skin)s\n' % mappingD
        vhm.set_map(mapping)

