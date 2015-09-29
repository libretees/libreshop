Feature: oauth
  As a user
  I want to log in using OAuth
  So that I can save time

  Scenario: log in with Facebook
     Given I am an anonymous user
      When I visit the user registration page
       And I click the "Log in with Facebook" link
       And I enter "My Facebook Username" in the "Email or Phone" field
       And I enter "My Facebook Password" in the "Password" field
       And I click the "Log In" button
       And I click the "Okay" button to authorize the app
      Then I will see "LibreShop | User Registration" in the browser title
