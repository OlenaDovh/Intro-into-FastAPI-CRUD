from typing import Optional
from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    """Модель елемента в базі даних.

    Attributes:
        id: Унікальний ідентифікатор елемента.
        title: Назва елемента.
        description: Опис елемента.
        price: Ціна елемента.
        is_active: Ознака активності елемента.
        owner_id: Ідентифікатор власника елемента.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool = True
    owner_id: int


class ItemCreate(SQLModel):
    """Схема для створення нового елемента.

    Attributes:
        title: Назва елемента.
        description: Опис елемента.
        price: Ціна елемента.
        owner_id: Ідентифікатор власника елемента.
    """

    title: str
    description: Optional[str] = None
    price: float
    owner_id: int


class ItemRead(SQLModel):
    """Схема для читання даних елемента.

    Attributes:
        id: Унікальний ідентифікатор елемента.
        title: Назва елемента.
        description: Опис елемента.
        price: Ціна елемента.
        is_active: Ознака активності елемента.
        owner_id: Ідентифікатор власника елемента.
    """

    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool
    owner_id: int


class ItemUpdate(SQLModel):
    """Схема для оновлення існуючого елемента.

    Attributes:
        title: Нова назва елемента.
        description: Новий опис елемента.
        price: Нова ціна елемента.
        is_active: Ознака активності елемента.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None