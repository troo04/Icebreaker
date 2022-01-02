import os
import discord
from server import keep_running
from discord_components import ComponentsBot, Select, SelectOption
from discord.ext import commands
from discord.utils import get
from replit import db

intents = discord.Intents.default()
intents.members = True

client = ComponentsBot("!", intents=intents)



def compare(sender, comparing_with):
  num_of_simillar = 0
  for i in range(len(sender)):
    if len(comparing_with) != 0 and sender[i] == comparing_with[i]:
      num_of_simillar += 1
  
  return round(num_of_simillar/len(sender) * 100, 2)

def get_people(percentages):
  list_of_people = []
  midpoint = len(percentages) // 2

  for index in range(len(percentages)):
    if index >= midpoint:
      list_of_people.append(percentages[index][1])
  
  return list_of_people

@client.event
async def on_member_join(member):
  channel = client.get_channel(int(os.environ['channel_id']))
  embed1=discord.Embed(title="Type `!create_profile` to get started!", color=discord.Color.blue())
  await channel.send(f'Welcome <@{member.id}>!\n')
  embed=discord.Embed(title="Commands:")
  embed.add_field(name="`!create_profile`", value="Allows the user to set up a profile for themselves\n", inline=False)
  embed.add_field(name="`!update_profile`", value="The user can update their profile, if they wish to.", inline=False)
  embed.add_field(name="`!delete_profile`", value="This command will delete the user's profile.", inline=False)
  embed.add_field(name="`!find_friend`", value="This command will personally dm the user, a person who shares simillar interests as them.", inline=False)
  embed.add_field(name="`!find_friends`", value="This command will create a private text channel, with people who best match your interets, where you can chat with them.", inline=False)
  await channel.send(embed=embed)
  await channel.send(embed=embed1)


@client.event
async def on_ready():
  channel = client.get_channel(int(os.environ['channel_id']))
  print('{0.user} is online'.format(client))

  embed=discord.Embed(title="Commands:")
  embed.add_field(name="`!create_profile`", value="Allows the user to set up a profile for themselves\n", inline=False)
  embed.add_field(name="`!update_profile`", value="The user can update their profile, if they wish to.", inline=False)
  embed.add_field(name="`!delete_profile`", value="This command will delete the user's profile.", inline=False)
  embed.add_field(name="`!find_friend`", value="This command will personally dm the user, a person who shares simillar interests as them.", inline=False)
  embed.add_field(name="`!find_friends`", value="This command will create a private text channel, with people who best match your interets, where you can chat with them.", inline=False)

  msg_to_pin = await channel.send(embed=embed)
  await msg_to_pin.pin()


@client.command(pass_context = True , aliases=["create_profile", "update_profile"])
async def c_select(ctx):
  embed=discord.Embed(title="To create your profile, answer the following questions:", color=discord.Color.orange())
  await ctx.author.send(embed=embed)
  user_choices = []
  two_choice_question_bank = ["Do you like to read?", "Do you like playing and/or watching sports?", "Are you an early bird?", "Are you a Harry Potter fan?", "Do you bake?", "Are you multilingual?"]
  answers_bank = ["Reading", "Sports", "Waking up early", "Harry Potter", "Baking", "Languages"]
  questionsNum = 0
  for question in two_choice_question_bank:
    choice = answers_bank[questionsNum]
    await ctx.message.author.send(
        question,
        components=[
            Select(
                placeholder="Choose...",
                options=[
                    SelectOption(label="Yes", value=choice),
                    SelectOption(label="No", value="False"),
                ],
                custom_id="select1",
            )
        ],
    )
    
    interaction = await client.wait_for(
      "select_option", check=lambda inter: inter.custom_id == "select1"
    )
    
    await interaction.send(content="Recorded!")
    user_choices.append(interaction.values[0])
    if (questionsNum+1) < len(answers_bank):
      questionsNum+=1



  four_choice_question_bank = ["What is your favorite season?", "What is your favorite household pet?", "Which chore would you rather do?", "What is your favorite way to spend freetime", "What type of music are you into?", "Which superpower would you like to have?", "Which of the following is your favorite social media app?", "What is your favorite entertainment app?"]
  answer_bank = ["Winter", "Summer", "Spring", "Fall", "Dogs", "Cats", "Fishs", "Reptiles", "Washing dishes", "Mowing the lawn", "Cleaning the bathroom", "Vacuuming the house", "Staying indoors", "Going Outdoors", "Spending time with Family/Friends", "Watching movies/tv-shows", "Rock", "Pop", "Jazz", "Classical", "Mind Reading", "Invisibility", "Teleportation", "Flying", "Facebook", "Snapchat", "Instagram", "Twitter", "Netflix", "Tiktok", "Youtube", "Twitch"]

  questionNum = 0
  for question in four_choice_question_bank:
    choice1 = answer_bank[questionNum]
    choice2 = answer_bank[questionNum+1]
    choice3 = answer_bank[questionNum+2]
    choice4 = answer_bank[questionNum+3]
    await ctx.message.author.send(
        question,
        components=[
            Select(
                placeholder="Choose...",
                options=[
                    SelectOption(label=choice1, value=choice1),
                    SelectOption(label=choice2, value=choice2),
                    SelectOption(label=choice3, value=choice3),
                    SelectOption(label=choice4, value=choice4),
                ],
                custom_id="select1",
            )
        ],
    )
    
    interaction = await client.wait_for(
      "select_option", check=lambda inter: inter.custom_id == "select1"
    )
    
    await interaction.send(content="Recorded!")
    user_choices.append(interaction.values[0])
    if (questionNum+4) < len(answer_bank):
      questionNum+=4
  embed=discord.Embed(title="Thank you for creating/updating your profile! You are all set to go!", color=discord.Color.orange())
  await ctx.author.send(embed=embed)
  author_id = str(ctx.message.author) + "_id"
  db[ctx.message.author] = user_choices
  db[author_id] = ctx.message.author.id


