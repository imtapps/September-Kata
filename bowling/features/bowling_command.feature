Feature: Django bowl command

    Scenario: Bowl a game with one player
        Given the game:
            | name | 1  |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 |  10       |
            | matt | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10,10,10  |
        When I run django's "bowl" command
        Then I should see "matt: [30][60][90][120][150][180][210][240][270][300]"

    Scenario: Bowl a game with two bowlers
        Given the games:
            | name |  1  | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10       |
            | matt | 1,1 | 2,2 | 3,3 | 4,4 | 5,5 | 1,1 | 2,2 | 3,3 | 4,4 | 5,5,10   |
            | fred | 2,2 | 2,2 | 2,2 | 2,2 | 2,2 | 2,2 | 2,2 | 2,2 | 2,2 | 2,2      |
        When I run django's "bowl" command
        Then I should see "matt: [2][6][12][20][31][33][37][43][51][71]"
        And I should see "fred: [4][8][12][16][20][24][28][32][36][40]"