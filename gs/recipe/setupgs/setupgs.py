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
from Products.GroupServer.creation import manage_addGroupserverSite
from zc.buildout import UserError
SITE_ID = 'initial_site'


class SetupGS(object):
    """ Setup GroupServer."""
    def __init__(self, app, zope_admin_name=''):
        admin = app.acl_users.acl_users.getUserById(zope_admin_name)
        admin = admin.__of__(app.acl_users)
        newSecurityManager(None, admin)
        self.app = makerequest.makerequest(app)

    def create_site(self, siteId, title, admin_email, admin_password,
        zope_admin_id, timezone, canonicalHost, canonicalPort,
        smtp_host, smtp_port, smtp_user, smtp_password, databaseHost,
        databasePort, databaseUsername, databasePassword, databaseName):
        '''Create a GroupServer site'''

        manage_addGroupserverSite(self.app, siteId, title, admin_email,
            admin_password, zope_admin_id, timezone, canonicalHost,
            canonicalPort, smtp_host, smtp_port, smtp_user, smtp_password,
            databaseHost, databasePort, databaseUsername, databasePassword,
            databaseName)
        # TODO: turn the asserts into tests that raise zc.buildout.UserError
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
