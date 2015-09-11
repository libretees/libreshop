Feature: admin
  As a staff member
  I want to use the admin panel
  So that I can manage the website effectively

  Scenario: access the admin login page
     Given I am a staff member
      When I visit the admin login page
      Then I will see "Log in | Django site admin" in the browser title

  Scenario: log in to the admin panel
     Given I am a staff member
      When I visit the admin login page
       And I log in to the site admin page
      Then I will see "Site administration | Django site admin" in the browser title

  Scenario: add a user via the admin panel
     Given I am a staff member
      When I visit the admin login page
       And I log in to the site admin page
       And I click the "Users" link
       And I click the "Add user" link
       And I add a user named "new_user"
      Then I will see a link for "new_user"

  Scenario: add a product via the admin panel
     Given I am a staff member
      When I visit the admin login page
       And I log in to the site admin page
       And I click the "Products" link
       And I click the "Add product" link
       And I add a product called "new_product"
      Then I will see a link for "new_product"
