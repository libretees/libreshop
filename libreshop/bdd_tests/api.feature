@api
Feature: api
  As a user
  I want to query the website via an API
  So that I can integrate with its products and services

  Scenario: get a list of users as an admin
     Given I am an admin
      When I query the "Users" API
      Then I get a list of all Users

  Scenario: get a list of users as a staff member
     Given I am a staff member
      When I query the "Users" API
      Then I get a list of all Users

  Scenario: get a list of users as a regular user
     Given I am a regular user
      When I query the "Users" API
      Then I get a list containing my User

  Scenario: get a list of users as an anonymous user
     Given I am an anonymous user
      When I query the "Users" API
      Then I will receive a "403 FORBIDDEN" response
       And the response will contain an authentication error

  Scenario: get a registration token as an admin
     Given I am an admin
      When I query the "Token" API
      Then I get a Registration Token

  Scenario: get a registration token as a regular user
     Given I am a regular user
      When I query the "Token" API
      Then I get a Registration Token

  Scenario: get a registration token as an anonymous user
     Given I am an anonymous user
      When I query the "Token" API
      Then I get a Registration Token

  Scenario: register a new user without a token
     Given I am an anonymous user
      When I create a new "User"
      Then I will receive a "400 BAD REQUEST" response
       And the response will contain an error description

  Scenario: register a new user without a CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I create a new "User"
      Then I will receive a "400 BAD REQUEST" response
       And the response will contain an error description

  Scenario: register a new user with a failed CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I fail the CAPTCHA
       And I create a new "User"
      Then I will receive a "400 BAD REQUEST" response
       And the response will contain an error description

  Scenario: register a new user with a solved CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I solve the CAPTCHA
       And I create a new "User"
      Then I will receive a "201 CREATED" response
       And the response will contain my username

  Scenario: register a new user with a solved CAPTCHA and email address
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I solve the CAPTCHA
       And I provide an email address of "user@test.com"
       And I create a new "User"
      Then I will receive a "201 CREATED" response
       And the response will contain my username
       And I will receive an email with the subject "Welcome to LibreShop!"

  Scenario: update someone else's email as an anonymous user
     Given I am an anonymous user
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "403 FORBIDDEN" response
       And the response will contain an authentication error

  Scenario: update my email as a regular user
     Given I am a regular user
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And the "email" field will equal "test@test.com"

  Scenario: update my email as a staff member
     Given I am a staff member
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And the "email" field will equal "test@test.com"

  Scenario: update my email as an admin
     Given I am an admin
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And the "email" field will equal "test@test.com"

  Scenario: update someone else's password as an anonymous user
     Given I am an anonymous user
      When I update the "password" field on a "User" object to "test"
      Then I will receive a "403 FORBIDDEN" response
       And the response will contain an authentication error

  Scenario: update my password as a regular user
     Given I am a regular user
      When I update the "password" field on a "User" object to "test"
      Then I will receive a "200 OK" response
       And the "password" field will equal "test"

  Scenario: update my password as a staff member
     Given I am a staff member
      When I update the "password" field on a "User" object to "test"
      Then I will receive a "200 OK" response
       And the "password" field will equal "test"

  Scenario: update my password as an admin
     Given I am an admin
      When I update the "password" field on a "User" object to "test"
      Then I will receive a "200 OK" response
       And the "password" field will equal "test"
