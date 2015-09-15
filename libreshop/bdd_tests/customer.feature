Feature: customer
  As a new customer
  I want to create an account
  So that I can order products and services

  Scenario: access the user registration page
     Given I am a new user
      When I visit the user registration page
      Then I will see "LibreShop | User Registration" in the browser title

  Scenario: create an account
     Given I am a new User
      When I visit the user registration page
       And I enter "new_user" in the "Username" field
       And I enter "test1234" in the "Password" field
       And I enter "test1234" in the "Password confirmation" field
       And I enter "1234" in the "Captcha" field
       And I click the "Submit" button
      Then I will see a link labeled "Log Out new_user"
