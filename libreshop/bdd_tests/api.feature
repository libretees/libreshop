Feature: api
  As a user
  I want to query the website via an API
  So that I can integrate with its products and services

  Scenario: get a list of users as an admin
     Given I am an admin
      When I query the Users API
      Then I get a list of Users

  Scenario: get a list of users as a regular user
     Given I am a regular user
      When I query the Users API
      Then I will be presented with an authentication error

  Scenario: get a list of users as an anonymous user
     Given I am an anonymous user
      When I query the Users API
      Then I will be presented with an authentication error
