Feature: Django bowling_scores command

    Scenario: I can view my previous bowling scores
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
        When I run django's "bowling_scores" command with "carl"
        Then I should see "carl: [20][39][48][56][64][70][78][98][128][158]"
        And I should see "carl: [30][53][71][79][94][104][112][120][134][154]"
        And I should see "carl: [30][60][90][120][150][180][210][240][270][300]"
