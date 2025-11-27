CREATE TABLE IF NOT EXISTS pokemon (
    num INTEGER,
    name VARCHAR(100) PRIMARY KEY,
    type1 VARCHAR(50),
    type2 VARCHAR(50),
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    sp_atk INTEGER,
    sp_def INTEGER,
    speed INTEGER,
    generation INTEGER,
    legendary BOOLEAN
);

COPY pokemon(num, name, type1, type2, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary)
FROM '/tmp/pokemon.csv'
DELIMITER ','
CSV HEADER;