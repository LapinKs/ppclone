import threading
import requests
import json
import re
from neo4j import GraphDatabase
from time import time
import queue
from src.config import *

def get_files_in_folder(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        files = json.loads(response.text)
        return files
    return None

def work(file, que: queue.Queue):
    file_url = file['download_url']
    file_content = requests.get(file_url).text
    
    file_name = file['name'][:-3]    # достаю название файла
    id = re.findall(r'`{3}.*\n(.*).*\n`{3}', file_content)  #достаю id из файла
    level = re.findall(r'сложности::(.*)', file_content)[0].replace(' ', '')    #достаю уровень сложности
    conns = re.findall(r'\[\[(.*?)\]\]', file_content)   # достаю список соединений
        
    node = 'MERGE (:task {name: "' + file_name + '", id: "' + str(id[0][4:] if id else 0).replace(' ', '') + '", description: "' + str(level) + '"})'
    
    create_conn = []
    for conn in conns:
        create_conn.append('MATCH (a:theme {name: "' + conn.split('|')[0]
                            + '"}),(b:task {name: "' + file_name + '"}) MERGE (a)-[:link]->(b)')
    que.put_nowait([node,create_conn])


def find_sentence_in_file(files):
    if files:
        create_nodes = []
        create_conn = []
        
        threads = []
        que = queue.Queue()
        for file in files:
            if file['type'] == 'file':
                thread = threading.Thread(target=work, args=(file, que,))
                thread.start()
                threads.append(thread)
                
        for thread in threads:
            thread.join()
            
        while not que.empty():
            node, conns = que.get()
            create_nodes.append(node)
            create_conn += conns
            
        return create_nodes ,create_conn        
        
    return None, None


def Database_conn(create_nodes, create_conn):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="neo4j") as session:
            # session.execute_write(delete)    # на случай сброса данных в бд
            session.execute_write(employ_person_tx, create_nodes, create_conn)
            print("ОПЕРАЦИИ ПРОИЗВЕДЕНЫ УСПЕШНО")


def delete(tx):
    tx.run("""
        MATCH (n)
        OPTIONAL MATCH (n)-[r]-()
        DELETE n,r
        """
    )

def employ_person_tx(tx, create_nodes, create_conn):
    # Создание новых "task" нод, если они еще не существуют
    for node in create_nodes:
        tx.run(node)
    
    # Создание связей
    for conn in create_conn:
        tx.run(conn)
    
    # nodes = tx.run("""
    #             MATCH (n) return n
    #             """)
    
    # for node in nodes:
    #     count = tx.run("""
    #            MATCH (:task{id:$id})-[p]->(m)
    #            return count(p)
    #            """,id = dict(node['n'])['id'])
        
    #     tx.run("""
    #            MATCH (n:task{id:$id})
    #            set n.description = $count
    #            """,count = count.value()[0], id = dict(node['n'])['id'])
        
    
    


AUTH = (USERNAME, PASSWORD)


def main():
    # Укажите данные вашего репозитория
    owner = 'shbma'
    repo = 'math_graph'
    path = 'Типовые задания'    
    # create_nodes, create_conn = (None, None)
    t = time()
    files = get_files_in_folder(owner, repo, path)
    print(time() - t)
    create_nodes, create_conn = find_sentence_in_file(files)
    print(time() - t)
    Database_conn(create_nodes, create_conn)
    print(time() - t)

if __name__ == "__main__":
    main()