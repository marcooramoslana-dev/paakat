USE paakat;

SET NAMES utf8mb4;

INSERT INTO categories (id, name, slug, description) VALUES
    (1, 'Cultura Maya', 'maya', 'Civilizacion mesoamericana de la peninsula de Yucatan, Chiapas y Campeche.'),
    (2, 'Cultura Mexica (Azteca)', 'mexica', 'Civilizacion del valle de Mexico, capital Tenochtitlan.'),
    (3, 'Cultura Teotihuacana', 'teotihuacana', 'Civilizacion que construyo la gran ciudad de Teotihuacan.'),
    (4, 'Cultura Zapoteca', 'zapoteca', 'Civilizacion de los valles centrales de Oaxaca.'),
    (5, 'Cultura Totonaca', 'totonaca', 'Civilizacion del Golfo de Mexico, en la costa de Veracruz.'),
    (6, 'Cultura Tolteca', 'tolteca', 'Civilizacion del altiplano central con centro en Tula.'),
    (7, 'Cultura Olmeca', 'olmeca', 'Civilizacion precolombina de la costa del Golfo, conocida por sus cabezas colosales.'),
    (8, 'Cultura Purepecha', 'purepecha', 'Civilizacion de Michoacan, con su capital Tzintzuntzan.')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO elements
    (id, category_id, name, slug, location, era, description, clip_prompt)
VALUES
    (1, 1, 'Chichen Itza', 'chichen-itza', 'Yucatan, Mexico', 'Clasico Terminal (600-1200 d.C.)',
     'Ciudad maya dominada por la piramide de Kukulcan (El Castillo), Patrimonio de la Humanidad y una de las Nuevas Siete Maravillas del Mundo.',
     'the El Castillo step pyramid of Chichen Itza, a Maya archaeological site in Yucatan, Mexico'),
    (2, 1, 'Tulum', 'tulum', 'Quintana Roo, Mexico', 'Posclasico (1200-1500 d.C.)',
     'Unica ciudad maya amurallada construida frente al mar Caribe; destaca el Templo del Dios Descendente y El Castillo sobre el acantilado.',
     'the Tulum archaeological site, an ancient Maya walled city with a temple on a cliff above the turquoise Caribbean sea'),
    (3, 1, 'Uxmal', 'uxmal', 'Yucatan, Mexico', 'Clasico (700-1000 d.C.)',
     'Ciudad maya de estilo Puuc famosa por la Piramide del Adivino, el Cuadrangulo de las Monjas y la Casa de las Tortugas.',
     'the Pyramid of the Magician at Uxmal, a Maya Puuc style archaeological site in Yucatan, Mexico'),
    (4, 1, 'Palenque', 'palenque', 'Chiapas, Mexico', 'Clasico (600-900 d.C.)',
     'Ciudad maya rodeada de selva, celebre por el Templo de las Inscripciones, la tumba de Pakal y su refinada arquitectura.',
     'the Temple of the Inscriptions at Palenque, a Maya archaeological site surrounded by jungle in Chiapas, Mexico'),
    (5, 1, 'Calakmul', 'calakmul', 'Campeche, Mexico', 'Preclasico-Clasico (300 a.C.-900 d.C.)',
     'Una de las ciudades mayas mas grandes, oculta en la Reserva de la Biosfera de Calakmul; famosa por sus estelas y su gran piramide.',
     'the great Maya city of Calakmul with tall pyramids rising above the rainforest in Campeche, Mexico'),
    (6, 1, 'Coba', 'coba', 'Quintana Roo, Mexico', 'Preclasico-Posclasico (100 a.C.-1500 d.C.)',
     'Ciudad maya con una extensa red de sacbeob (caminos) y la piramide de Nohoch Mul, la mas alta de la peninsula de Yucatan.',
     'the Nohoch Mul pyramid at Coba, a tall ancient Maya pyramid in the jungle of Quintana Roo, Mexico'),
    (7, 2, 'Templo Mayor', 'templo-mayor', 'Ciudad de Mexico, Mexico', 'Posclasico (1325-1521 d.C.)',
     'Centro ceremonial principal de Tenochtitlan, la capital mexica; dedicado a Huitzilopochtli y Tlaloc.',
     'the Templo Mayor ruins, the main Aztec ceremonial pyramid of Tenochtitlan in Mexico City'),
    (8, 3, 'Teotihuacan', 'teotihuacan', 'Estado de Mexico, Mexico', 'Preclasico-Clasico (100 a.C.-550 d.C.)',
     'La ciudad prehispanica mas grande de Mesoamerica, con las Piramides del Sol y la Luna y la Calzada de los Muertos.',
     'the Pyramid of the Sun and the Avenue of the Dead at Teotihuacan, the largest ancient city in Mexico'),
    (9, 4, 'Monte Alban', 'monte-alban', 'Oaxaca, Mexico', 'Preclasico-Clasico (500 a.C.-800 d.C.)',
     'Antigua capital zapoteca construida sobre una montana, con plazas, templos y observatorio astronomico.',
     'the Monte Alban Zapotec archaeological site with stone platforms and pyramids on a flattened mountain top in Oaxaca, Mexico'),
    (10, 4, 'Mitla', 'mitla', 'Oaxaca, Mexico', 'Posclasico (900-1500 d.C.)',
     'Sitio zapoteco conocido por sus complejos mosaicos de grecas de piedra y sus tumbas.',
     'the Mitla archaeological site with intricate geometric stone mosaic fretwork in Oaxaca, Mexico'),
    (11, 5, 'El Tajin', 'el-tajin', 'Veracruz, Mexico', 'Clasico (600-1200 d.C.)',
     'Ciudad totonaca celebre por la Piramide de los Nichos y sus juegos de pelota; Patrimonio de la Humanidad.',
     'the Pyramid of the Niches at El Tajin, a Totonac archaeological site in Veracruz, Mexico'),
    (12, 6, 'Tula', 'tula', 'Hidalgo, Mexico', 'Posclasico (900-1150 d.C.)',
     'Capital tolteca famosa por los Atlantes, columnas en forma de guerreros que sostenian el techo de un templo.',
     'the Atlantean warrior columns at Tula, the ancient Toltec capital in Hidalgo, Mexico'),
    (13, 7, 'La Venta', 'la-venta', 'Tabasco, Mexico', 'Preclasico (900-400 a.C.)',
     'Centro ceremonial olmeca famoso por sus cabezas colosales de piedra y su piramide de tierra.',
     'the colossal Olmec stone heads at La Venta, an ancient Olmec site in Tabasco, Mexico'),
    (14, 8, 'Tzintzuntzan', 'tzintzuntzan', 'Michoacan, Mexico', 'Posclasico (1200-1530 d.C.)',
     'Antigua capital del pueblo purepecha, con sus yacatas: plataformas y templos de base semicircular.',
     'the yacatas semicircular platforms of Tzintzuntzan, the ancient Purepecha capital in Michoacan, Mexico')
ON DUPLICATE KEY UPDATE name = VALUES(name);
