# -*- coding: utf-8 -*-
# Module:        constant.py
# Author:        Raks Raja - Development Team
# Description:   This module is used to initialize all the constants which will be used in Barcode generation and scanning
# Copyrights:    2020 (c) All Rights Reserved

# Python libraries
import logging, base64

# Logger Config
logger = logging.getLogger(__name__)

class Constant:

    EMAIL = 'raks@labfellows.com'
    API_KEY = '70f7e376626b9382c09c4f71753abe31'
    SUBDOMAIN = 'labfellows'
    BASE_URL = 'http://api.labfellows.org/'
    encoded_auth = base64.b64encode(('%s:%s' % (EMAIL, API_KEY)).encode('utf8')).decode( 'utf8').replace('\n', '')

    headers = {
        'Content-Type': "application/vnd.api+json",
        'x-authorization': "Bearer organization %s" % SUBDOMAIN,
        'Authorization': "Basic %s" % encoded_auth
    }

