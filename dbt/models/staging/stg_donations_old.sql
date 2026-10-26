with src as (
    select *,
        concat_ws('|', campaign_id, donor_label, amount_uah) as natural_key
    from {{ source('raw', 'donations_old') }}
)
select
    md5(o.natural_key || '|' || row_number() over (partition by o.natural_key order by o.loaded_at)) as donation_id,
    o.campaign_id::int                                       as campaign_id,
    null::timestamptz                                        as donated_at,
    round(replace(o.amount_uah, ',', '.')::numeric, 2)       as amount_uah,
    o.currency,
    null::text                                               as donor_key,
    coalesce(a.donor_type,
        case o.donor_label when 'ч' then 'male'
                           when 'ж' then 'female'
                           else 'alias' end)                 as donor_type,
    'period'                                                 as time_precision
from src o
left join {{ ref('donor_aliases') }} a on lower(trim(o.donor_label)) = lower(a.alias)
