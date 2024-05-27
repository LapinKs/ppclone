from fastapi import APIRouter, Query
from src.adaptive_logic.schemes import ByReq, Result
from src.adaptive_logic.handling import create_with_neg, create_positive, get_name_id, get_id_name

router = APIRouter(
    tags=['Для создания ответных тестов'],
    prefix="/api",
)


@router.post('')
async def main_foo(data: ByReq) -> Result:
    test, count = data.get_test()
    negative = [mod for mod in test if not mod.answer]
    positive = [mod for mod in test if mod.answer]

    if negative:
        res = await create_with_neg(negative, positive, count, data.list_studied, data.topic)
        return res
    return await create_positive(positive, count, data.list_studied, data.topic)


@router.get('/id/', name='Из id в имя')
async def get_name(id_name: str = Query()) -> str:
    return get_name_id(id_name)

@router.get('/name/', name='Из имени в id ')
async def get_name(name: str = Query()) -> str:
    return get_id_name(name)