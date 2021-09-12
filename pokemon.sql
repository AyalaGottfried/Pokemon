-- DROP DATABASE DB_Pokemon;
CREATE DATABASE DB_Pokemon;
use DB_Pokemon;
 CREATE table pokemon(
    id INT PRIMARY KEY,
    name varchar(50),
    height int,
    weight int
);
CREATE table types(
    pokemon_id INT,
    name varchar(50),
    primary key(pokemon_id, name),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE
);
CREATE table trainer(
    id int primary key AUTO_INCREMENT,
    name varchar(50),
    town varchar(50)
);
CREATE table owned_by(
    id_pokemon INT,
    id_trainer int,
    primary key (id_pokemon,id_trainer),
    FOREIGN KEY (id_pokemon) REFERENCES pokemon(id),
    FOREIGN KEY (id_trainer) REFERENCES trainer(id)
);  


