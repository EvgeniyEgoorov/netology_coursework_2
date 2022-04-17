# VKinder

Best _(definitely)_ service for finding new acquaintances!

## Execution

````
You need to specify `group_auth` in handler.py - it can be found in VK group settings and required for bot to respond 
to messages sent to the group. `db_name` and `db_auth` - data source name to your PostgreSQL database 
(eg. postgresql://name:auth@localhost:5432/db).
To allow the bot authenticate with a user token you need to specify `user_auth` in handler.py. 
This is necessary to perform the user search.
Run main.py
````
