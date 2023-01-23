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


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_menu_create(test_db):
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    assert response.status_code == 201


def test_menu_get(test_db):
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    response_get = client.get(url_menu + '/1')
    assert response_get.json()['description'] == "Test menu"
    assert response_get.status_code == 200


def test_menu_patch(test_db):
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    edit_data = {"title": "Test2", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    response_get = client.get(url_menu+'/1')
    response_patch = client.patch(url_menu+'/1', json=edit_data)
    response_get_second = client.get(url_menu + '/1')
    assert response_get.json()['title'] == "Test1"
    assert response_patch.status_code == 200
    assert response_get_second.json()['title'] == "Test2"


def test_menu_delete(test_db):
    url_menu = '/api/v1/menus'
    data = {"title": "Test1", "description": "Test menu"}
    response = client.post(url_menu, json=data)
    response_delete = client.delete(url_menu + '/1')
    assert response_delete.json()['status'] == "true"


def test_menus_get(test_db):
    url_menu = '/api/v1/menus/'
    response = client.get(url_menu)
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_create(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    assert response_submenu.status_code == 201


def test_submenu_get(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_get_menu = client.get(url_menu+'/1')
    response_get_submenu = client.get(url_submenu+'/1')
    assert response_get_submenu.json()['description'] == "Test submenu"
    assert response_get_submenu.status_code == 200
    assert response_get_menu.json()["submenus_count"] == 1


def test_submenu_patch(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    edit_data = {"title": "SubTest2", "description": "Test submenu"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_get = client.get(url_submenu+'/1')
    response_patch = client.patch(url_submenu+'/1', json=edit_data)
    response_get_second = client.get(url_submenu + '/1')
    assert response_get.json()['title'] == "SubTest1"
    assert response_patch.status_code == 200
    assert response_get_second.json()['title'] == "SubTest2"


def test_submenu_delete(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_delete = client.delete(url_submenu + '/1')
    assert response_delete.json()['status'] == "true"


def test_dish_create(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_dish = client.post(url_dish, json=dish_data)
    assert response_dish.status_code == 201


def test_dish_get(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_dish = client.post(url_dish, json=dish_data)
    response_get_menu = client.get(url_menu+'/1')
    response_get_submenu = client.get(url_submenu+'/1')
    response_get_dish = client.get(url_dish + '/1')
    assert response_get_dish.json()['description'] == "Test dish"
    assert response_get_dish.status_code == 200
    assert response_get_menu.json()["submenus_count"] == 1
    assert response_get_submenu.json()["dishes_count"] == 1


def test_dish_patch(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    edit_data = {"title": "DishTest2", "description": "Test dish", "price": "10.12"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_dish = client.post(url_dish, json=dish_data)
    response_get = client.get(url_dish+'/1')
    response_patch = client.patch(url_dish+'/1', json=edit_data)
    response_get_second = client.get(url_dish + '/1')
    assert response_get.json()['title'] == "DishTest1"
    assert response_patch.status_code == 200
    assert response_get_second.json()['title'] == "DishTest2"


def test_dish_delete(test_db):
    url_menu = '/api/v1/menus'
    url_submenu = '/api/v1/menus/1/submenus'
    url_dish = '/api/v1/menus/1/submenus/1/dishes'
    menu_data = {"title": "Test1", "description": "Test menu"}
    submenu_data = {"title": "SubTest1", "description": "Test submenu"}
    dish_data = {"title": "DishTest1", "description": "Test dish", "price": "10.12"}
    response = client.post(url_menu, json=menu_data)
    response_submenu = client.post(url_submenu, json=submenu_data)
    response_dish = client.post(url_dish, json=dish_data)
    response_delete = client.delete(url_dish + '/1')
    assert response_delete.json()['status'] == "true"
