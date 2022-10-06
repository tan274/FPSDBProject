DROP PROCEDURE IF EXISTS GetMonsters;

DELIMITER //

CREATE PROCEDURE GetMonsters ( IN varMonsterName varchar(100) )
BEGIN
	/* SET NOCOUNT ON; */
	IF varMonsterName = '' THEN THEN
		SELECT * FROM Monsters;
	ELSE
		SELECT * FROM Monsters WHERE monsterName = varMonsterName;
	END IF;
END //

DELIMITER ;