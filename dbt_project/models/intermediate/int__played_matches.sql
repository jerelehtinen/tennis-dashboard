{{
  config(
    materialized = 'incremental',
    unique_key = 'id',
    )
}}

with matches as (
    select *
    from {{ source('tennis_raw', 'past_month_matches__matches') }}
),

leagues as (
    select *
    from {{ source('tennis_raw', 'leagues') }}
)

select
    matches.id,
    matches.name,
    matches.status,
    matches.status_reason,
    matches.duration,
    matches.start_time as start_datetime,
    matches.start_time::date as start_date,
    matches.home_team_id,
    matches.home_team_name,
    matches.away_team_id,
    matches.away_team_name,
    matches.home_team_score,
    matches.away_team_score,
    matches.tournament_id,
    matches.tournament_name,
    matches.tournament_importance,
    matches.league_id,
    leagues.name as league_name,
    leagues.importance as league_importance,
    leagues.current_champion_team_id as league_current_champion_team_id,
    leagues.current_champion_team_name as league_current_champion_team_name,
    leagues.ground as league_ground,
    leagues.number_of_sets as league_number_of_sets,
    leagues.start_league as league_start_league,
    leagues.end_league as league_end_league,
    leagues.class_id as league_class_id,
    leagues.class_name as league_class_name,
    matches.season_id,
    matches.season_name,
    matches.away_team_period_1_score,
    matches.away_team_period_2_score,
    matches.away_team_period_3_score,
    matches.away_team_period_4_score,
    matches.home_team_period_1_score,
    matches.home_team_period_2_score,
    matches.home_team_period_3_score,
    matches.home_team_period_4_score
from matches
left join leagues on
    matches.league_id = leagues.id
