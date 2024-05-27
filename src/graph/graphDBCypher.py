from pydantic import BaseModel
from src.config import driver


class GraphObject(BaseModel):
    id: str
    description: int
    count: int = 1
    complexity: int = 0

    def __lt__(self, other):
        return self.description < other.description

    def __hash__(self):
        return hash(self.id)


def behindFoo(id_n):
    with driver.session() as session:
        query = """MATCH (n:theme)-[:uses]->(:theme{id: $id}) RETURN n"""
        res = list(session.run(query, id=id_n))
        if res:
            result = [GraphObject(**{'id': i['n'].get('id'), 'description': i['n'].get('description')}) for i in res]
            return list(set(result))
        return []


def nextFoo(id_m: str):
    with driver.session() as session:
        query = """MATCH (:theme{id: $id})-[:uses]->(n:theme) RETURN n"""

        res = list(session.run(query, id=id_m))
        if res:
            result = [GraphObject(**{'id': i['n'].get('id'), 'description': i['n'].get('description')}) for i in res]
            return list(set(result))
        return []


def pathFoo(start: str, end: str, list_studied=[]):
    with driver.session() as session:
        if start != end:
            query = """MATCH path = shortestPath((start:theme {id: $name1})-[:uses]->(end:theme{id: $name2})) RETURN path"""
            res = list(session.run(query, name1=start, name2=end))
            if res:
                r = res[0]['path']
                res = [GraphObject(**{'id': i.get('id'), 'description': i.get('description')}) for i in r.nodes]
                for i in res:
                    if i.id not in list_studied:
                        return [i]
            else:
                return behindFoo(end)
        return []


def createobj(id_w):
    with driver.session() as session:
        query = """MATCH (n:theme{id: $name2})RETURN n"""
        res = list(session.run(query, name2=id_w))
        if res:
            result = [GraphObject(**{'id': i['n'].get('id'), 'description': i['n'].get('description')}) for i in res]
            return result[0]
        return []


def getThemeByIdTask(id_task):
    with driver.session() as session:
        query = """MATCH (n:theme)-[:link]->(m:task{id: $id}) RETURN n,m"""
        res = list(session.run(query, id=id_task))
        if res:
            return res
        return []


def get_name_id_graph(id_theme):
    with driver.session() as session:
        query = """MATCH (n:theme {id: $id}) RETURN n"""
        res = list(session.run(query, id=id_theme))
        if res:
            res = dict(res[0])
            return res.get('n').get('name')
        return 'Нет по данному айди'

def get_id_name_graph(theme):
    with driver.session() as session:
        query = """MATCH (n:theme {name: $name}) RETURN n"""
        res = list(session.run(query, name=theme))
        if res:
            res = dict(res[0])
            return res.get('n').get('id')
        return 'Нет такой темы в графе'