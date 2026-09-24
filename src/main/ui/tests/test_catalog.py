from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    expect(catalog.product_cards).to_have_count(6)


def test_count_catalog_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    CatalogSteps(page).check_catalog_opened()


def test_sorted_by_name(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    catalog.sort_items('az')
    names = catalog.get_product_names()
    assert names == sorted(names), "Товары не отсортированы по имени A-Z"


def test_sorted_by_name_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("za")      # уводим с дефолтной сортировки, иначе az проверяется "бесплатно"
        .sort_items("az")
        .check_names_sorted())


def test_sorted_by_name_za(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    catalog.sort_items("za")
    names = catalog.get_product_names()
    assert names == sorted((names), reverse=True), "Товары не отсортированы по имени Z-A"


def test_sorted_by_name_za_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("za")
        .check_names_sorted(reverse=True))


def test_sort_by_price(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    catalog.sort_items("lohi")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices())
    catalog.sort_items("hilo")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices(), reverse=True)


def test_sort_by_price_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .sort_items("lohi")
        .check_prices_sorted()
        .sort_items("hilo")
        .check_prices_sorted(reverse=True))


def test_add_to_cart(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    button = catalog.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    expect(catalog.cart_badge).to_have_text("1")


def test_add_to_cart_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Sauce Labs Bike Light")
        .check_cart_count(1))


def test_add_sauce_labs_one(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    button = catalog.add_to_cart("Sauce Labs Onesie")
    expect(button).to_have_text("Remove")
    expect(catalog.cart_badge).to_have_text("1")
    add_button = catalog.remove_from_cart("Sauce Labs Onesie")
    expect(add_button).to_have_text("Add to cart")
    expect(catalog.cart_badge).not_to_be_visible()


def test_add_and_remove_onesie_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Sauce Labs Onesie")
        .check_cart_count(1)
        .remove_from_cart("Sauce Labs Onesie")
        .check_cart_count(0))


def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"


def test_product_details_onesie_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .check_product_details("Sauce Labs Onesie"))


def test_product_details_jacket(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"


def test_product_details_jacket_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .check_product_details("Sauce Labs Fleece Jacket"))


def test_remove_item_from_catalog(auth_page):
    # Кликаем по кнопке Add to cart
    product_card = auth_page.locator(".inventory_item", has_text="Test.allTheThings() T-Shirt (Red)")
    product_button = product_card.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    product_button.click()
    # Проверяем, что кнопка Remove появилась
    remove_button = product_card.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]')
    expect(remove_button).to_be_visible()
    # Удаляем из корзины
    remove_button.click()
    # Проверяем, что кнопка Add to cart вернулась после удаления
    add_button = product_card.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    expect(add_button).to_be_visible()


def test_remove_item_from_catalog_steps(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    (CatalogSteps(page)
        .check_catalog_opened()
        .add_to_cart("Test.allTheThings() T-Shirt (Red)")
        .check_cart_count(1)
        .remove_from_cart("Test.allTheThings() T-Shirt (Red)")
        .check_cart_count(0))


def test_remove_red_from_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    remove_button = catalog.add_to_cart(product_name='Test.allTheThings() T-Shirt (Red)')
    expect(remove_button).to_have_text("Remove")
    add_button = catalog.remove_from_cart(product_name='Test.allTheThings() T-Shirt (Red)')
    expect(add_button).to_have_text("Add to cart")


# test_remove_red_from_catalog_steps не нужен: это тот же сценарий, что test_remove_item_from_catalog_steps.


