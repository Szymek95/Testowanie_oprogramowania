from datetime import datetime
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

landing_page = "http://localhost:8000/"

@fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    # Rozdzielczosc
    # Tryb incognito
    # FullScreen (maximized)
    # Headless mode
    print(driver)
    # driver = webdriver.Firefox()
    # driver = webdriver.Safari()
    # driver = webdriver.Edge()
    # driver = webdriver.Ie()
    # driver.get("http://localhost:8000/")

    driver.get(landing_page)
    yield driver
    driver.quit()

def test_check_title(driver):
    """
    Documentation
    """
    assert driver.title == "Employee Manager"

def test_check_that_elements_exists(driver):
    """
    Documention
    """
    # driver.find_element     # zwraca pojedynczy element
    # driver.find_elements    # zwraca listę elementów
    name = driver.find_element(By.ID, "name")
    assert name is not None

    name_selector = driver.find_element(By.CSS_SELECTOR, "#name")
    assert name_selector is not None

    add_button = driver.find_element(By.CLASS_NAME, "btn-add")
    assert add_button is not None

    select_tag = driver.find_element(By.TAG_NAME, "select")
    assert select_tag is not None

    codebrainers_link = driver.find_element(By.LINK_TEXT, "CodeBrainers")
    assert codebrainers_link is not None

    codebrainers_p_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Brainers")
    assert codebrainers_p_link is not None

    xpath_example = driver.find_element(By.XPATH, '//*[@id="on_leave"]')
    assert codebrainers_p_link is not None

    # By.ID: Locate by element ID.
    # By.NAME: Locate by the name attribute.
    # By.XPATH: Locate by an XPath expression.
    # By.CSS_SELECTOR: Locate by a CSS selector.
    # By.CLASS_NAME: Locate by the class attribute.
    # By.TAG_NAME: Locate by the tag name (e.g., "input", "button").
    # By.LINK_TEXT: Locate a link element by its exact text.
    # By.PARTIAL_LINK_TEXT: Locate a link element by partial text match.
    # RelativeBy: Locate elements relative to a specified root element.

    # assert driver.find_element(By.ID, "submitBtn") is not None

def test_validate_name_field(driver):
    # id="name"
    # id="submitBtn"
    # id="errorBox"

    error_text = "name: String should match pattern"
    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys("Test@123")
    assert name_field.get_attribute("value") == "Test@123"

    add_button = driver.find_element(By.ID, "submitBtn")
    add_button.click()

    error_box = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.ID, "errorBox")
            )
        )
    screenshot_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_error.png"
    driver.save_screenshot(screenshot_path)
    assert error_box.get_attribute("textContent") is not None

    # implicit - czeka zawsze zalozony czas! nie wazne ze element zostanie znaleziony szybciej
    # explicit - czeka az element zostanie znaleziony i zatrzymuje ten wait po jego znalezieniu!

def test_create_employee(driver):
    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys("Jan Kowalski")

    # driver.find_element(By.ID, "name").send_keys("Jan Kowalski")

    salary_field = driver.find_element(By.ID, "salary")
    salary_field.send_keys("10000")

    age_field = driver.find_element(By.ID, "age")
    age_field.send_keys("30")

    position_dropdown = driver.find_element(By.ID, "position")
    Select(position_dropdown).select_by_value("Senior QA")

    vacation_checkbox = driver.find_element(By.ID, "on_leave")
    vacation_checkbox.click()
    assert vacation_checkbox.is_selected() == True

    add_button = driver.find_element(By.ID, "submitBtn")
    add_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "employees"),
            "Jan Kowalski"
        )
    )

    assert "Jan Kowalski" in driver.page_source

    screenshot_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_error.png"
    driver.save_screenshot(screenshot_path)

    # uzupelnijcie pola
    # name
    # salary
    # age
    # position
    # nacisnij przycisk add
    # zrob zrzut ekranu aby potwierdzic ze pracownik zostal dodany

    # Select(driver.find_element(By.ID, "position")).select_by_index()
    # Select(driver.find_element(By.ID, "position")).select_by_value("QA Lead")
    # Select(driver.find_element(By.ID, "position")).select_by_visible_text


def test_edit_employee(driver):
    elements = driver.find_elements(By.CLASS_NAME, "btn-edit")
    first_edit_button = elements[0]
    first_edit_button.click()

    name_field = driver.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys("John Kowalski")
    assert name_field.get_attribute("value") == "John Kowalski"

    update_button = driver.find_elements(By.CLASS_NAME, "btn-update")
    update_button[0].click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "employees"),
            "John Kowalski"
        )
    )

    assert "John Kowalski" in driver.page_source
    screenshot_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_error.png"
    driver.save_screenshot(screenshot_path)

def test_check_table(driver):
    # zidentyfikummy tabele (wiersze)
    employee_table = driver.find_element(By.ID, "employees")
    assert employee_table.is_displayed()

    rows = driver.find_elements(By.CSS_SELECTOR, "#employees tr")
    assert rows[0].is_displayed()

    name_cell = driver.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
    assert name_cell.text == "John Kowalski"

    # name_cell = driver.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
    # 3 - Salary
    # 4 - Age
    # 5 - Position

    # Dodac tutaj walidacje kolejnych wartosci

def test_delete_employee(driver):
    delete_button = driver.find_element(By.CLASS_NAME, "btn-delete")
    delete_button.click()

    name_cell = driver.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
    assert name_cell.is_displayed == False






    # table - table
    # tr - table row
    # th - table header
    # td - table komórka (cell)

    from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from configuration import driver

class EmployeePage:
    NAME = (By.ID, "name")
    SALARY = (By.ID, "salary")
    AGE = (By.ID, "age")
    POSITION = (By.ID, "position")
    VACATION = (By.ID, "on_leave")
    ADD_BUTTON = (By.ID, "submitBtn")

    def __init__(self, driver):
        self.driver = driver

    def input_name(self, name):
        self.driver.find_element(*self.NAME).send_keys(name)

    def input_salary(self, salary):
        self.driver.find_element(*self.SALARY).send_keys(salary)

    def input_age(self, age):
        self.driver.find_element(*self.AGE).send_keys(age)

    def select_position(self, position):
        Select(self.driver.find_element(*self.POSITION)).select_by_value(position)

    def click_add_button(self):
        self.driver.find_element(*self.ADD_BUTTON).click()