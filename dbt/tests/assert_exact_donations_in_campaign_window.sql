-- повертає "погані" рядки: точні донати поза періодом збору. Порожній результат = тест пройдено
select f.*
from {{ ref('fact_donation') }} f
join {{ ref('dim_campaign') }} c using (campaign_id)
where f.time_precision in ('exact', 'day')
  and f.donated_date not between c.start_date and c.end_date
