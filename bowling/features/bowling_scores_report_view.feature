Feature: Django bowling scores report view

    Scenario: I see who the bowling scores are for on the page
        Given the game:
            | name  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | carl  | 5,5 | 10  | 8,1 | 4,4 | 0,8 | 2,4 | 6,2 | 5,5 | 10  | 10,10,10 |
        And I run django's "bowl" command
        When I visit the "bowling_scores" page for the "bowler" "carl"
        Then I should see "Bowling Scores for: carl" on the web page

    Scenario: I see how many games the bowler has bowled
        Given the game:
            | name  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | carl  | 5,5 | 10  | 8,1 | 4,4 | 0,8 | 2,4 | 6,2 | 5,5 | 10  | 10,10,10 |
        And I run django's "bowl" command
        And The game:
            | name  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | carl  | 10  | 10  | 10  | 3,5 | 2,8 | 5,5 | 0,8 | 3,5 | 8,2 | 4,6,10   |
        And I run django's "bowl" command
        And The game:
            | name  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | carl  | 10  | 10  | 10  | 10  | 10  | 10  | 10  | 10  | 10  | 10,10,10 |
        And I run django's "bowl" command
        When I visit the "bowling_scores" page for the "bowler" "carl"
        Then I should see "carl has bowled 3 games" on the web page

    Scenario: I see each game's details
        Given the game:
            | name  | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | carl  | 1,1 | 2,2 | 3,3 | 4,4 | 5,5 | 6,0 | 7,0 | 8,0 | 9,0 | 0,0      |
        And I run django's "bowl" command
        When I visit the "bowling_scores" page for the "bowler" "carl"
        Then I should see "2" on the web page
        And I should see "6" on the web page
        And I should see "12" on the web page
        And I should see "20" on the web page
        And I should see "36" on the web page
        And I should see "42" on the web page
        And I should see "49" on the web page
        And I should see "57" on the web page
        And I should see "66" on the web page
