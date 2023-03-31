/* 2.1 */
SELECT goal.playerName
FROM game
NATURAL JOIN goal
WHERE game.Stadium = 'Old Trafford';

/* 2.2 */
SELECT *
FROM goal
WHERE playerName LIKE '%Keane';

/* 2.3 */
SELECT COUNT(*) AS TotalGames
FROM game
WHERE Team1Name = 'AFC Richmond'
OR Team2Name = 'AFC Richmond';

/* 2.4 */
SElECT goal.*
FROM game AS g
NATURAL JOIN goal
WHERE (g.Team1Name = 'Manchester' AND g.Team2Name = 'Arsenal')
OR (g.Team1Name = 'Arsenal' AND g.Team2Name = 'Manchester');

/* 2.5 */
SELECT COUNT(*) AS TotalGoals
FROM goal
WHERE goalTime < 10;

/* 2.6 */
SELECT COUNT(*) AS TotalGoals
FROM goal
WHERE playerName LIKE 'Lionel%';

/* 2.7 */
SELECT Stadium, Count(*) AS TotalGames
FROM game
GROUP BY Stadium
HAVING TotalGames > 50;

/* 2.8 */
SELECT playerName, Count(*) AS TotalGoals
FROM goal
GROUP BY playerName
HAVING COUNT(DISTINCT gameID < 10);