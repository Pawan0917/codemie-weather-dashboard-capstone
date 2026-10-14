Feature: Weather Dashboard

  Background:
    Given the Weather Dashboard is running in mock mode

  Scenario: Search city shows current weather and forecast
    When I search for city "Pune"
    Then I should see the results page
    And I should see "5-day forecast"

  Scenario: Toggle unit to Fahrenheit
    Given I am on the home page
    When I set unit to "F"
    And I search for city "Pune"
    Then I should see temperatures displayed in "F"

  Scenario: Add favorite city
    When I search for city "Pune"
    And I add the city to favorites
    Then I should see "Pune" in the favorites list