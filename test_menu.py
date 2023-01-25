from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from main import app, get_db
from database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()




app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_menus_get():
    url_menu = '/api/v1/menus/'
    response = client.get(url_menu)
    assert response.status_code == 200
    assert response.json() == []


def test_menu_create():
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    assert response.status_code == 201
    assert response.json() == {
          "title": "Test1",
          "description": "Test menu",
          "id": "1",
          "submenus_count": 0,
          "dishes_count": 0
        }


def test_menu_get():
    url_menu = '/api/v1/menus'
    response = client.get(url_menu + '/1')
    assert response.status_code == 200
    assert response.json() == {
          "title": "Test1",
          "description": "Test menu",
          "id": "1",
          "submenus_count": 0,
          "dishes_count": 0
        }


def test_menu_patch():
    url_menu = '/api/v1/menus'
    edit_data = {"title": "Test2", "description": "Test menu"}
    response = client.patch(url_menu+'/1', json=edit_data)
    assert response.status_code == 200
    assert response.json() == {
          "title": "Test2",
          "description": "Test menu",
          "id": "1",
          "submenus_count": 0,
          "dishes_count": 0
        }


def test_menu_delete():
    url_menu = '/api/v1/menus/1'
    response = client.delete(url_menu)
    assert response.json()['status'] == "true"


def test_menu_get_not_found():
    url_menu = '/api/v1/menus/0'
    response = client.get(url_menu)
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"


def test_menu2_create():
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    assert response.status_code == 201
    assert response.json() == {
          "title": "Test1",
          "description": "Test menu",
          "id": "1",
          "submenus_count": 0,
          "dishes_count": 0
        }


def test_submenus_get():
    url_menu = '/api/v1/menus/1/submenus'
    response = client.get(url_menu)
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_create():
    url_submenu = '/api/v1/menus/1/submenus'
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    response_submenu = client.post(url_submenu, json=submenu_data)
    assert response_submenu.status_code == 201
    assert response_submenu.json() == {
            "title": "SubTest1",
            "description": "Test submenu",
            "id": "1",
            "dishes_count": 0
        }


def test_submenu_get():
    url_submenu = '/api/v1/menus/1/submenus'
    response = client.get(url_submenu+'/1')
    assert response.json() == {
            "title": "SubTest1",
            "description": "Test submenu",
            "id": "1",
            "dishes_count": 0
        }


def test_submenu_patch():
    url_submenu = '/api/v1/menus/1/submenus'
    edit_data = {"title": "SubTest2", "description": "Test submenu"}
    response = client.patch(url_submenu+'/1', json=edit_data)
    assert response.status_code == 200
    assert response.json() == {
            "title": "SubTest2",
            "description": "Test submenu",
            "id": "1",
            "dishes_count": 0
        }


def test_submenu_delete():
    url_submenu = '/api/v1/menus/1/submenus'
    response_delete = client.delete(url_submenu+'/1')
    assert response_delete.json()['status'] == "true"


def test_submenu_get_not_found():
    url_submenu = '/api/v1/menus/1/submenus/0'
    response = client.get(url_submenu)
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


def test_submenu2_create():
    url_submenu = '/api/v1/menus/1/submenus'
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    response_submenu = client.post(url_submenu, json=submenu_data)
    assert response_submenu.status_code == 201
    assert response_submenu.json() == {
            "title": "SubTest1",
            "description": "Test submenu",
            "id": "1",
            "dishes_count": 0
        }


def test_dishes_get():
    url_menu = '/api/v1/menus/1/submenus/1/dishes'
    response = client.get(url_menu)
    assert response.status_code == 200
    assert response.json() == []


def test_dish_create():
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    response_dish = client.post(url_dish, json=dish_data)
    assert response_dish.status_code == 201
    assert response_dish.json() == {
          "title": "DishTest1",
          "description": "Test dish",
          "price": "10.12",
          "id": "1"
        }


def test_dish_get():
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    response = client.get(url_dish + '/1')
    assert response.status_code == 200
    assert response.json() == {
          "title": "DishTest1",
          "description": "Test dish",
          "price": "10.12",
          "id": "1"
        }


def test_dish_patch():
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    edit_data = {"title": "DishTest2", "description": "Test dish", "price": "10.12"}
    response = client.patch(url_dish+'/1', json=edit_data)
    assert response.status_code == 200
    assert response.json() == {
          "title": "DishTest2",
          "description": "Test dish",
          "price": "10.12",
          "id": "1"
        }


def test_dish_delete():
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    response = client.delete(url_dish + '/1')
    assert response.json()['status'] == "true"


def test_dish_get_not_found():
    url_dish = '/api/v1/menus/1/submenus/1/dishes/0'
    response = client.get(url_dish)
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


def test_dish2_create():
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    response_dish = client.post(url_dish, json=dish_data)
    assert response_dish.status_code == 201
    assert response_dish.json() == {
          "title": "DishTest1",
          "description": "Test dish",
          "price": "10.12",
          "id": "1"
        }


def test_menu_count():
    url_menu = '/api/v1/menus'
    response = client.get(url_menu + '/1')
    assert response.status_code == 200
    assert response.json() == {
        "title": "Test1",
        "description": "Test menu",
        "id": "1",
        "submenus_count": 1,
        "dishes_count": 1
    }
    Base.metadata.drop_all(bind=engine)

