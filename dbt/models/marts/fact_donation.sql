{{ config(materialized='incremental', unique_key='donation_id') }}

select
    donation_id,
    campaign_id,
    source_seq,
    donated_at,
    (donated_at at time zone 'Europe/Kyiv')::date   as donated_date,
    amount_uah,
    donor_key,
    donor_type,
    donor_type in ('cat', 'alias')                  as is_anonymous,
    donor_key is not null                           as is_name_known,
    time_precision
from {{ ref('stg_donations') }}

{% if is_incremental() %}
where donation_id not in (select donation_id from {{ this }})
{% endif %}
