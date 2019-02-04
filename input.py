

def take_input():
    APIkey = input('Enter API key: ')
    dict_ = {}
    specific = input('Enter G for general search and A for advanced search: ')
    if specific.lower() == 'g':
        search = input('Enter text to search anywhere in the document: ')
        dict_['all'] = str(search)
    else:
        print('Enter the following details (Enter -1 to leave the field blank)')
        abst = input('Search in Abstract: ')
        affil = input('Search in Affiliations: ')
        affilcity = input('Search in Affiliation City: ')
        affilcountry = input('Search in Affiliation Country: ')
        author_name = input('Search by Author name: ')
        fund_sponsor_acr = input('Search by Funding sponsor acronym: ')
        fund_sponsor = input('Search by Funding sponsor name: ')
        key = input('Search by keywords: ')
        title = input('Search by titles: ')
        dict_['abs'] = abst
        dict_['affil'] = affil
        dict_['affilcity'] = affilcity
        dict_['affilcountry'] = affilcountry
        dict_['author-name'] = author_name
        dict_['key'] = key
        dict_['title'] = title
        dict_['fund-acr'] = fund_sponsor_acr
        dict_['fund-sponsor'] = fund_sponsor

    return dict_, APIkey
