select * from {{ ref('stg_donations_new') }}
union all
select * from {{ ref('stg_donations_old') }}
union all
select * from {{ ref('stg_donations_api') }}
union all
select * from {{ ref('stg_donations_manual') }}
