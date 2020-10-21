# Faceit hub histogram
Given a player's nickname, return a JSON report with some metrics of their match history.

For each match, it stores the date it happened, if the player won or lost it and the dishonesty factor of his team.

The dishonesty factor is the sum of the square of the level differences of all the pairs of players in the same team.

# Example output
```
python main.py --player-name s1mple --faceit-api-key $(cat api-key)                                                                                
{'FPL CSGO Europe': [{'player_won': 1, 'dishonesty_factor': 0, 'match_date': 1601501881}, {'player_won': 1, 'dishonesty_factor': 0, 'match_date': 1601498065}, {'player_won': 0, 'dishonesty_factor': 0, 'match_date': 1601494014}, ...],
'CSGO 5v5': [...]
}
```

