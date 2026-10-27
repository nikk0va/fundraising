with c as (
    select
        campaign_id,
        name,
        start_date,
        end_date,
        end_date - start_date + 1                         as duration_days,
        row_number() over (order by start_date, campaign_id) as fundraiser_no
    from {{ ref('stg_campaigns') }}
)
select
    *,
    'Fundraiser ' || fundraiser_no as fundraiser_label
from c
