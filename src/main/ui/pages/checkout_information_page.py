from playwright.sync_api import Page
from src.main.ui.pages.checkout_overview_page import CheckoutOverviewPage

class CheckoutInformationPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.get_by_role('button', name="Cancel")
        self.error_message = page.locator('[data-test="error"]')

    def fill_form(self, first_name:str, last_name:str, postal_code:str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def submit(self):
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)