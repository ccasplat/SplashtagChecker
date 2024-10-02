# SplashtagChecker
A small library used for verifying Splashtags across Battlefy and Google Forms

## Maintainers
- dama

## Purpose
To ensure the integrity of CCA events, we need to ensure that teams both register on Google Form and Battlefy.
The purpose of this library is to compare teams from Battlefy and Google Forms to ensure teams and team rosters 
are consistent with each other.

The current usage of this library in the CCA is to generate a Discord message that can be sent in an Announcements 
channel for captains to view.

## Requirements
Python 3.9+

## Usage
You will need to download csvs from both Google Forms and Battlefy to run this library. Headers for each csv file can
be modified in the `utl/parse_csv.py` file if required.
```
$ python3.9 main.py --help 
usage: SplashtagChecker [-h] [-b BATTLEFY_FILENAME] [-g GFORM_FILENAME]

Checks Splashtags given two csvs from Google Forms and Battlefy

optional arguments:
  -h, --help            show this help message and exit
  -b BATTLEFY_FILENAME, --battlefy-filename BATTLEFY_FILENAME
                        File path to Battlefy's csv export
  -g GFORM_FILENAME, --gform-filename GFORM_FILENAME
                        File path to Google Form's csv export

Written by dama for the CCA, hi Frosty!
```

```
$ python3.9 main.py -b path/to/battlefy.csv -g path/to/gform.csv
## Splashtag Errors on Battlefy
The below teams have players on Battlefy that do not have a properly formatted Splashtag:
- dama's A-team: @def | `drf`, `mizuno`
- dama's B-team: @abc | `dama`, `damazon`

## Teams that have not registered via Google form
The below teams registered on Battlefy but did not register via Google Form:
- `UCSD Esports Gold`: @adam 

## Splashtag Cross Check
The below teams have players with splashtags that are different across Battlefy and Google Form registrations:
- UCSD Esports Navy: @notadam 
  - Players only on Battlefy: `ad a m #1234`, `Notadam#9876`
  - Players only on Google Form: `adam#1234`, `notadam#9876`
- dama's A-team: @def
  - Players only on Battlefy: `drf`, `mizuno`
  - Players only on Google Form: `drf#1234`, `mizuno#9876`
- dama's B-team: @abc
  - Players only on Battlefy: `dama`, `damazon`
  - Players only on Google Form: `dama#1234`, `damazon#9876`, `player#87654`
```

### Additional Notes
If you do not populate one or both of the above arguments, it will default to the values of the`battlefy_csv_filename` 
and `gform_csv_filename` variables in `main.py` respectively. 

There is a warning that will alert you if the age of both Battlefy csv and the Google Form csv have a difference of more
than 5 minutes. Another way of saying this is that both csv files must be generated within 5 minutes of each other. 
This is to ensure we properly crosschecking the correct exports.

In the `Splashtag Cross Check` section, we check with strict typing. We only correct Splashtags by removing any 
trailing/leading spaces and any Splashtags with a space between the username and the octothorpe. It is up to staff 
members to review and determine if a Splashtag discrepancy should be allowed or not.  
