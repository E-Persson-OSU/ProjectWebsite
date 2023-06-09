""" imports list """
import http.client
from http.client import RemoteDisconnected
import json
import os
import copy
import threading

GLOBAL_PARAMS = {
    'source_id': '',
    'page': 1,
    'last_name': '',
    'first_name': ''
}
__recent__ = '/recent/'
__search__ = '/search/'
__sources__ = '/sources/'


"""
------------------------------------------

            App Functions

------------------------------------------
"""

"""
    searches jailbase API for given first name and last name for each source_id provided
    might return data object as dictionary containing 'exception' key
"""
def searchjailbase(source_ids, last_name, first_name=''):
    search_results = []
    params = copy.deepcopy(GLOBAL_PARAMS)
    for source_id in source_ids:
        another_page = True
        page = 1
        while another_page:
            params.update({'source_id': source_id['source_id'], 'last_name': last_name, 'first_name': first_name, 'page': page})
            data = _requestbuilder(__search__, params)
            if 'exception' not in data:
                records = data['records']
                for record in records:
                    search_results.append(record)
                if data['next_page'] > 0:
                    page = data['next_page']
                else:
                    another_page = False
    return search_results
        

"""
    Gets recents from required source_id
    might return data object as dictionary containing 'exception' key
"""
def getrecent(source_id, page=1):
    params = copy.deepcopy(GLOBAL_PARAMS)
    params['source_id'] = source_id
    params['page'] = page
    return _requestbuilder(__recent__, params)


"""
------------------------------------------

            Init Functions

------------------------------------------
"""
"""
    populates source_ids table in database with information regarding source IDs for jails
"""
def getsourceids():
    records = _requestbuilder(__sources__, None)
    params = copy.deepcopy(GLOBAL_PARAMS)
    
    working_source_ids = []

    for record in records['records']:
        params['source_id'] = record['source_id']
        data = _requestbuilder(__recent__, params)
        if 'exception' not in data:
            working_source_ids.append(record)
            print('{} is a working souce_id\n'.format(params['source_id']))
        else:
            print('{} is broken\n'.format(params['source_id']))


    return working_source_ids



"""
------------------------------------------

            Internal Functions

------------------------------------------
"""

"""builds a request to send to the jailbase API, sends it,
   and returns a dictionary with the response
   If there was an issue retrieving the data, it returns
   a dictionary containing a key exception"""
def _requestbuilder(type, params):
    conn = http.client.HTTPSConnection("jailbase-jailbase.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': '{}'.format(os.environ['X-RapidAPI-Key']),
        'X-RapidAPI-Host': "jailbase-jailbase.p.rapidapi.com"
    }

    data = {}

    query = type

    """params will only be None if type is __sources__"""
    if params is not None:
        query = query + '?source_id={}'.format(params['source_id'])
        if len(params['last_name']) > 0:
            query = query + '&last_name={}'.format(params['last_name'])

        if len(params['first_name']) > 0:
            query = query + '&first_name={}'.format(params['first_name'])

        if params['page'] > 0:
            query = query + '&page={}'.format(params['page'])
    
    while True:
        try:
            conn.request('GET', query, headers=headers)
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            break   
        except (json.decoder.JSONDecodeError, http.client.ResponseNotReady, RemoteDisconnected) :
            data = {
                'exception': '500'
            }
            break

    return data
