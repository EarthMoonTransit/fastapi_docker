from sqlalchemy import Column, ForeignKey, Integer, String, select, func, and_
from sqlalchemy.orm import relationship, column_property
from database import Base


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(String)

    submenu_id = Column(Integer, ForeignKey('submenus.id'))


class SubMenu(Base):
    __tablename__ = "submenus"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    menu_id = Column(Integer, ForeignKey('menus.id'))

    dishes = relationship('Dish', cascade="all, delete")
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id==id).correlate_except(Dish).scalar_subquery()
    )


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    submenus = relationship('SubMenu', cascade="all, delete")
    submenus_count = column_property(
        select(func.count(SubMenu.id)).where(SubMenu.menu_id==id).correlate_except(SubMenu).scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(and_(SubMenu.id==Dish.submenu_id, SubMenu.menu_id==id)).correlate_except(Dish).scalar_subquery()
    )
