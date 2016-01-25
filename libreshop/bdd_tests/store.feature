@store
Feature: store
  As an anonymous user
  I want to learn more about libreshop
  So that I can use their services in the future

  Scenario: visit the home page
     Given I am an anonymous user
      When I visit the "home" page
      Then I will see the text "LibreShop"

  Scenario: add an item to cart
     Given I am an anonymous user
      When I visit the "home" page
       And I click the "Get One!" button
       And I select "Small" from the "Size" field
       And I select "White" from the "Color" field
       And I click the "Get One!" button
      Then I will see a "shopping cart" icon
       And I will see the text "Your cart contains"


  Scenario: remove an item from the cart
     Given I am an anonymous user
      When I visit the "home" page
       And I click the "Get One!" button
       And I select "Small" from the "Size" field
       And I select "White" from the "Color" field
       And I click the "Get One!" button
       And I click the x button next to "foo (White Small)"
      Then I will not see the text "Your cart contains"
