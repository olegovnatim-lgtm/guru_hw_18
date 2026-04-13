import allure
from allure_commons.types import Severity
from data.users import User, Gender, Hobbies
from pages.registration_page import RegistrationPage


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "timofeevaao")
@allure.feature("Регистрация пользователя")
@allure.story("Регистрация")
def test_guru_hw_18():
    nastya = User(first_name='Nastya', last_name='Timofeeva', email='testtt@as.ru', gender=Gender.FEMALE,
                  mobile='9857894569', year_of_birth='2020', month_of_birth='4', day_of_birth='18',
                  subject='Maths', hobbies=Hobbies.READING, picture='test_file.pdf', address='Moscow', state='NCR',
                  city='Delhi')
    registration_page = RegistrationPage()

    registration_page.open()
    registration_page.register(nastya)
    registration_page.should_have_registered(nastya)
