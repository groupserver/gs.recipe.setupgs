# coding=utf-8
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.GroupServer.groupserver import manage_addGroupserverSite

SITE_ID = 'initial_site'

class SetupGS(object):
    """ Setup GroupServer.
    
    """
    def __init__(self, app, zope_admin_name=''):
        admin = app.acl_users.acl_users.getUserById(zope_admin_name)
        admin = admin.__of__(app.acl_users)
        newSecurityManager(None, admin)
        self.app = makerequest.makerequest(app)
           
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
        assert hasattr(getattr(getattr(self.app, id), 'Content'), SITE_ID), '%s not found' % SITE_ID

        vhm = getattr(self.app, 'virtual_hosting', None)
        assert vhm, 'Could not find the VHM in %s' % self.app
        #'++skin++skin_gs_ogn' does not work during install
        mappingD = {'host': canonicalHost,
                    'id': id,
                    'site': SITE_ID,
                    'skin': ''} 
        mapping = '%(host)s/%(id)s/Content/%(site)s/%(skin)s\n' % mappingD
        vhm.set_map(mapping)

