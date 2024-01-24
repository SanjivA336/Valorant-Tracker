# Valorant Tracker
A discord bot to track any Valorant player's statistics over time.
<br>
***Players must have an account on www.Tracker.gg for the bot to access their statistics***

## Add The Bot
[Add Valorant Tracker to your server](https://discord.com/api/oauth2/authorize?client_id=854765196550995979&permissions=116736&scope=bot)

## Controlling The Bot

### Bot Prefix:
    v!

### Available Commands
- Commands (`command`, `help`): Displays all the commands the robot can do.
  
        v!command
- Player Statistics (`stats`, `stat`, `track`): Find a player's statistics.

        v!stats {id} {mode}
  * Parameters:
    * `id`: name#number of the Valorant account.
    * `mode`: The game mode you want to check the stats on. Defaults to competitive.


- Player Weapons (`weapons`, `weapon`, `guns`, `gun`): Find the weapon statistics of a player.

        v!weapons {id} {mode}
  * Parameters:
    * `id`: name#number of the Valorant account.
    * `mode`: The game mode you want to check the stats on. Defaults to competitive.
- Player Playtime (`playtime`, `time`, `hours`): Find the amount of time a player has on Valorant.
  
        v!playtime {id}
  * Parameters:
    * `id`: name#number of the Valorant account. Replace spaces with a dash (-).
- Ping (`ping`): Checks the bot's ping.
  
        v!ping
