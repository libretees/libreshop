Feature: storefront
  As a new user
  I want to learn more about libreshop
  So that I can use their services in the future

  Scenario: visit the home page
     Given I am a new user
      when I visit the home page
      then I will see the text "LibreShop Homepage"
