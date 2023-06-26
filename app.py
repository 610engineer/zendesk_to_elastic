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

    tickets = zenpy_client.tickets()
    for ticket in tickets:
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

def insert_elasticsearch(json_data):

    # エンドポイントを設定
    es = Elasticsearch(os.environ.get('ELASTICSEARCH_URL'))

    # "zen_test"のインデックスを作成し、jsonを登録
    res = es.index(index = "zen_test",
                   document = json_data)
    
    # エンドポイントとの接続をクローズ
    es.close()

if __name__ == "__main__":
    main()