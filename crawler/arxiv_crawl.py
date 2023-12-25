import requests
from lxml import etree
from pymongo import MongoClient
import pprint
import io
import os


class DataBase:
    def __init__(self, host='172.27.88.132', port=27017, db_name='arxiv', collection_name='arxiv_crawl'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_metadata(self, metadata):
        """
        Add one piece of metadata to the collection
        :param paper_id: id of the paper
        :param metadata: metadata of the paper
        :return: None
        """
        try:
            if not self.collection.find_one({"id": metadata["id"]}):
                self.collection.insert_one(metadata)
                print("[META] Successfully add metadata to the collection")
            else:
                print("[META] Metadata already exists")
        except Exception as e:
            print(e)


def fetch_metadata(url: str, headers) -> dict:
    """
    Fetch metadata from arxiv.org
    :param url: url of the paper
    :param headers: headers
    :return: metadata
    """
    month_mapping = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                     "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    try:
        metadata = {"id": url.split('/')[-1]}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = etree.HTML(response.text.encode('utf-8'))
            metadata["submitter"] = html.xpath('//*[@id="abs-outer"]/div[1]/div[4]/text()')[1][7:-2]
            metadata["authors"] = html.xpath('//*[@id="abs"]/div[2]/a/text()')
            metadata["title"] = html.xpath('//*[@id="abs"]/h1/text()')[0]
            comments = html.xpath('//td[@class="tablecell comments mathjax"]/text()')
            metadata["comments"] = comments[0] if comments else None
            journal_ref = html.xpath('//td[@class="tablecell jref"]/text()')
            metadata["journal_ref"] = journal_ref[-1] if journal_ref else None
            doi = html.xpath('//td[@class="tablecell doi"]/a/text()')
            metadata["doi"] = doi[0][16:] if doi else None
            report_no = html.xpath('//td[@class="tablecell jref"]/text()')
            metadata["report-no"] = report_no[0] if report_no else None
            metadata["categories"] = html.xpath('//td[@class="tablecell subjects"]/ \
                                                span[@class="primary-subject"]/text()')[0].split('(')[-1][:-1]
            license = html.xpath('//div[@class="abs-license"]/a/@href')
            metadata["license"] = license[0] if license else None
            metadata["abstract"] = html.xpath('//*[@id="abs"]/blockquote/text()')[1]
            # versions
            versions = []
            version = html.xpath('//div[@class="submission-history"]/strong/a/text()')
            version.append(html.xpath('//div[@class="submission-history"]/strong/text()')[-1])
            created = [elem.strip() for elem in html.xpath('//div[@class="submission-history"]/text()')[4::2]]
            for i in range(len(version)):
                versions.append({"version": version[i], "created": created[i]})
            metadata["versions"] = versions
            # date
            date = html.xpath('//div[@class="submission-history"]/text()')[-2][:]
            date = date.strip().split(' ')
            if len(date[1]) == 1:
                date[1] = '0' + date[1]
            metadata["update_date"] = f'{date[3]}-{month_mapping[date[2]]}-{date[1]}'
            # FIXME: the update_date crawled from arxiv.org does not correspond to the field update_date in the dataset
            print("[META] Successfully fetch metadata")
            return metadata
        else:
            print('Request Error')
    except Exception as e:
        print(f"[META ERROR]{e}")


def download_pdf(url: str, headers, file_name: str, file_path: str):
    """
    Download pdf file from arxiv.org
    :param url: url of the paper
    :param headers: headers
    :param file_name: name of the pdf file
    :param file_path: path to save the pdf file
    :return: None
    """
    try:
        url = url.replace('abs', 'pdf') + '.pdf'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if not os.path.exists(os.path.join(file_path, file_name)):
                pdf_content = io.BytesIO(response.content)
                with open(os.path.join(file_path, file_name), 'wb') as file:
                    file.write(pdf_content.read())
                print("[PDF] Successfully download pdf file")
            else:
                print("[PDF] File already exists")
        else:
            print('Request Error')
    except Exception as e:
        print(e)


def fetch_paper_url(field: str, skip: int, show: int):
    """
    Fetch paper urls from arxiv.org
    :param field: field of the paper
    :param skip: skip
    :param show: show
    :return: urls
    """
    try:
        paper_urls = []
        url = f"https://arxiv.org/list/{field}/pastweek?skip={skip}&show={show}"
        response = requests.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.text.encode('utf-8'))
            paper_urls = ["https://arxiv.org" + url for url in html.xpath('//div[@id="dlpage"]/dl/dt/span/a[1]/@href')]
            print("[URL] Successfully fetch urls")
            return paper_urls
        else:
            print('Request Error')
    except Exception as e:
        print(e)


test_url = "https://arxiv.org/abs/2312.02981"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64\
            ) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/93.0.4577.63 Safari/537.36'}

if __name__ == "__main__":
    # metadata = fetch_metadata(test_url, headers=headers)
    # pprint.pprint(metadata)
    # download_pdf(test_url, headers=headers, file_name="0704.0008.pdf",
    #              file_path="E:/2023fall/ICE2604/database/test_arxiv_pdf")

    db = DataBase()
    urls = fetch_paper_url(field="cs", skip=0, show=50)
    print(urls)
    tot = len(urls)
    for i, url in enumerate(urls):
        metadata = fetch_metadata(url, headers=headers)
        # pprint.pprint(metadata)
        db.add_metadata(metadata)
        # download_pdf(url, headers=headers, file_name=f"{metadata['id']}.pdf",
        #              file_path="E:/2023fall/ICE2604/database/arxiv_pdf")
        # print(f"[INFO][{i+1}/{tot}] Successfully add metadata and download pdf file")
        print(f"[INFO][{i + 1}/{tot}] Successfully add metadata")
