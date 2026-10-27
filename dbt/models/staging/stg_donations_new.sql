with src as (
    select *,
        lower(trim(regexp_replace(counterparty, '^Від:\s*', ''))) as donor_name,
        concat_ws('|', campaign_id, operation_ts, amount, counterparty, balance) as natural_key
    from {{ source('raw', 'donations_new') }}
    where counterparty is not null
)
select
    md5(s.natural_key || '|' || row_number() over (partition by s.natural_key order by s.loaded_at)) as donation_id,
    s.campaign_id::int                                       as campaign_id,
    (to_timestamp(s.operation_ts, 'DD.MM.YYYY HH24:MI')::timestamp)
        at time zone 'Europe/Kyiv'                           as donated_at,
    round(replace(s.amount, ',', '.')::numeric, 2)           as amount_uah,
    s.currency,
    case when a.alias is null then encode(sha256(convert_to(
        '{{ env_var("DONOR_SALT") }}' || s.donor_name,
        'UTF8')), 'hex') end                                 as donor_key,
    coalesce(a.donor_type, 'named')                          as donor_type,
    'exact'                                                  as time_precision
from src s
left join {{ ref('donor_aliases') }} a on s.donor_name = lower(a.alias)
