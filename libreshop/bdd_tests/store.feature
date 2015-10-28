Feature: store
  As an anonymous user
  I want to learn more about libreshop
  So that I can use their services in the future

  Scenario: visit the home page
     Given I am an anonymous user
      When I visit the home page
      Then I will see the text "LibreShop"

  Scenario: visit the home page
     Given I am an anonymous user
      When I visit the home page
      Then I will see a "shopping cart" icon