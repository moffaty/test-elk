from services.client import Client
if __name__ == "__main__":
    client = Client()
    client.index_reload()
    client.doc_add()
    # print(client.upload_test_data())
    # client.format_output(client.test_queries())