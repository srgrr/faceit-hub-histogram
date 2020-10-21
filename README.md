# Faceit history report
Given a FACEIT player nickname, return a JSON report with some metrics of their match history. It also includes a stats script to print a summary of the stored report.

For each match, it stores the date it took place, if the player won or lost the match and the dishonesty factor of his team.

The dishonesty factor is the sum of the square of the level differences of all the pairs of players in the same team.

You need and API Key from FACEIT 

# Example output
```
python history.py --player-name s1mple --faceit-api-key $(cat api-key)                                                                                
{'FPL CSGO Europe': [{'player_won': 1, 'dishonesty_factor': 0, 'match_date': 1601501881}, {'player_won': 1, 'dishonesty_factor': 0, 'match_date': 1601498065}, {'player_won': 0, 'dishonesty_factor': 0, 'match_date': 1601494014}, ...],
'CSGO 5v5': [...]
}
```

If you instead deviate the standard output to a file and store it for future use you can feed it 