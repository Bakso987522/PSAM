CREATE TABLE IF NOT EXISTS import_history (
    id           SERIAL PRIMARY KEY,
    published_at TIMESTAMPTZ,
    imported_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    status       TEXT NOT NULL,
    message      TEXT
);

-- Dictionaries

CREATE TABLE active_substance (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE product_type (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE crop (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE pest (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE application_group (
    id smallint PRIMARY KEY,
    name text NOT NULL
);

-- Product
CREATE TABLE product (
    id_sor             varchar(38) PRIMARY KEY,   -- GUID from register
    name               text NOT NULL,
    producer           text NOT NULL,
    permit_number      text NOT NULL,
    permit_valid_until date NOT NULL,
    sale_allowed_until date NOT NULL,
    use_allowed_until  date NOT NULL,
    for_amateurs       boolean NOT NULL,
    packaging          text,
    label_url          text,
    label_matched      boolean NOT NULL DEFAULT false,
    base_product_name  text,
    removed_at         date
);

CREATE TABLE product_product_type (
    product_id      varchar(38) NOT NULL REFERENCES product ON DELETE CASCADE,
    product_type_id integer     NOT NULL REFERENCES product_type,
    PRIMARY KEY (product_id, product_type_id)
);

CREATE TABLE product_substance (
    product_id   varchar(38) NOT NULL REFERENCES product ON DELETE CASCADE,
    substance_id integer     NOT NULL REFERENCES active_substance,
    content      numeric(12, 4),
    unit         varchar(10),
    PRIMARY KEY (product_id, substance_id)
);

CREATE TABLE usage (
    id                   serial PRIMARY KEY,
    product_id           varchar(38) NOT NULL REFERENCES product ON DELETE CASCADE,
    group_id             smallint    NOT NULL REFERENCES application_group,
    dose                 text,
    timing               text,
    method               text,
    combined_use         text,
    minor_use            boolean NOT NULL DEFAULT false,
    pre_harvest_days     smallint,
    pre_harvest_source   varchar(20)
);

CREATE TABLE usage_crop (
    usage_id integer NOT NULL REFERENCES usage ON DELETE CASCADE,
    crop_id  integer NOT NULL REFERENCES crop,
    PRIMARY KEY (usage_id, crop_id)
);

CREATE TABLE usage_pest (
    usage_id integer NOT NULL REFERENCES usage ON DELETE CASCADE,
    pest_id  integer NOT NULL REFERENCES pest,
    PRIMARY KEY (usage_id, pest_id)
);

-- Foreign keys
CREATE INDEX usage_product_idx ON usage (product_id);
CREATE INDEX usage_crop_crop_idx ON usage_crop (crop_id);
CREATE INDEX usage_pest_pest_idx ON usage_pest (pest_id);
CREATE INDEX product_substance_sub_idx ON product_substance (substance_id);
CREATE INDEX product_product_type_tp_idx ON product_product_type (product_type_id);
