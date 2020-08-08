# Smashcords2Blog
Discord Bot developed for Smashcords to archive messages in a static blog

## Dependencies
- PostgreSQL or docker + docker-compose

Not directly needed to run the bot but needed to create the static website:
- hugo

## Install
```
git clone git@github.com:WolfenCLI/Smashcords2Blog.git
cd Smashcords2Blog/hugo-src
hugo init
git submodule add https://github.com/jakewies/hugo-theme-codex.git themes/hugo-theme-codex
```
Then the first time you'll add the bot to a server it will generate the `config.toml` file automatically.

### How to start
Either use you own postgreSQL installation or use the one provided with the docker-compose.  
If it's the first time you start the database, remember to initialize it with `database/init.sql`.  
To start the bot, first set the following environment variables:
```
DBNAME=postgres
DBUSER=postgres
DBPASS=development
DBHOST=localhost
DBPORT=5432
BOT_TOKEN=
OWNER_ID=
```
I left the default values for the docker PostgreSQL included, you might want to change at least the password.

## Build website
```
cd hugo-src
hugo
```
Now copy the content of the `public` folder in the root of your webserver.

### Deploy the blog
This bot creates .md files to be built with hugo into a blog.  
I personally used the following theme: [Codex](https://themes.gohugo.io/hugo-theme-codex/)  
To move and build the files I use a script on a crontab every 15 minutes.

## TODO
- Dockerize the bot too (adding hugo-src as a volume)
- Add a script to generate the startup script with the environment variables set
