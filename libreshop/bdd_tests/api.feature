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
      Then I get an empty list

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
       And The response will contain an error description

  Scenario: register a new user without a CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I create a new "User"
      Then I will receive a "400 BAD REQUEST" response
       And The response will contain an error description

  Scenario: register a new user with a failed CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I fail the CAPTCHA
       And I create a new "User"
      Then I will receive a "400 BAD REQUEST" response
       And The response will contain an error description

  Scenario: register a new user with a solved CAPTCHA
     Given I am an anonymous user
      When I query the "Token" API
       And I get a Registration Token
       And I solve the CAPTCHA
       And I create a new "User"
      Then I will receive a "201 CREATED" response
       And The response will contain my username

  Scenario: update a user as an anonymous user
     Given I am an anonymous user
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "404 NOT FOUND" response

  Scenario: update a user as a regular user
     Given I am a regular user
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And The "email" field will equal "test@test.com"

  Scenario: update a user as a staff member
     Given I am a staff member
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And The "email" field will equal "test@test.com"

  Scenario: update a user as an admin
     Given I am an admin
      When I update the "email" field on a "User" object to "test@test.com"
      Then I will receive a "200 OK" response
       And The "email" field will equal "test@test.com"
