from services.client import Client

client = Client()
client.format_output(client.search_simple('Про'))
# print(json.dumps(client.anylize(ES.INDEX.NAME, {
#     "analyzer": "ru_en",
#     "text": "четко"
# }).body, ensure_ascii=False, indent=4))
# client.doc_add()
# for _ in range(10):
#     client.doc_add()