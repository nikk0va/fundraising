select
    campaign_id,
    name,
    start_date,
    end_date,
    end_date - start_date + 1 as duration_days
from {{ ref('stg_campaigns') }}
