select
    campaign_id::int  as campaign_id,
    name,
    start_date::date  as start_date,
    end_date::date    as end_date
from {{ source('raw', 'campaigns') }}
