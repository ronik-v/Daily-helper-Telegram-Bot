CREATE TABLE Rates (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    rate_text VARCHAR(70) NOT NULL,
    rate_symbol VARCHAR(5) NOT NULL,
    sum_rub FLOAT NOT NULL
);

CREATE TABLE FinNews (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title VARCHAR(400) NOT NULL,
    text VARCHAR(1000) NOT NULL,
    url VARCHAR(400) NOT NULL
);