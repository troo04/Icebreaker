# Icebreaker
A discord bot meant to bring people closer :)

# Inspiration
Our inspiration for creating this project was our own experiences during this pandemic. Our ability to mingle/meet new people were negatively affected, due to many restrictions placed at school, at parks, movie theaters, and etc.

# What it does
The Icebreaker Bot asks users to create profiles and then connects them to others with similar interests

# How we built it
To create and test the bot, we used the library Discord.py, the API wrapper for Discord written in Python, to create and test our discord bot. We used flask, a web framework written in Python, for running our bot on a web server, therefore eliminating the need for the continual running of the bot's python script. However, a web server, on its own, will only run for up to an hour when it is not in use. This is where the Uptime robot comes in, Uptime robot will ping the webserver every 5 minutes, therefore the webserver hosted on repl.it, will never shut down since constant requests are being made.

# Challenges we ran into
As time progressed, and the more we began to run the bot for testing purposes, we constantly overloaded the Discord API. This led to the timing out of the bot, which meant we had to find a work around to this issue. Another problem we ran into, was the use of several different clients. Each client had it's own job, and other clients were not able to run the jobs of other clients. This led to the question of how to either combine all of these individual clients into one or the running of several clients at once. This posed as a time-consuming issue.

# Accomplishments that we're proud of
We are proud of successfully creating a discord bot useful to the community

# What we learned
Since this was our first time creating a discord bot together, we were faced with several bugs and logical issues, which programmers well-versed with Discord.py, would not have faced. Throughout the creation of our project, we have learned many things on how to create a discord bot, how to host one, how to get help on debugging, and more.

# What's next for IceBreaker
The next step for Icebreaker is to publicize our bot and get it out into many servers. This way many people will benefit from our bot, by finding and meeting people, who they would have never due to the pandemic.
