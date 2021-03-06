# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from zc.buildout import UserError
from Products.GroupServer import creation
SITE_ID = 'initial_site'


class SetupGS(object):
    """ Setup GroupServer."""
    def __init__(self, app, zope_admin_name=''):
        self.set_admin_security_manager(app, zope_admin_name)
        self.app = makerequest.makerequest(app)

    def set_admin_security_manager(self, app, zope_admin_name=''):
        'Dark magic to do with security'
        admin = app.acl_users.acl_users.getUserById(zope_admin_name)
        admin = admin.__of__(app.acl_users)
        newSecurityManager(None, admin)

    def create_site(self, siteId, title, supportEmail,
        admin_email, admin_password, canonicalHost, canonicalPort,
        smtp_host, smtp_port, smtp_user, smtp_password):
        '''Create a GroupServer site'''

        creation.manage_addGroupserverSite(self.app, siteId, title,
            supportEmail, admin_email, admin_password,
            canonicalHost, canonicalPort,
            smtp_host, smtp_port, smtp_user, smtp_password)

        if not hasattr(self.app, siteId):
            m = '"{0}" folder not found'.format(siteId)
            raise UserError(m)
        if not hasattr(getattr(self.app, siteId), 'Content'):
            m = '"Content" folder not found in {0}'.format(siteId)
            raise UserError(m)
        if not hasattr(getattr(getattr(self.app, siteId), 'Content'), SITE_ID):
            m = '"{0}" not found in the "{0}/Content" folder'.format(SITE_ID)
            raise UserError(m)

        vhm = getattr(self.app, 'virtual_hosting', None)
        if not vhm:
            m = 'Could not find the VHM in {0}'.format(self.app)
            raise UserError(m)
        #'++skin++skin_gs_ogn' does not work during install
        mappingD = {'host': canonicalHost,
                    'id': siteId,
                    'site': SITE_ID,
                    'skin': ''}
        mapping = '%(host)s/%(id)s/Content/%(site)s/%(skin)s\n' % mappingD
        vhm.set_map(mapping)
