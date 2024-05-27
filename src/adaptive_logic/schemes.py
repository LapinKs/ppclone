from pydantic import BaseModel
from src.graph.graphDBCypher import getThemeByIdTask

class Task(BaseModel):
    id: str | list[str]
    answer: bool

    def get_theme(self):
        themes = []
        if isinstance(self.id, list):
            for i in self.id:
                reqv = getThemeByIdTask(i)
                complexity = int(dict(reqv[0]['m'])['description'])
                theme = [name['n']['id'] for name in reqv]
                themes.extend([ThemeReq(**{"id": i,
                                           "complexity": complexity,
                                           "answer": self.answer
                                           }) for i in theme])
        else:
            reqv = getThemeByIdTask(self.id)
            complexity = int(dict(reqv[0]['m'])['description'])
            theme = [name['n']['id'] for name in reqv]
            themes.extend([ThemeReq(**{"id": i,
                                       "complexity": complexity,
                                       "answer": self.answer
                                       }) for i in theme])
        return themes


class ThemeRes(BaseModel):
    id: str
    complexity: int
    count: int = 1


class Result(BaseModel):
    tasks: list[ThemeRes]
    list_studied: list[str]
    pass


class ThemeReq(BaseModel):
    id: str | list[str]
    complexity: int
    answer: bool

    def get_theme(self):
        if isinstance(self.id, list):
            return [ThemeReq(**{"id": i,
                                "complexity": self.complexity,
                                "answer": self.answer
                                }) for i in self.id]
        else:
            return [ThemeReq(**{"id": self.id,
                                "complexity": self.complexity,
                                "answer": self.answer
                                })]


class ByReq(BaseModel):
    test: list[ThemeReq | Task]
    list_studied: list[str] | None = []
    topic: str | None = None

    def get_test(self):
        res = []
        for i in self.test:
            res.extend(i.get_theme())
        return res, len(res)
