from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar


DataT = TypeVar('DataT')


# MENU SCHEMAS
class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str
    description: str


class Menu(MenuBase):
    id: str
    submenus_count: int | None = None
    dishes_count: int | None = None

    class Config:
        orm_mode = True


# SUBMENU SCHEMAS
class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    title: str
    description: str


class SubMenu(SubMenuBase):
    id: str
    dishes_count: int | None = None

    class Config:
        orm_mode = True


# DISH SCHEMAS
class DishBase(BaseModel):
    title: str
    description: str
    price: str | None = None


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    title: str
    description: str
    price: str | None = None


class Dish(DishBase):
    id: str

    class Config:
        orm_mode = True


class Response(GenericModel, Generic[DataT]):
    status: str
    message: str
