with m as (
    select *, row_number() over (partition by campaign_id order by donor_label, amount_uah) as rn
    from {{ ref('manual_donations') }}
),
base as (
    select campaign_id, max(source_seq) as max_seq
    from {{ ref('stg_donations_old') }}
    group by 1
)
select
    md5('manual|' || m.campaign_id || '|' || m.donor_label || '|' || m.amount_uah || '|' || m.rn) as donation_id,
    coalesce(b.max_seq, 0) + m.rn                            as source_seq,
    m.campaign_id::int                                       as campaign_id,
    null::timestamptz                                        as donated_at,
    round(m.amount_uah::numeric, 2)                          as amount_uah,
    'UAH'                                                    as currency,
    null::text                                               as donor_key,
    coalesce(a.donor_type,
        case m.donor_label when 'ч' then 'male' when 'ж' then 'female' else 'alias' end) as donor_type,
    'period'                                                 as time_precision
from m
left join base b on b.campaign_id = m.campaign_id
left join {{ ref('donor_aliases') }} a on lower(trim(m.donor_label)) = lower(a.alias)
