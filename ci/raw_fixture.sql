CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

CREATE TABLE raw.campaigns (campaign_id bigint, name text, start_date text, end_date text);
INSERT INTO raw.campaigns VALUES
 (1, 'Fundraiser 1', '2025-03-09', '2025-03-12'),
 (3, 'Fundraiser 3', '2026-09-14', '2026-09-18'),
 (99, 'Simulated live fundraiser', '2026-10-18', '2026-12-31');

CREATE TABLE raw.donations_new (operation_ts text, category text, amount text, currency text,
  counterparty text, comment text, balance text, balance_currency text,
  campaign_id bigint, source_file text, loaded_at timestamptz);
INSERT INTO raw.donations_new VALUES
 ('14.09.2026 12:11', 'За посиланням', '100.00', 'UAH', 'Від: Test Donor', '', '100.00', 'UAH', 3, 'fixture', now()),
 ('15.09.2026 10:00', 'За посиланням', '200.00', 'UAH', 'Від: 🐈', '', '300.00', 'UAH', 3, 'fixture', now());

CREATE TABLE raw.donations_old (donor_label text, amount text, currency text, amount_uah text,
  source text, campaign_id bigint, source_file text, loaded_at timestamptz);
INSERT INTO raw.donations_old VALUES
 ('ж', '100', 'UAH', '100', 'Monobank jar', 1, 'fixture', now()),
 ('котик', '50', 'UAH', '50', 'Monobank jar', 1, 'fixture', now());

CREATE TABLE raw.donations_api (id text PRIMARY KEY, tx_time bigint, description text, comment text,
  amount bigint, balance bigint, currency_code int, jar_id text, campaign_id int,
  loaded_at timestamptz DEFAULT now());
INSERT INTO raw.donations_api (id, tx_time, description, amount, balance, currency_code, jar_id, campaign_id)
VALUES ('fixture0001', 1792800000, 'Від: Test Donor', 50000, 50000, 980, 'SIMJAR001', 99);
