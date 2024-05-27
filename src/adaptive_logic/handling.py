from src.graph.graphDBCypher import (
    createobj,
    GraphObject,
    behindFoo,
    pathFoo,
    nextFoo,
    get_name_id_graph, get_id_name_graph)
from src.adaptive_logic.schemes import ThemeRes, Result, ThemeReq


async def get_list_res_neg(neg_list):
    res = []
    foundMinCompl = {}
    for mod in neg_list:
        if mod.id in foundMinCompl:
            if mod.complexity < foundMinCompl[mod.id]:
                foundMinCompl[mod.id] = mod.complexity
        else:
            foundMinCompl[mod.id] = mod.complexity

    for id_name, complexity in foundMinCompl.items():
        if 0 < complexity:
            obj = createobj(id_name)
            obj.count = 1
            obj.complexity = complexity - 1
            res.append(obj)
        else:
            list_obj = behindFoo(id_name)
            for obj in list_obj:
                obj.count = 1
                obj.complexity = 2
            res.extend(list_obj)
    return res


async def get_list_res_pos(pos_list, topic: str, list_studied=[]):
    res = []
    foundMinCompl = {}

    for mod in pos_list:
        if mod.id in foundMinCompl:
            if mod.complexity > foundMinCompl[mod.id]:
                foundMinCompl[mod.id] = mod.complexity
        else:
            foundMinCompl[mod.id] = mod.complexity

    for id_name, complexity in foundMinCompl.items():
        if 1 < complexity:
            list_studied.append(id_name)
            if topic:
                list_obj = pathFoo(id_name, topic, list_studied)
            else:
                list_obj = nextFoo(id_name)
            for obj in list_obj:
                obj.count = 1
                obj.complexity = 0
            res.extend(list_obj)
        else:
            obj = createobj(id_name)
            obj.count = 1
            obj.complexity = complexity + 1
            res.append(obj)
    return res


async def create_with_neg(neg_list: list[ThemeReq], pos_list: list, count: int, list_studied: list,
                          topic: str = '') -> Result:
    res = await get_list_res_neg(neg_list)
    res = list(set(res))
    if len(res) > count:
        res.sort(key=lambda x: x.description, reverse=True)
        res: list[GraphObject] = res[:count]
        return Result(
            **{"tasks": [ThemeRes.model_validate(th, from_attributes=True) for th in res],
               "list_studied": list_studied})
    else:
        res_pos = await get_list_res_pos(pos_list, topic, list_studied)
        res_pos = list(set(res_pos))
        res_pos.sort(key=lambda x: x.description, reverse=True)
        res = res + res_pos[:count - len(res)]
        if len(res) < count:
            n = len(res)
            for r in res:
                r.count += 1
                n += 1
                if n >= count:
                    break
        return Result(
            **{"tasks": [ThemeRes.model_validate(th, from_attributes=True) for th in res],
               "list_studied": list_studied})


async def create_positive(pos_list: list[ThemeReq], count: int, list_studied: list, topic: str = '') -> Result:
    res = await get_list_res_pos(pos_list, topic, list_studied)
    res = list(set(res))
    res = [theme for theme in res if theme.id not in list_studied]
    if len(res) > count:

        res.sort(key=lambda x: x.description, reverse=True)
        res: list[GraphObject] = res[:count]
        return Result(
            **{"tasks": [ThemeRes.model_validate(th, from_attributes=True) for th in res],
               "list_studied": list_studied})
    else:
        if len(res) < count:
            n = len(res)
            for r in res:
                r.count += 1
                n += 1
                if n >= count:
                    break
        return Result(
            **{"tasks": [ThemeRes.model_validate(th, from_attributes=True) for th in res],
               "list_studied": list_studied})


def get_name_id(id_name):
    return get_name_id_graph(id_name)

def get_id_name(name):
    return get_id_name_graph(name)
