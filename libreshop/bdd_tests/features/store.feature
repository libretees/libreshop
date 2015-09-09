Feature: store
  As a new user
  I want to learn more about libreshop
  So that I can use their services in the future

  Scenario: visit the home page
     Given I am a new user
      When I visit the home page
      Then I will see the text "LibreShop"
