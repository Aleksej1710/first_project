from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_auth_standard_user(page):
    LoginSteps(page).open_login_page().login("standard_user", "secret_sauce")
    CatalogSteps(page).check_catalog_opened()

def test_auth_locked_out_user(page):
    (LoginSteps(page)
        .open_login_page()
        .login("locked_out_user", "secret_sauce")
        .check_login_page_opened()
        .check_error("Epic sadface: Sorry, this user has been locked out."))

def test_logout_standard_user(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    CatalogSteps(page).check_catalog_opened().logout()
    login_steps.check_login_page_opened()

def test_logout_visual_user(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("visual_user", "secret_sauce")
    CatalogSteps(page).check_catalog_opened().logout()
    login_steps.check_login_page_opened()

