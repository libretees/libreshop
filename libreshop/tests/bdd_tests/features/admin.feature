Feature: admin
  As a staff member
  I want to use the admin panel
  So that I can manage the website effectively

  Scenario: visit the admin login page
     Given I am a staff member
      When I visit the admin login page
      Then I will see "Log in | Django site admin" in the browser title

  Scenario: log in to the admin panel
     Given I am a staff member
      When I log in from the admin login page
      Then I will see "Site administration | Django site admin" in the browser title
