# Feature: customer
#   As a new customer
#   I want to create an account
#   So that I can order products and services

#   Scenario: access the user registration page
#     Given I am an anonymous user
#       When I visit the user registration page
#       Then I will see "LibreShop | User Registration" in the browser title

#   Scenario: create an account with a failed CAPTCHA
#     Given I am an anonymous user
#       When I visit the user registration page
#       And I enter "new_user" in the "Username" field
#       And I enter "test1234" in the "Password" field
#       And I enter "test1234" in the "Password confirmation" field
#       And I enter "4321" in the "Captcha" field
#       And I click the "Submit" button
#       Then I will see the text "captcha"

#   Scenario: create an account with a solved CAPTCHA
#     Given I am an anonymous user
#       When I visit the user registration page
#       And I enter "new_user" in the "Username" field
#       And I enter "test1234" in the "Password" field
#       And I enter "test1234" in the "Password confirmation" field
#       And I enter "1234" in the "Captcha" field
#       And I click the "Submit" button
#       Then I will see a link labeled "Log Out new_user"
