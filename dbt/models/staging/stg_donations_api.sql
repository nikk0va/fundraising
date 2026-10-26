with src as (
    select *,
        lower(trim(regexp_replace(description, '^Від:\s*', ''))) as donor_name
    from {{ source('raw', 'donations_api') }}
)
select
    md5('api|' || s.id)                                      as donation_id,
    s.campaign_id                                            as campaign_id,
    to_timestamp(s.tx_time)                                  as donated_at,
    round(s.amount / 100.0, 2)                               as amount_uah,
    'UAH'                                                    as currency,
    case when a.alias is null then encode(sha256(convert_to(
        '{{ env_var("DONOR_SALT", "dev_salt") }}' || s.donor_name,
        'UTF8')), 'hex') end                                 as donor_key,
    coalesce(a.donor_type, 'named')                          as donor_type,
    'exact'                                                  as time_precision
from src s
left join {{ ref('donor_aliases') }} a on s.donor_name = lower(a.alias)
