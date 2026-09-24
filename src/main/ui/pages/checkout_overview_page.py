from playwright.sync_api import Page
from src.main.ui.pages.checkout_complete_page import CheckoutCompletePage

class CheckoutOverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.cancel_button = page.locator('[data-test="cancel"]')

    def get_subtotal(self) -> float:
        subtotal = self.subtotal_label.text_content()
        return float(subtotal.split("$")[1])

    def get_tax(self) -> float:
        tax = self.tax_label.text_content()
        return float(tax.split("$")[1])

    def get_total(self) -> float:
        total = self.total_label.text_content()
        return float(total.split("$")[1])

    def finish(self):
        self.finish_button.click()
        return CheckoutCompletePage(self.page)