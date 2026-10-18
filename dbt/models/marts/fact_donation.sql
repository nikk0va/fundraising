select
    row_number() over (order by campaign_id, donated_at, amount_uah)  as donation_id,
    campaign_id,
    donated_at,
    (donated_at at time zone 'Europe/Kyiv')::date                     as donated_date,
    amount_uah,
    donor_key,
    donor_type,
    donor_key is null                                                 as is_anonymous,
    time_precision
from {{ ref('stg_donations') }}
