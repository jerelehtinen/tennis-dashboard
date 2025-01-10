{{
  config(
        materialized = 'incremental',
        unique_key = 'id',
        merge_exclude_columns = ['_dlt_parent_id', '_dlt_list_idx', '_dlt_id']
    )
}}

select *
from {{ source('tennis_raw', 'matches_by_date__matches') }}