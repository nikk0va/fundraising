select
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
from {{ source('raw', 'donations_old') }} o
left join {{ ref('donor_aliases') }} a on lower(trim(o.donor_label)) = lower(a.alias)
