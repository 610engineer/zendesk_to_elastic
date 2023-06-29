from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
from elasticsearch import Elasticsearch
import os
import json
import env

# Zenpy credential

creds = {
        "token" : os.environ.get('ZEN_TOKEN'),
        "email" : os.environ.get('ZEN_EMAIL'),
        "subdomain" : os.environ.get('ZEN_SUBDOMAIN')
    }

def main():
    
    # Zenpy instance
    zenpy_client = Zenpy(**creds)

    tickets = zenpy_client.search(type='ticket' , status="closed")
    for ticket in tickets:

        # Elasticsearchにすでにチケット情報が存在している場合はスキップ
        if(search_document(ticket.id) == True):
            continue

        # チケット情報をdict型に変換
        ticket_data = ticket.to_dict()

        comment_list = []

        # チケットIDからチャット履歴を取得
        for comment in zenpy_client.tickets.comments(ticket = ticket.id):
            
            # チャットデータをdict型へ変換
            comment_data = comment.to_dict()

            # dict型からjsonへ変換
            comment_json = json.dumps(comment_data, indent = 4, ensure_ascii=False)

            # チャットリストへ追加
            comment_list.append(comment_json)

        # チャットリストをdict型に変換
        chat_json = {"chats": comment_list}

        # チケット情報のdictにチャットリストを追加
        ticket_data.update(chat_json)

        # チケット情報をjsonに変換
        ticket_json = json.dumps(ticket_data, indent = 4, ensure_ascii=False)
        # print(ticket_json)
        
        # Elasticsearchへチケット情報を登録
        insert_elasticsearch(ticket_json)


# Elasticsearchにチケット情報を登録する
def insert_elasticsearch(json_data):

    # エンドポイントを設定
    es = Elasticsearch(os.environ.get('ELASTICSEARCH_URL'))

    # "zen_test"のインデックスを作成し、jsonを登録
    res = es.index(index = "zen_test",
                   document = json_data)
    
    # エンドポイントとの接続をクローズ
    es.close()

# チケットIDを検索し、インデックスに存在する場合はTrue、ない場合はFlaseを返す
def search_document(docId):
    # エンドポイントを設定
    es = Elasticsearch(os.environ.get('ELASTICSEARCH_URL'))
    
    # indexの存在確認
    exist = es.indices.exists(index = "zen_test")

    # indexがない場合は作成
    if(exist == False):
        es.indices.create(index = "zen_test")

    # 検索クエリ作成
    query = {"query": {"match": {"id": docId}}}

    # _sourceから対象のidを検索
    search_result = es.search(index= "zen_test", body = query)

    # idが存在すればTrue、ない場合はFalseを返す
    if(search_result["hits"]["total"]["value"] == 0):
        return False
    else:
        return True


if __name__ == "__main__":
    main()