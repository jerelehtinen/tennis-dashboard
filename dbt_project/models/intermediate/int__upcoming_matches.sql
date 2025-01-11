{{
  config(
        materialized = 'table',
    )
}}

select *
from {{ source('tennis_raw', 'future_matches_by_date__matches') }}