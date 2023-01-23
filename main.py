from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/api/v1/menus', response_model=list[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    return crud.get_menus(db)


@app.get('/api/v1/menus/{api_test_menu_id}', response_model=schemas.Menu,
         status_code=status.HTTP_200_OK
         )
def read_menu(
        api_test_menu_id: str, db: Session = Depends(get_db)
):
    return crud.get_menu(db=db, api_test_menu_id=api_test_menu_id)


@app.post('/api/v1/menus', response_model=schemas.Menu,
          status_code=status.HTTP_201_CREATED
          )
def create_menu(
        menu: schemas.MenuCreate, db: Session = Depends(get_db)
):
    return crud.create_menu(db=db, menu=menu)


@app.patch('/api/v1/menus/{api_test_menu_id}', response_model=schemas.Menu)
def update_menu(
        api_test_menu_id: str, menu: schemas.MenuUpdate, db: Session = Depends(get_db)
):
    return crud.update_menu(db=db, menu=menu, api_test_menu_id=api_test_menu_id)


@app.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu(
        api_test_menu_id: str, db: Session = Depends(get_db)
):
    crud.delete_menu(db=db, api_test_menu_id=api_test_menu_id)
    return schemas.Response(status="true", message="The menu has been deleted").dict(exclude_none=True)


# SUBMENU#
@app.get('/api/v1/menus/{api_test_menu_id}/submenus', response_model=list[schemas.SubMenu])
def read_submenus(
        api_test_menu_id: str, db: Session = Depends(get_db)
):
    return crud.get_submenus(db=db, api_test_menu_id=api_test_menu_id)


@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
         response_model=schemas.SubMenu, status_code=status.HTTP_200_OK
         )
def read_submenu(api_test_submenu_id: str, db: Session = Depends(get_db)):
    return crud.get_submenu(db=db, api_test_submenu_id=api_test_submenu_id)


@app.post('/api/v1/menus/{api_test_menu_id}/submenus',
          response_model=schemas.SubMenu, status_code=status.HTTP_201_CREATED
          )
def create_submenu(
        api_test_menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)
):
    return crud.create_submenu(db=db, submenu=submenu, api_test_menu_id=api_test_menu_id)


@app.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
           response_model=schemas.SubMenu
           )
def update_submenu(
        api_test_submenu_id: str, submenu: schemas.SubMenuUpdate, db: Session = Depends(get_db)
):
    return crud.update_submenu(db=db, submenu=submenu, api_test_submenu_id=api_test_submenu_id)


@app.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def delete_menu(
        api_test_submenu_id: str, db: Session = Depends(get_db)
):
    crud.delete_submenu(db=db, api_test_submenu_id=api_test_submenu_id)
    return schemas.Response(status="true", message="The menu has been deleted").dict(exclude_none=True)


# DISH
@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes',
         response_model=list[schemas.Dish]
         )
def read_dishes(api_test_submenu_id: str, db: Session = Depends(get_db)):
    return crud.get_dishes(db=db, api_test_submenu_id=api_test_submenu_id)


@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
         response_model=schemas.Dish, status_code=status.HTTP_200_OK
         )
def read_dish(api_test_dish_id: str, db: Session = Depends(get_db)):
    return crud.get_dish(db=db, api_test_dish_id=api_test_dish_id)


@app.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes',
          response_model=schemas.Dish, status_code=status.HTTP_201_CREATED
          )
def create_dish(api_test_submenu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    return crud.create_dish(db=db, dish=dish, api_test_submenu_id=api_test_submenu_id)


@app.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
           response_model=schemas.Dish)
def update_dish(api_test_dish_id: str, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    return crud.update_dish(db=db, dish=dish, api_test_dish_id=api_test_dish_id)


@app.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def delete_dish(api_test_dish_id: str, db: Session = Depends(get_db)):
    crud.delete_dish(db=db, api_test_dish_id=api_test_dish_id)
    return schemas.Response(status="true", message="The menu has been deleted").dict(exclude_none=True)

