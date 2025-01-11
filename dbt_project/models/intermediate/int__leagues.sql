select *
from {{ source('tennis_raw', 'leagues') }}