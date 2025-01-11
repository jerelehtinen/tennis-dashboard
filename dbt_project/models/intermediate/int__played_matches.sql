{{
  config(
        materialized = 'table',
    )
}}

select *
from {{ source('tennis_raw', 'past_matches_by_date__matches') }}