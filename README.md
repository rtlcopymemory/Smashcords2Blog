# Smashcords2Blog
Discord Bot developed for Smashcords to archive messages in a static blog

## Dependencies
- PostgreSQL or docker + docker-compose

Not directly needed to run the bot but needed to create the static website:
- hugo

## Install
```
git clone git@github.com:WolfenCLI/Smashcords2Blog.git
```

Soon: a `make` script will generate the `start.sh` file

**This Bot requires a PostgreSQL database**, example configuration can be taken by the `docker-compose.yml` file.  
Alternatively you can edit and use the `docker-compose.yml` file included.  
Once the database is up, run the `database/init.sql` script to setup the neccessary schema.

### How to start
To start the bot, first set the following environment variables (soon replaced with start.sh script):
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

## Build website sources
```
./build.sh
```
Now copy the content of the `public` folders to the root of your webserver.

### Deploy the blog
This bot creates .md files to be built with hugo into a blog.  
I personally used the following theme: [Learn](https://themes.gohugo.io/hugo-theme-learn/)  
To move and build the files I use a script on a crontab every 15 minutes.

## TODO
- Dockerize the bot too (adding hugo-src as a volume)
- Add a script (Makefile) to generate the startup script with the environment variables set
- Include attachments (images) to messages