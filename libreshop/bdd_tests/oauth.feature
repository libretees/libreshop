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
       And I will navigate to the "Facebook" app settings page
       And I will remove the "LibreShop" app

  Scenario: log in with GitHub
     Given I am an anonymous user
      When I visit the user registration page
       And I click the "Log in with GitHub" link
       And I enter "My GitHub Username" in the "Username or email address" field
       And I enter "My GitHub Password" in the "Password" field
       And I click the "Sign in" button
       And I click the "Authorize application" button
      Then I will see "LibreShop | User Registration" in the browser title
       And I will navigate to the "GitHub" app settings page
       And I will remove the "LibreShop" app

  Scenario: log in with Twitter
     Given I am an anonymous user
      When I visit the user registration page
       And I click the "Log in with Twitter" link
       And I enter "My Twitter Username" in the "Username or email" field
       And I enter "My Twitter Password" in the "Password" field
       And I click the "Sign In" button
      Then I will see "LibreShop | User Registration" in the browser title
       And I will navigate to the "Twitter" app settings page
       And I will remove the "LibreShop" app

  Scenario: log in with Reddit
     Given I am an anonymous user
      When I visit the user registration page
       And I click the "Log in with Reddit" link
       And I enter "My Reddit Username" in the "username" field
       And I enter "My Reddit Password" in the "password" field
       And I click the "log in" button
       And I click the "Allow" button
      Then I will see "LibreShop | User Registration" in the browser title
       And I will navigate to the "Reddit" app settings page
       And I will remove the "LibreShop" app
