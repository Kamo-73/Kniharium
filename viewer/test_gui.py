import time
from unittest import skip

from django.contrib.auth.models import User
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class GuiTestWithSelenium(TestCase):
    @skip
    def test_home_page_firefox(self):
        driver = webdriver.Firefox()
        driver.get('http://127.0.0.1:8000')
        assert 'Knihy' in driver.page_source

    @skip
    def test_home_page_chrome(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000')
        assert 'Autoři' in driver.page_source

    def test_signup(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:8000/accounts/signup/")
        time.sleep(2)
        username_field = driver.find_element(By.ID, "id_username")
        username_field.send_keys("TestUser")
        time.sleep(2)
        first_name_field = driver.find_element(By.ID, "id_first_name")
        first_name_field.send_keys("TestFirstName")
        time.sleep(2)
        last_name_field = driver.find_element(By.ID, "id_last_name")
        last_name_field.send_keys("TestLastName")
        time.sleep(2)
        email_field = driver.find_element(By.ID, "id_email")
        email_field.send_keys("test@test.cz")
        time.sleep(2)
        password1_field = driver.find_element(By.ID, "id_password1")
        password1_field.send_keys("TestPassword1!")
        time.sleep(2)
        password2_field = driver.find_element(By.ID, "id_password2")
        password2_field.send_keys("TestPassword1!")
        time.sleep(2)
        date_of_birth_field = driver.find_element(By.ID, "id_date_of_birth")
        date_of_birth_field.send_keys("2001-01-01")
        time.sleep(2)
        biography_field = driver.find_element(By.ID, "id_biography")
        biography_field.send_keys("TestBiography.")
        time.sleep(2)
        phone_field = driver.find_element(By.ID, "id_phone")
        phone_field.send_keys("666666666")
        time.sleep(2)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.send_keys(Keys.RETURN)
        time.sleep(2)



        #self.assertTrue(
            #User.objects.filter(username="TestUserName").exists(),
            #"Uživatel nebyl vytvořen v databázi."
        #)

        #driver.quit()









