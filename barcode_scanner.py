# -*- coding: utf-8 -*-
# Module:        barcode_scanner.py
# Author:        Raks Raja - Development Team
# Description:   This module is used to process the barcodes in the S3 bucket and updates the loaction IDs and the status of item line IDs
# Copyrights:    2020 (c) All Rights Reserved

# Python libraries
import requests
import itertools
import re
from os import listdir
from os.path import isfile, join
import json
import random

from constant import Constant #Inheriting Constant class


class BarcodeScanner:

    def update_item_line_status(item_line_id, location_id):
        """Scans the item line and updates the location id and checked in, checked out status """
        try:
            check_in_check_out_url = Constant.BASE_URL + 'v2/inventory_item_lines/%s' % (item_line_id)
            location_url = Constant.BASE_URL + 'v2/inventory_item_lines/%s' % (item_line_id)
            location_definition_request = requests.get(location_url, headers=Constant.headers)
            if location_definition_request.status_code != 200:
                print('An exception has occured while processing the API request for the item line ID%s: %s %s' % (item_line_id, location_definition_request.status_code, location_definition_request.reason))
                return
            location_json = location_definition_request.json()
            previous_location_id = location_json['location']['id']
            check_in_check_out_status_definition_request = requests.get(check_in_check_out_url, headers=Constant.headers)
            if check_in_check_out_status_definition_request.status_code != 200:
                print('An exception has occured while processing the API request for the item line ID %s: %s %s' % (item_line_id, check_in_check_out_status_definition_request.status_code, check_in_check_out_status_definition_request.reason))
                return
            check_in_check_out_status_response = check_in_check_out_status_definition_request.json()
            mode = 'checkout' if  check_in_check_out_status_response['checked_out_at'] else 'checkin'
            if mode == 'checkin':
                checked_out = False
                status = 'checked-in'
            elif mode == 'checkout' and location_id == previous_location_id:
                checked_out = True
                status = 'checked-out'
            else:
                print('The item ' + str(item_line_id) + ' has been skipped (Previous Location: ' + str(previous_location_id) + ', Mode: ' + str(mode) + ')')
                return True
            param = json.dumps({
                "checked_out": checked_out,
                "location_id": location_id
            })
            requests.patch(check_in_check_out_url, data=param, headers=Constant.headers) #updates the loaction id and check in, check out status through api
            print('The item line ID ' + str(item_line_id) + ' has been ' + str(status) + ' for the location ID '+ str(location_id))
        except Exception as exception:
            print('An exception has occured: ' + str(exception))

    barcodes = [f for f in listdir("./barcodes") if isfile(join("./barcodes", f))]  # loads all the barcode images from current barcodes directory
    random.shuffle(barcodes)
    location_barcodes = [idx for idx in barcodes if idx[0].lower() == 'L'.lower()]
    location_ids = []
    for location_file in location_barcodes:
        location_id = re.findall('\d+', location_file)
        location_ids.append(location_id)
    location_ids = list(itertools.chain.from_iterable(location_ids))
    item_barcodes = [idx for idx in barcodes if idx[0].lower() == 'I'.lower()]
    item_ids = []
    item_line_ids = []
    for item_file in item_barcodes:
        id = re.findall('\d+', item_file)
        item_ids.append(id[0])
        item_line_ids.append(id[1])
    item_ids = list(dict.fromkeys(item_ids))
    random.shuffle(location_ids)
    random.shuffle(item_line_ids)
    print('Location IDs: ' + str(location_ids))
    print('Item IDs: ' + str(item_ids))
    print('Item line IDs: ' + str(item_line_ids))
    if len(barcodes) >= 100:
        barcodes = barcodes[:100]
    current_location_id = False
    for barcode in barcodes:
        if 'LOC' in barcode:
            current_location_id = int(re.findall('\d+', barcode)[0])
            location_url = Constant.BASE_URL + 'v2/locations/%s' % (current_location_id)
            location_definition_request = requests.get(location_url, headers=Constant.headers)
            if location_definition_request.status_code != 200:
                print(('An exception has occured while processing the Location ID  %s: %s %s' % (current_location_id, location_definition_request.status_code, location_definition_request.reason)))
            print('Current Location ID: ' + str(current_location_id))
            continue
        if 'INV' in barcode:
            if not current_location_id:
                continue
            item_line_id = int(re.findall('\d+', barcode)[1])
            update_item_line_status(item_line_id, current_location_id)