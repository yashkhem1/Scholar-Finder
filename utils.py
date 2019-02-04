import numpy as np
import pandas as pd
import requests
import csv
import APIURI


def extract_eid_citations(key, query, index=0):
    par = {'apikey': key, 'query': query, 'sort': '-citedby-count,-coverDate', 'start': index, 'httpAccept': 'application/json'}
    res = requests.get(APIURI.SEARCH, params=par)
    res.raise_for_status()
    js = res.json()
    entries = js['search-results']['entry']
    list_eids = [x['eid'] for x in entries]
    # print(list_eids)
    return(list_eids)


def get_author_id(key, eid):
    # Here eid is that of the research paper
    par = {'apikey': key, 'httpAccept': 'application/json'}
    url = APIURI.ABSTRACT + '/eid/' + str(eid)
    print(url)
    res = requests.get(url, params=par)
    res.raise_for_status()
    js = res.json()
    authors = js['abstracts-retrieval-response']['authors']
    auid_list = []
    if authors is not None:
        authors = authors['author']
        for author in authors:
            auid_list.append(author['@auid'])
    keywords = js['abstracts-retrieval-response']['authkeywords']
    if keywords is not None:
        keywords = keywords['author-keyword']
        try:
            if(isinstance(keywords, list)):
                auth_keywords = [x['$'] for x in keywords]
            else:
                auth_keywords = [keywords['$']]
        except:
            auth_keywords = []

    else:
        auth_keywords = []
    return auid_list, auth_keywords


def get_author_keywords(key, eid):
    # Here eid is that of the research paper
    par = {'apikey': key, 'httpAccept': 'application/json'}
    url = APIURI.ABSTRACT + '/eid/' + str(eid)
    print(url)
    res = requests.get(url, params=par)
    res.raise_for_status()
    js = res.json()
    keywords = js['abstracts-retrieval-response']['authkeywords']['author-keyword']
    auth_keywords = [x['$'] for x in keywords]
    # print(auth_keywords)
    return auth_keywords


def get_dict_author_id(key, list_eid):
    dict_author_id = {}
    for eid in list_eid:
        try:
            auid_list, auth_keywords = get_author_id(key, eid)
            for auid in auid_list:
                print(auid)
                if auid in dict_author_id.keys():
                    dict_author_id[auid]['keywords'] += auth_keywords
                else:
                    dict_author_id[auid] = {}
                    dict_author_id[auid]['keywords'] = auth_keywords

        except:
            a = 1
    # print(dict_author_id)
    return dict_author_id


def get_author_info(key, auth_id):
    par = {'apikey': key, 'httpAccept': 'application/json'}
    url = APIURI.AUTHOR + '/author_id/' + str(auth_id)
    print(url)
    res = requests.get(url, params=par)
    res.raise_for_status()
    js = res.json()
    js = js['author-retrieval-response'][0]
    auth_info = {}
    auth_info['full-name'] = js['author-profile']['preferred-name']['given-name'] + js['author-profile']['preferred-name']['surname']
    auth_info['indexed-name'] = js['author-profile']['preferred-name']['indexed-name']

    if 'affiliation-current' in list(js['author-profile'].keys()):
        try:
            temp_list = js['author-profile']['affiliation-current']['affiliation']
            if isinstance(temp_list, list):
                auth_info['affiliation-current'] = temp_list[0]['ip-doc']['afdispname']
            else:
                auth_info['affiliation-current'] = temp_list['ip-doc']['afdispname']
        except:
            auth_info['affiliation-current'] = 'None'
    else:
        auth_info['affiliation-current'] = 'None'
    auth_info['document-count'] = js['coredata']['document-count']
    auth_info['cited-by-count'] = js['coredata']['cited-by-count']
    subj_interests = [x['$'] for x in js['subject-areas']['subject-area']]
    auth_info['subj_interests'] = subj_interests
    return auth_info


def get_authors_info(key, dict_author_id):
    for auth_id in list(dict_author_id.keys()):
        try:
            auth_info = get_author_info(key, auth_id)
            dict_author_id[auth_id] = dict(list(auth_info.items()) + list(dict_author_id[auth_id].items()))
        except:
            a = 1

    return dict_author_id


def queryGenerator(queryDict):
    query = ''
    for key in queryDict.keys():
        if(queryDict[key]) != '-1':
            if query == '':
                query = query + key + '(' + queryDict[key] + ')'
            else:
                query = query + ' and ' + key + '(' + queryDict[key] + ')'
    return query
