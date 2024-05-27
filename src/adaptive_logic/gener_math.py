import requests

def req_math(lst: list[dict]) -> dict:
    """
    Получение ответа от генератора с листом запрошенных задач
    :param lst: лист для JSON для создания задач генератором
    :return: то что сгенерирует генератор
    """
    url = 'https://math-generator-7450.onrender.com/task'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=lst, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
        return {}
