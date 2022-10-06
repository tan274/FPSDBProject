DROP PROCEDURE IF EXISTS GetStages;

DELIMITER //

CREATE PROCEDURE GetStages ( IN varStageName varchar(100) )
BEGIN
	IF varStageName = '' THEN
		SELECT * FROM Stage;
	ELSE
		SELECT * FROM Stage WHERE stageName = varStageName;
	END IF;
END //

DELIMITER ;