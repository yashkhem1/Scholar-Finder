from utils import extract_eid_citations, get_dict_author_id, get_authors_info, queryGenerator
from input import take_input
import csv

if __name__ == "__main__":
    dict_, APIkey = take_input()
    file_location = input('Enter File Path: ')
    query = queryGenerator(dict_)
    print(query)
    file = open(file_location, 'a')
    writer = csv.writer(file)
    writer.writerow(['Name', 'Indexed Name', 'Current Affiliation', 'Document count', 'Citations Count', 'Subject of Interest', 'Keywords'])
    list_eid = extract_eid_citations(APIkey, query)
    dict_author_id = get_dict_author_id(APIkey, list_eid)
    get_authors_info(APIkey, dict_author_id, writer)
    # print(authors_info)

    # auth_list = []

    # for auth_id in list(authors_info.keys()):
    #     auth_list.append(list(authors_info[auth_id].values()))
    # # auth_list.sort(key=lambda x: int(x[4]), reverse=True)
    # writer.writerows(auth_list)
    file.close()
