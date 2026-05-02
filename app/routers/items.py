from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import crud
from app.models import ItemRead, ItemCreate, ItemUpdate

router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create(item: ItemCreate, session: AsyncSession = Depends(get_session)) -> ItemRead:
    """Створює новий елемент.

    Args:
        item: Дані для створення елемента.
        session: Асинхронна сесія бази даних.

    Returns:
        Створений елемент.
    """

    return await crud.create_item(session, item)


@router.get("/", response_model=list[ItemRead])
async def list_items(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        owner_id: Optional[int] = None,
        search: Optional[str] = None,
        sort_by: str = Query(default="id"),
        sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
        session: AsyncSession = Depends(get_session)
) -> list[ItemRead]:
    """Повертає список елементів із фільтрацією, пошуком і сортуванням.

    Args:
        skip: Кількість елементів, які потрібно пропустити.
        limit: Максимальна кількість елементів у відповіді.
        owner_id: Ідентифікатор власника для фільтрації.
        search: Текст для пошуку.
        sort_by: Поле для сортування.
        sort_order: Напрям сортування.
        session: Асинхронна сесія бази даних.

    Returns:
        Список елементів.
    """

    return await crud.get_items(
        session=session,
        skip=skip,
        limit=limit,
        owner_id=owner_id,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)) -> ItemRead:
    """Повертає елемент за його ідентифікатором.

    Args:
        item_id: Ідентифікатор елемента.
        session: Асинхронна сесія бази даних.

    Returns:
        Знайдений елемент.
    """

    item = await crud.get_item(session, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item_endpoint(
        item_id: int,
        item_update: ItemUpdate,
        owner_id: int,
        session: AsyncSession = Depends(get_session)
) -> ItemRead:
    """Оновлює елемент, якщо користувач є його власником.

    Args:
        item_id: Ідентифікатор елемента.
        item_update: Дані для оновлення елемента.
        owner_id: Ідентифікатор власника елемента.
        session: Асинхронна сесія бази даних.

    Returns:
        Оновлений елемент.
    """

    item = await crud.update_item(session, item_id, item_update, owner_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if item is False:
        raise HTTPException(status_code=403, detail="Only owner can update this item")

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_endpoint(
        item_id: int,
        owner_id: int,
        session: AsyncSession = Depends(get_session)
) -> None:
    """Видаляє елемент, якщо користувач є його власником.

    Args:
        item_id: Ідентифікатор елемента.
        owner_id: Ідентифікатор власника елемента.
        session: Асинхронна сесія бази даних.

    Returns:
        None.
    """

    success = await crud.delete_item(session, item_id, owner_id)

    if success is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if not success:
        raise HTTPException(status_code=403, detail="Only owner can delete this item")

    return None
