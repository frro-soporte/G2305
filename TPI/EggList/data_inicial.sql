START TRANSACTION;
/*
Seleccionar BBDD del proyecto


*/
/*

Roles

*/



INSERT INTO `egglist`.`roles`
(`name`)
VALUES
('Usuario');

INSERT INTO `egglist`.`roles`
(`name`)
VALUES
('Admin');


/*
Roles en lista
*/


INSERT INTO `egglist`.`roles_en_lista`
(`name`)
VALUES
('Armador');

INSERT INTO `egglist`.`roles_en_lista`
(`name`)
VALUES
('Comprador');
/*

PROVINCIAS

*/



#PROV ID 1
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Buenos Aires');

#PROV ID 2
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('CABA');

#PROV ID 3
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Catamarca');

#PROV ID 4
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Chaco');

#PROV ID 5
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Chubut');

#PROV ID 6
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Córdoba');

#PROV ID 7
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Corrientes');

#PROV ID 8
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Entre Ríos');


#PROV ID 9
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Formosa');

#PROV ID 10
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Jujuy');

#PROV ID 11
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('La Pampa');

#PROV ID 12
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('La Rioja');

#PROV ID 13
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Mendoza');

#PROV ID 14
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Misiones');

#PROV ID 15
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Neuquén');

#PROV ID 16
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Río Negro');

#PROV ID 17
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Salta');

#PROV ID 18
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('San Juan');

#PROV ID 19
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('San Luis');

#PROV ID 20
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santa Cruz');

#PROV ID 21
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santa Fe');

#PROV ID 22
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santiago del Estero');

#PROV ID 23
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Tierra del fuego');

#PROV ID 24
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Tucumán');

#PROV ID 25
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Antártida');

#PROV ID 26
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Islas Malvinas');

#PROV ID 27
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Uruguay');



















/* 
CIUDADES
*/



#Provincia de Santa Fe





#CAÑADA
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`,
`position_x`,
`position_y`,
`min_zoom`)
VALUES
(2500,
'Cañada de Gomez',
21,
-32.8128982,
-61.3991846,
13);


#CHABÁS
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`,
`position_x`,
`position_y`,
`min_zoom`)
VALUES
(2173,
'Chabás',
21,
-33.2439432,
-61.362308,
14);

#ROSARIO
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`,
`position_x`,
`position_y`,
`min_zoom`)
VALUES
(2000,
'Rosario',
21,
-32.9493696,
-60.6480603,
11);


#VILLA CAÑÁS
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`,
`position_x`,
`position_y`,
`min_zoom`)
VALUES
(2607,
'Villa Cañás',
21,
-34.0072577,
-61.6035609,
13);











/*
Supermercados
*/



#Cañada
INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Super Ahorro (Chacabuco 747)',
2500,
-32.814596,
-61.3820704);


#CHABÁS
INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('El Solar Supermercado(Mitre 1679)',
2173,
-33.2456195,
-61.3578597);

#ROSARIO
INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Supermercado La Reina(San Martín 3419)',
2000,
-32.9769227,
-60.6513294);

INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Carrefour (27 feb 100)',
2000,
-32.9699811,
-60.6293451);

INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Tienda de medallas "Forjador de Campeones"(Av. Alberdi 23 bis )',
2000, 
-32.9297296,
-60.6738319);

INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Tienda de impresoras municipal(Av. Int. Morcillo 2501-2699)',
2000,
-32.9566572,
-60.6638297);


#VILLA CAÑAS
INSERT INTO `egglist`.`supermercados`
(`nombre`,
`cod_postal`,
`position_x`,
`position_y`)
VALUES
('Supermercados Dia(299, calle 7)',
2607,
-34.0025696,
-61.6097995);


COMMIT;