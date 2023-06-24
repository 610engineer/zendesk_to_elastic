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
        for comment in zenpy_client.tickets.comments(ticket = ticket.id):
            comment_data = comment.to_dict()
            comment_json = json.dumps(comment_data, indent = 4, ensure_ascii=False)
            comment_list.append(comment_json)

        #print(comment_list)

        chat_json = {"chats": comment_list}

        ticket_data.update(chat_json)
        # チケット情報をjsonに変換
        ticket_json = json.dumps(ticket_data, indent = 4, ensure_ascii=False)
        print(ticket_json)
        

        #print(comment_list)

        
        # print("TICKET_JSON : ", ticket_json)
        insert_elasticsearch(ticket_json)

    #for comment in zenpy_client.tickets.comments(ticket=3):
    #    print(comment.body)


def insert_elasticsearch(json_data):
    es = Elasticsearch(os.environ.get('ELASTICSEARCH_URL'))

    res = es.index(index = "zen_test",
                   document = json_data)
    print(res)

    es.close()
    
    
    



if __name__ == "__main__":
    main()