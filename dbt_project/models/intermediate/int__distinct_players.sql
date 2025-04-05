select distinct home_team_name as player_or_team_name
from {{ ref('int__played_matches') }}

union 

select distinct away_team_name as player_or_team_name
from {{ ref('int__played_matches') }}