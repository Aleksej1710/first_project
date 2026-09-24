from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    CatalogSteps(page).check_catalog_opened()


def test_sorted_by_name(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("za")      # уводим с дефолтной сортировки, иначе az проверяется "бесплатно"
        .sort_items("az")
        .check_names_sorted())


def test_sorted_by_name_za(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("za")
        .check_names_sorted(reverse=True))


def test_sort_by_price(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("lohi")
        .check_prices_sorted()
        .sort_items("hilo")
        .check_prices_sorted(reverse=True))


def test_add_to_cart(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Sauce Labs Bike Light")
        .check_cart_count(1))


def test_add_and_remove_onesie(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Sauce Labs Onesie")
        .check_cart_count(1)
        .remove_from_cart("Sauce Labs Onesie")
        .check_cart_count(0))


def test_product_details_onesie(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .check_product_details("Sauce Labs Onesie"))


def test_product_details_jacket(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .check_product_details("Sauce Labs Fleece Jacket"))


def test_remove_item_from_catalog(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Test.allTheThings() T-Shirt (Red)")
        .check_cart_count(1)
        .remove_from_cart("Test.allTheThings() T-Shirt (Red)")
        .check_cart_count(0))
