import json
import os
import requests
from lxml import etree
from statistic import save_json
main_domain_full_name = {}
def get_main_domain_full_name():
    """
    Get the main domain of each subject
    :return: None
    """
    with open('main_domain_archive.json') as f:
        json_file = json.load(f)
        archives = json_file['archives']
        for archive in archives:
            main_domain_full_name[archive[0]] = archive[1]
        archives = json_file['defunct']
        for archive in archives:
            main_domain_full_name[archive[0]] = archive[1]


def fetch_full_name(url: str, dic:dict):
    """
    Fetch the full name of the subject
    :param url: url of the subject
    :return: None
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.text.encode('utf-8'))
            sub_domain = html.xpath("// *[ @ id = 'content'] / ul[2]/li/b/text()")
            # print(sub_domain)
            for string in sub_domain:
                lst = string.split(' - ')
                dic[lst[0]] = lst[1]
        else:
            print('Request Error')
    except Exception as e:
        print(e)
    return dic


if __name__ == '__main__':
    get_main_domain_full_name()
    full_name = main_domain_full_name.copy()
    for key, value in main_domain_full_name.items():
        url = f"https://arxiv.org/archive/{key}"
        full_name = fetch_full_name(url, full_name)
        print(f"Successfully fetch all subdomains under {key} ")
    print(full_name)
    save_json(full_name, "full_name.json")
