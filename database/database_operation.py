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
    ##############################
    # change this directory
    pics_dir = '/mnt/e/2023fall/ICE2604/database/edited_100_PDF_pics'
    ##############################

    for i, paper in enumerate(collection.find()):
        # inquire id of files
        query = {'_id': paper.get('_id')}

        # field and values to be renewed
        pic_address = []
        for root, dirs, files in os.walk(os.path.join(pics_dir, paper.get('paper_id'))):
            for file_name in files:
                print("open", file_name + '\n')
                pic_address.append(f"/home/share/files/edited_100_PDF_pics/{paper.get('paper_id')}/{file_name}")
        update = {'$set': {'pics_address': pic_address}}

        # execute the update operation
        collection.update_one(query, update, upsert=True)

        print(f'successfully update {i}-th {paper.get("paper_id")} \n')


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


def format_authors_in_collection():
    """
    Connects to a MongoDB collection and formats the 'author' field for each document.
    It concatenates all author names into a single string and updates the document with this new string.

    """
    client = MongoClient()
    db = client.papers
    collection = db['100pdfs']

    # Iterate through all documents in the collection
    for document in collection.find({}):
        authors_parsed = document['author']['name']
        authors_joint = ''
        # Concatenate all but the last author with a comma
        for author in authors_parsed[:-1]:
            authors_joint += author + ', '
        # Add the last author without a comma
        authors_joint += authors_parsed[-1]
        # Update the document with the concatenated author string
        document['author'] = authors_joint
        collection.update_one({'_id': document['_id']}, {'$set': {'authors': authors_joint}})

    client.close()


def insert_arxiv_data():
    """
    Loads data from a JSON file and inserts it into a MongoDB collection.
    It filters out non-dict elements to ensure only valid data is inserted.

    """
    client = MongoClient('localhost', 27017)
    db = client['arxiv']
    collection = db['arxiv_new']

    with open('arxiv_edited.json', 'r') as file:
        data = json.load(file)

    # Check if data is a list and contains only dictionaries
    if isinstance(data, list):
        valid_data = [item for item in data if isinstance(item, dict)]
        collection.insert_many(valid_data)
    else:
        print("Data is not a list or contains non-dict elements.")

    client.close()


def update_authors_format():
    """
    Connects to a MongoDB collection and updates the format of the 'authors_parsed' field for each document.
    It reverses the order of each author's name parts and concatenates them into a single string.

    """
    client = MongoClient()
    db = client.arxiv
    collection = db.arxiv

    # Iterate through all documents in the collection
    for document in collection.find({}):
        authors_parsed = document['authors_parsed']
        # Reverse and join each author's name parts
        authors_combined = [' '.join(author[::-1]).strip() for author in authors_parsed]
        # Update the document with the new author format
        document['author'] = authors_combined
        collection.update_one({'id': document['id']}, {'$set': {'author': authors_combined}})

    client.close()


def process_entry(entry):
    """
    Processes a single entry from the JSON file, adding a 'year' field derived from the 'id',
    replacing 'update_date' with 'date', and formatting the 'authors_parsed' field.

    :param entry: A dictionary representing a single JSON entry.
    :return: The processed entry or None if an error occurs.
    """
    try:
        # Extract year from the ID and add to the entry
        year = 2000 + int(entry["id"][:2])
        entry["year"] = year

        # Handle missing update_date
        if "update_date" in entry:
            entry["date"] = entry.pop("update_date")
        else:
            entry["date"] = None

        # Handle empty authors list and format authors' names
        authors_combined = []
        if "authors_parsed" in entry and entry["authors_parsed"]:
            for author in entry["authors_parsed"]:
                # Combining first name, middle name (if present), and last name
                full_name = ' '.join(author[::-1]).strip()
                authors_combined.append(full_name)
        entry["author"] = authors_combined

        return entry
    except Exception as e:
        print(f"Error processing entry: {e}")
        return None


def process_json_file(file_path):
    """
    Processes a JSON file line by line, using the process_entry function for each JSON object.
    It captures any JSON decoding errors and continues processing.

    :param file_path: The path to the JSON file to be processed.
    :return: A list of processed JSON entries.
    """
    processed_data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                json_object = json.loads(line)
                processed_entry = process_entry(json_object)
                if processed_entry is not None:
                    processed_data.append(processed_entry)
            except json.JSONDecodeError as e:
                # Handle the JSON decode error here
                print(f"Error decoding JSON: {e}")
                continue
    return processed_data


def update_document_years():
    """
    Connects to a MongoDB collection and updates each document with the year extracted from the 'versions' field.
    It assumes the MongoDB is running on the local machine at the default port.

    """
    # 连接到MongoDB（这里假设MongoDB运行在本地默认端口）
    client = MongoClient('localhost', 27017)

    # 选择数据库和集合
    db = client.arxiv  # 替换为你的数据库名称
    collection = db.arxiv  # 替换为你的集合名称

    # 遍历集合中的所有文档
    for document in collection.find():
        # 假设日期信息在 'versions' 字段的 'created' 子字段中
        if 'versions' in document and document['versions']:
            for version in document['versions']:
                if 'created' in version:
                    created_date = version['created']
                    # 从日期字符串中提取年份
                    match = re.search(r'\d{4}', created_date)
                    if match:
                        year = int(match.group())
                        # 更新文档，添加年份字段
                        collection.update_one({'_id': document['_id']}, {'$set': {'year': year}})

    print("年份数据更新完成。")
    client.close()


if __name__ == '__main__':
    db = DataBase(host='10.80.135.195', port=27017, db_name='papers', collection_name='100pdfs')
    collection = db.collection
    update_column_pics_address(collection)
