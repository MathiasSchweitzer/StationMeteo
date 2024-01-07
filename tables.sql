CREATE TABLE data(
    dateDonnee VARCHAR(8) NOT NULL,
    heure VARCHAR(4) NOT NULL,
    typeDonnee VARCHAR(8) NOT NULL,
    donnee FLOAT NOT NULL,
    PRIMARY KEY (dateDonnee, heure, typeDonnee)
);