CREATE DATABASE IF NOT EXISTS SolarXDWH;

USE SolarXDWH;


CREATE TABLE dimDate(
    date_key                        INT AUTO_INCREMENT,
    date                            DATE NOT NULL,
    year                            SMALLINT NOT NULL,
    quarter                         SMALLINT NOT NULL,
    month                           SMALLINT NOT NULL,
    week                            SMALLINT NOT NULL,
    day                             SMALLINT NOT NULL,
    is_weekend                      BOOLEAN
);


CREATE TABLE dimSolarPanel(
    solar_panel_key                 SMALLINT AUTO_INCREMENT,
    solar_panel_id                  SMALLINT,
    name VARCHAR(25)                NOT NULL,
	capacity_kwh                    FLOAT NOT NULL,

    PRIMARY KEY (solar_panel_key)
);


CREATE TABLE dimBattery(
    battery_key                     SMALLINT AUTO_INCREMENT,
    battery_id                      SMALLINT,
    name VARCHAR(25)                NOT NULL,
	capacity_kwh                    FLOAT NOT NULL,
    charge_max_speed_watt_second    FLOAT NOT NULL,

    PRIMARY KEY (battery_key)
);


CREATE TABLE dimHome(
    home_key                        SMALLINT AUTO_INCREMENT,
    home_id                         SMALLINT,
    name VARCHAR(25)                NOT NULL,

    PRIMARY KEY (home_key)
);


CREATE TABLE FactHomePower(
    home_power_key                  INT NOT NULL AUTO_INCREMENT,

    home_key                        SMALLINT NOT NULL REFERENCES dimHome(home_key),
    solar_pannel_key                SMALLINT REFERENCES dimSolarPanel(solar_panel_key),
    battery_key                     SMALLINT REFERENCES dimBattery(battery_key),
    date_key                        SMALLINT REFERENCES dimDate(date_key),

    power_consumption_amount        FLOAT NOT NULL,
    
    PRIMARY KEY (battery_power_key)
);


CREATE TABLE FactSolarPowerGeneration(
    solar_power_generation_key      INT NOT NULL AUTO_INCREMENT,

    solar_panel_key                 SMALLINT NOT NULL REFERENCES dimSolarPanel(solar_panel_key),
    date_key                        SMALLINT NOT NULL REFERENCES dimDate(date_key),

    power_generation_amount         FLOAT NOT NULL,

    PRIMARY KEY (solar_power_generation_key)
);

CREATE TABLE FactBatteryPower(
    battery_power_key               INT NOT NULL AUTO_INCREMENT,

    battery_key                     SMALLINT NOT NULL REFERENCES dimBattery(battery_key),
    date_key                        SMALLINT NOT NULL REFERENCES dimDate(date_key),

    power_generation_amount         FLOAT NOT NULL,
    power_consumption_amount        FLOAT NOT NULL,
    
    PRIMARY KEY (battery_power_key)
);