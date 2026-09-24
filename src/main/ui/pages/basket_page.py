from playwright.sync_api import Page
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_information_page import CheckoutInformationPage

class BasketPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.continue_shopping_button = page.get_by_role("button", name="Continue Shopping")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def remove_item(self, product_name:str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.get_by_role("button", name="Remove")
        button.click()
        return card

    def checkout(self):
        self.checkout_button.click()
        return CheckoutInformationPage(self.page)

    def continue_shopping(self):
        self.continue_shopping_button.click()
        return CatalogPage(self.page)

    def get_item_prices(self) -> list[float]:
        prices = self.item_prices.all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

