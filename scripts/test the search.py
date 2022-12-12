TEMP_ORDER_dict = (
    (0, None),
    (1, '0 to 5 up','1 up', '2 up', '3 up', '4 up', '1up', '2up', '3up', '4up', '1u', '2u', '3u', '4u'), 
    (2, '6 up', '6up', '6u', '6up'),
    (3, '7 up', '7up', '7u', '7up'),
    (4, '8 up', '8up', '8u', '8up'),
    (5, '9 up', '9up', '9u', '9up'),
    (6, '10 up', '10up', '10u', '10up'),
    (7, '11 up', '11up', '11u', '11up'),
    (8, '12 up', '12up', '12u', '12up'),
    (9, '13 up', '13up', '13u', '13up'),
    (10, '14 up', '14up', '14u', '14up'),
    (11, '15 up', '15up', '15u', '15up'),
    (12, '16 up', '16up', '16u', '16up'),
    (13, '17 up', '17up', '17u', '17up'),
    (14, '18 up', '18up', '18u', '18up'),
    (15, '19 up', '19up', '19u', '19up'),
    (16, '20 up', '20up', '20u', '20up'),
    (17, '21 up', '21up', '21u', '21up'),
    (18, '22 up', '22up', '22u', '22up'),
    (19, 'above 22', 'above22', '23', '24', '25', '23u', '24u', '25u', '23d', '24d', '25d'),
    (20, '22 down', '22down', '22down', '22d'),
    (21, '21 down', '21down', '21down', '21d'),
    (22, '20 down', '20down', '20down', '20d'),
    (23, '19 down', '19down', '19down', '19d'),
    (24, '18 down', '18down', '18down', '18d'),
    (25, '17 down', '17down', '17down', '17d'),
    (26, '16 down', '16down', '16down', '16d'),
    (27, '15 down', '15down', '15down', '15d'),
    (28, '14 down', '14down', '14down', '14d'),
    (29, '13 down', '13down', '13down', '13d'),
    (30, '12 down', '12down', '12down', '12d'),
    (31, '11 down', '11down', '11down', '11d'),
    (32, '10 down', '10down', '10down', '10d'),
    (33, '9 down', '9down', '9down', '9d'),
    (34, '8 down', '8down', '8down', '8d'),
    (35, '7 down', '7down', '7down', '7d'),
    (36, '6 down', '6down', '6down', '6d'),
    (37, '5 down', '5down', '5down', '5d'),
    (38, '4 down to 0', '4downto0', '4downto0', '4dto0','3down', '2down', '1down', '4d', '3d', '2d', '1d'),
     )

for sublist in TEMP_ORDER_dict:
    # print (sublist)
    edit = str(sublist[1])
    new_data1 = (edit.replace(" ", ""))
    new_data2 = (new_data1.replace("p", ""))
    new_data3 = (new_data1.replace("own", ""))

    line = (f"({sublist[0]}, '{sublist[1]}', '{new_data1}', '{new_data2}', '{new_data3}'),")

    print (line)

