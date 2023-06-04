CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE', 'OTHER');

CREATE TABLE IF NOT EXISTS Clismo_User (
    id VARCHAR(256) NOT NULL,
    username VARCHAR ( 256 ),
    password VARCHAR ( 256 ),
    gender gender_enum,
    weight FLOAT,
    height FLOAT,
    age INT
);

create index I_username on Clismo_User(username);
create index I_password on Clismo_User(password);
create index I_gender on Clismo_User(gender);
create index I_weight on Clismo_User(weight);
create index I_height on Clismo_User(height);
create index I_age on Clismo_User(age);