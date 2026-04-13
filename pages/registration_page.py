import allure
from pygments.lexers import resource
from selene import have, command
from selene.support.shared import browser
import utils
from data.users import User


class RegistrationPage:

    @allure.step("Открыть форму регистрации")
    def open(self):
        browser.open('https://demoqa.com/automation-practice-form')
        browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    @allure.step("Заполнить поле 'First Name'")
    def fill_first_name(self, first_name):
        browser.element('#firstName').type(first_name)

    @allure.step("Заполнить поле 'Last Name'")
    def fill_last_name(self, last_name):
        browser.element('#lastName').type(last_name)

    @allure.step("Заполнить поле 'Email'")
    def fill_email(self, email):
        browser.element('#userEmail').type(email)

    @allure.step("Выбрать поле 'Date of Birth'")
    def fill_date_of_birth(self, year, month, day):
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(month)
        browser.element('.react-datepicker__year-select').type(year)
        browser.element(
            f'.react-datepicker__day--0{day}:not(.react-datepicker__day--outside-month)'
        ).click()

    @allure.step("Заполнить радиобаттон 'Gender'")
    def fill_gender(self, gender):
        if gender == "Male":
            browser.element('[for="gender-radio-1"]').click()
        elif gender == "Female":
            browser.element('[for="gender-radio-2"]').click()
        else:
            browser.element('[for="gender-radio-3"]').click()

    @allure.step("Заполнить поле 'Mobile'")
    def fill_mobile(self, mobile):
        browser.element('#userNumber').type(mobile)

    @allure.step("Заполнить поле 'Subjects'")
    def fill_subject(self, subject):
        browser.element('#subjectsInput').type(subject).press_enter()

    @allure.step("Заполнить чекбокс 'Hobbies'")
    def fill_hobbies(self, hobbies):
        if hobbies == "Sports":
            browser.element('[for="hobbies-checkbox-1"]').click()
        elif hobbies == "Reading":
            browser.element('[for="hobbies-checkbox-2"]').click()
        elif hobbies == "Music":
            browser.element('[for="hobbies-checkbox-3"]').click()

    @allure.step("Прикрепить фотографию")
    def upload_picture(self, picture):
        browser.element('#uploadPicture').set_value(utils.path(picture))

    @allure.step("Заполнить поле 'Current Address'")
    def fill_address(self, address):
        browser.element('#currentAddress').type(address)


    @allure.step("Заполнить поле 'State'")
    def fill_state(self, name):
        browser.element('#state').perform(command.js.scroll_into_view)
        browser.element('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text(name)
        ).click()

    @allure.step("Заполнить поле 'City'")
    def fill_city(self, city):
        browser.element('#city').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text(f'{city}')
        ).click()

    @allure.step("Кликнуть на кнопку 'Submit'")
    def click_submit(self):
        browser.element('#submit').click()

    @allure.step("Заполнить форму регистрации")
    def register(self, user: User):
        self.fill_first_name(user.first_name)
        self.fill_last_name(user.last_name)
        self.fill_email(user.email)
        self.fill_gender(user.gender)
        self.fill_mobile(user.mobile)
        self.fill_date_of_birth(user.year_of_birth, user.month_of_birth, user.day_of_birth)
        self.fill_subject(user.subject)
        self.fill_hobbies(user.hobbies)
        self.upload_picture(user.picture)
        self.fill_address(user.address)
        self.fill_state(user.state)
        self.fill_city(user.city)
        self.click_submit()

    @allure.step("Сверить ранее заполненные значения")
    def should_have_registered(self, user: User):
        browser.element('.table').all('td').even.should(
            have.exact_texts(
                user.first_name + ' ' + user.last_name,
                user.email,
                user.gender.value,
                user.mobile,
                utils.format_date(user.year_of_birth, user.month_of_birth, user.day_of_birth),
                user.subject,
                user.hobbies.value,
                user.picture,
                user.address,
                user.state + ' ' + user.city,
            )
        )
