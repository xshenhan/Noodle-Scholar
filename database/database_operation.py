from pymongo import MongoClient
import json
import os
from gridfs import GridFS


class DataBase:
    def __init__(self, host='172.27.88.132', port=27017, db_name='arxiv', collection_name='num_papers_authors'):
        self.collection_name = collection_name
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


def add_100_PDF_metadata(collection):
    """
    Add metadata of 100 papers to the collection
    :param collection: collection to be added
    :return: None
    """
    with open("100_PDF_MetaData.json", "r") as file:
        data = json.load(file)

    for paper_id, metadata in data.items():
        # paper_id, tag and metadata given in the json file
        collection.insert_one({"paper_id": paper_id, "tag": "geography"} | metadata)


def add_PDFs(db):
    """
    Put files into GridFS
    :param db: database
    :return: None
    """
    folder_path = '/mnt/e/2023fall/ICE2604/database/100_PDF'
    args = {"content_type": "PDF"}
    gfs = GridFS(db, collection="test")

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            print("open", file_name + '\n')
            with open(os.path.join(folder_path, file_name), "rb") as file:
                gfs.put(file, filename=file_name, **args)
            print(file_name, "successfully added\n")


def update_column_pdf_address(collection):
    """
    Add new columns to the collection
    :param collection: collection to be added
    :return: None
    """
    for i, paper in enumerate(collection.find()):
        # inquire id of files
        query = {'_id': paper.get('_id')}

        # field and values to be renewed
        update = {'$set': {'pdf_address': f'/home/share/files/100_PDF/{paper.get("paper_id")}.pdf'}}

        # execute the update operation
        collection.update_one(query, update, upsert=True)

        print(f'successfully update {i}-th {paper.get("paper_id")} \n')


def update_column_pics_address(collection):
    pics_dir = '/mnt/e/2023fall/ICE2604/database/100_PDF_pics'

    for root, dirs, files in os.walk(pics_dir):
        # print(f"root: {root}")
        # print(f"dirs: {dirs}")
        # print(f"files: {files}")
        try:
            paper = collection.find_one({"paper_id": os.path.split(root)[1]})

            query = {'_id': paper.get("_id")}
            address_files = [os.path.join("/home/share/files/100_PDF_pics/",os.path.split(root)[1], filename)
                             for filename in files]
            print(f"address_files: {address_files}")
            update = {'$set': {'pics_address': address_files}}

            # execute the update operation
            collection.update_one(query, update, upsert=True)
        except Exception as e:
            print(e)


def add_statistic_data(collection, file_name, key_name, value_name):
    """
    Add statistic data to the collection
    :param collection: collection to be added
    :param file_name: file name of the statistic data
    :param key_name: key name of the statistic data
    :param value_name: value name of the statistic data
    :return: None
    """
    data = []
    with open(file_name) as f:
        dic = json.load(f)
        for key, value in dic.items():
            data.append({key_name: key, value_name: value})
    collection.insert_many(data)


if __name__ == '__main__':
    # db = DataBase(collection_name='num_papers_main_subject')
    # collection = db.collection
    # add_statistic_data(collection, 'num_papers_authors.json', 'author', 'num_papers')
    # add_statistic_data(collection, 'num_papers_main_subject.json', 'main_subject', 'num_papers')
    # db = DataBase(collection_name='num_papers_sub_subject')
    # collection = db.collection
    # add_statistic_data(collection, 'num_papers_sub_subject.json', 'sub_subject', 'num_papers')
    db = DataBase(collection_name='num_papers_year', host='10.80.135.195')
    collection = db.collection
    add_statistic_data(collection, 'num_papers_year.json', 'year', 'num_papers')