@client.command(name="find_friend")
async def person_finder(ctx):
  channel = client.get_channel(int(os.environ['channel_id']))
  keys = db.keys()
  for i in keys:
    val = i
  if str(ctx.message.author) in keys:
    if (len(keys) != 1 and ctx.message.author != val):
      most_similar = ""
      most_answers_in_common = 0
      most_common_interests = ""
      user_data = db[str(ctx.message.author)]
      for key in keys:
        if str(ctx.message.author) != key and "id" not in key:
          answers_in_common = 0
          common_interests = ""
          for answer in range(len(db[key])):
            testing_user = db[key]
            if testing_user[answer] == user_data[answer]:
              answers_in_common+=1
              if testing_user[answer] != "False":
                print(testing_user[answer])
                if common_interests == "":
                  common_interests += testing_user[answer]
                else:
                  common_interests += (", " + testing_user[answer])
          if (answers_in_common > most_answers_in_common):
            most_answers_in_common = answers_in_common
            most_similar = key
            most_common_interests = common_interests

      
      percentage = (most_answers_in_common / len(db[str(ctx.message.author)])) * 100
      
      embed=discord.Embed(title="You should get in touch with `@{}`".format(most_similar), description="{}% of your interests are alike!".format(round(percentage,2)), color=0xFBFF00)
      print(most_common_interests)
      ##embed.add_field(name="You both: ", value=most_common_interests, inline=False)
      await ctx.message.author.send(embed=embed)
      
      
    else:
      await channel.send("Sorry, but no one else has created a profile :(")
  else:
    await channel.send("Please create your profile first")
  
@client.command(name="find_friends", pass_context=True)
async def friends_finder(ctx):
  percentages_2 = {}
  channel = client.get_channel(int(os.environ['channel_id']))
  keys = db.keys()
  member = ctx.author
  author = str(ctx.message.author)


  if author in keys:
    author_info = list(db[author])
    for key in keys:
      if str(key) != author and "id" not in key:
        percentages_2[compare(author_info, db[key])] = key
    dictionary_items = percentages_2.items()
    sorted_items = sorted(dictionary_items)

    people = get_people(sorted_items)

    names = "Private channel "

    guild = ctx.guild

    overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      member: discord.PermissionOverwrite(read_messages=True)
    }

    channel = await guild.create_text_channel(names, overwrites=overwrites)
    embed=discord.Embed(title="Welcome!", color=discord.Color.red())
    embed.add_field(name=" You can converse with your new friends here!", value="The people in this private channel are:", inline=False)
    await channel.send(embed=embed)
    for person in people:
      await channel.send("`" + person + "`")
    await channel.send("`" + author + "`")
    invite = await channel.create_invite()
    
    embed=discord.Embed(title="Click on the invite below to find your new friends!", color=discord.Color.purple())
    
    await ctx.message.author.send(embed=embed)
    await ctx.message.author.send(invite)

    for key in keys:
      if "id" in key: 
        copy = key
        person = copy.replace("_id", "")
        if person in people:
          user = await client.get_user_info(user_id=int(db[key]))
          embed=discord.Embed(title="Want to meet some new people? If so click on the invite below!", color=discord.Color.purple())
          await client.send_message(user, embed=embed)
          await client.send_message(user, invite)
  else:
    await channel.send("Please create your profile first")

@client.command(name="delete_profile")
async def deleter(ctx):
  try:
    del db[str(ctx.message.author)]
    del db[str(ctx.message.author) + "_id"]
    await ctx.send("Your profile has been successfully deleted!")
  except:
    await ctx.send("Sorry, no profile exists for you.")

keep_running()
client.run(os.environ['TOKENS'])
