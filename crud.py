from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from models import Menu, SubMenu, Dish
from schemas import MenuCreate, MenuUpdate, SubMenuCreate,\
    SubMenuUpdate, DishCreate, DishUpdate


# MENUS
def get_menus(db: Session):
    return db.query(Menu).all()


def get_menu(db: Session, api_test_menu_id: str):
    menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
    if menu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'menu not found'})
    return menu


def create_menu(db: Session, menu: MenuCreate):
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu: MenuUpdate, api_test_menu_id: str):
    updated_menu = get_menu(db=db, api_test_menu_id=api_test_menu_id)
    if updated_menu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'menu not found'})
    updated_menu.title = menu.title
    updated_menu.description = menu.description
    db.commit()
    db.refresh(updated_menu)
    return updated_menu


def delete_menu(db: Session, api_test_menu_id: str):
    menu = get_menu(db=db, api_test_menu_id=api_test_menu_id)
    if menu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'menu not found'})
    db.delete(menu)
    db.commit()


# SUBMENUS
def get_submenus(db: Session, api_test_menu_id: str):
    return db.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id).all()


def get_submenu(db: Session, api_test_submenu_id: str):
    submenu = db.query(SubMenu).filter(SubMenu.id == api_test_submenu_id).first()
    if submenu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'submenu not found'})
    return submenu


def create_submenu(db: Session, submenu: SubMenuCreate, api_test_menu_id: str):
    current_submenu = submenu.title
    check_submenu = db.query(SubMenu).filter(SubMenu.title == current_submenu).count()
    if check_submenu > 0:
        return JSONResponse(status_code=400, content='already exist')
    db_submenu = SubMenu(**submenu.dict(), menu_id=api_test_menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, submenu: SubMenuUpdate, api_test_submenu_id: str):
    updated_submenu = get_submenu(db=db, api_test_submenu_id=api_test_submenu_id)
    if updated_submenu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'submenu not found'})
    updated_submenu.title = submenu.title
    updated_submenu.description = submenu.description
    db.commit()
    db.refresh(updated_submenu)
    return updated_submenu


def delete_submenu(db: Session, api_test_submenu_id: str):
    submenu = get_submenu(db=db, api_test_submenu_id=api_test_submenu_id)
    if submenu is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'submenu not found'})
    db.delete(submenu)
    db.commit()


# DISH
def get_dishes(db: Session, api_test_submenu_id: str):
    return db.query(Dish).filter(Dish.submenu_id == api_test_submenu_id).all()


def get_dish(db: Session, api_test_dish_id: str):
    dish = db.query(Dish).filter(Dish.id == api_test_dish_id).first()
    if dish is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'dish not found'})
    return dish


def create_dish(db: Session, dish: DishCreate, api_test_submenu_id: str):
    current_dish = dish.title
    check_dish = db.query(Dish).filter(Dish.title == current_dish).count()
    if check_dish > 0:
        return JSONResponse(status_code=400, content='already exist')
    db_dish = Dish(**dish.dict(), submenu_id=api_test_submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish: DishUpdate, api_test_dish_id: str):
    updated_dish = get_dish(db=db, api_test_dish_id=api_test_dish_id)
    if updated_dish is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'dish not found'})
    updated_dish.title = dish.title
    updated_dish.description = dish.description
    updated_dish.price = dish.price
    db.commit()
    db.refresh(updated_dish)
    return updated_dish


def delete_dish(db: Session, api_test_dish_id: str):
    dish = get_dish(db=db, api_test_dish_id=api_test_dish_id)
    if dish is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'dish not found'})
    db.delete(dish)
    db.commit()
