from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps


def test_add_item_and_check_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.check_cart_count(1)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Backpack"])


def test_add_items_and_check_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog.check_cart_count(2)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt"])
    basket.check_cart_count(2)


def test_remove_jacket_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.check_cart_count(1)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Fleece Jacket"])

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.check_cart_count(0)
    basket.expect_items_in_cart([])


def test_remove_items_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    catalog.check_cart_count(2)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Backpack", "Test.allTheThings() T-Shirt (Red)"])

    basket.remove_item("Sauce Labs Backpack")
    basket.check_cart_count(1)
    basket.expect_items_in_cart(["Test.allTheThings() T-Shirt (Red)"])

    basket.remove_item("Test.allTheThings() T-Shirt (Red)")
    basket.check_cart_count(0)
    basket.expect_items_in_cart([])


def test_full_e2e(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog.check_cart_count(2)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt"])
    basket.check_cart_count(2)
    basket_total = basket.get_items_total_price()

    basket.checkout()
    checkout.check_information_opened()
    checkout.start_checkout("Алексей", "Ковалев", "0")
    checkout.check_overview_opened()
    checkout.check_subtotal(basket_total)
    checkout.check_total()

    checkout.finish_checkout()
    checkout.check_complete_opened()
    checkout.check_pdf_downloaded()


def test_checkout_without_postal_code(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.check_cart_count(1)

    catalog.open_cart()
    basket.check_basket_opened()
    basket.expect_items_in_cart(["Sauce Labs Fleece Jacket"])

    basket.checkout()
    checkout.check_information_opened()
    checkout.start_checkout("Алексей", "Ковалев", "")
    checkout.check_error("Error: Postal Code is required")
    checkout.check_information_opened()


def test_download_pdf_order(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page()
    login.login("standard_user", "secret_sauce")
    catalog.check_catalog_opened()

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.open_cart()
    basket.check_basket_opened()

    basket.checkout()
    checkout.start_checkout("Алексей", "Ковалев", "0")
    checkout.check_overview_opened()

    checkout.finish_checkout()
    checkout.check_complete_opened()
    checkout.check_pdf_downloaded()
