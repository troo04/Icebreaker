import os
import discord
from server import keep_running
from discord_components import ComponentsBot, Select, SelectOption
from replit import db

intents = discord.Intents.default()
intents.members = True


client = ComponentsBot("!", intents=intents)


@client.event
async def on_member_join(member):
  channel = client.get_channel(int(os.environ['channel_id']))
  embed=discord.Embed(title="Type `!create_profile` to get started!", color=discord.Color.blue())
  await channel.send(f'Welcome <@{member.id}>!\n')
  await channel.send(embed=embed)


@client.event
async def on_ready():
  channel = client.get_channel(int(os.environ['channel_id']))
  print('{0.user} is online'.format(client))

  embed=discord.Embed(title="Commands:")
  embed.add_field(name="`!create_profile`", value="Allows the user to set up a profile for themselves\n", inline=False)
  embed.add_field(name="`!update_profile`", value="The user can update their profile, if they wish to.", inline=False)
  embed.add_field(name="`!delete_profile`", value="This command will delete the user's profile.", inline=False)
  embed.add_field(name="`!find`", value="This command will personally dm the user, a person who shares simillar interests as them.", inline=False)

  msg_to_pin = await channel.send(embed=embed)
  await msg_to_pin.pin()


@client.command(pass_context = True , aliases=["create_profile", "update_profile"])
async def c_select(ctx):
  embed=discord.Embed(title="To create your profile, answer the following questions:", color=discord.Color.orange())
  await ctx.author.send(embed=embed)
  user_choices = []
  two_choice_question_bank = ["Do you like to read?", "Do you like playing or watching sports?", "Do you believe in aliens?", "Do you consider yourself afraid of the dark?", "Have you ever met a celebrity?", "Are you a Harry Potter fan?", "Do you bake?", "Do you speak more than one language?"]
  for question in two_choice_question_bank:
    await ctx.message.author.send(
        question,
        components=[
            Select(
                placeholder="Choose...",
                options=[
                    SelectOption(label="Yes", value=True),
                    SelectOption(label="No", value=False),
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



  four_choice_question_bank = ["What is your favorite season?", "What is your favorite household pet?", "Which would you rather do?", "What is your favorite way to spend freetime", "What type of music are you into?"]
  answer_bank = ["Winter", "Summer", "Spring", "Fall", "Dog", "Cat", "Fish", "Reptile", "Wash dishes", "Mow the lawn", "Clean the bathroom", "Vacuum the house", "Stay indoors", "Go Outdoors", "Spend time with Family/Friends", "Watch movies/tv-shows", "Rock", "Pop", "Jazz", "Classical"]

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
                    SelectOption(label=choice1, value=1),
                    SelectOption(label=choice2, value=2),
                    SelectOption(label=choice3, value=3),
                    SelectOption(label=choice4, value=4),
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
  db[ctx.message.author] = user_choices
  print(user_choices)
  print(db.keys())


@client.command(name="find")
async def similarity_Finder(ctx):
  channel = client.get_channel(int(os.environ['channel_id']))
  keys = db.keys()
  for i in keys:
    val = i
  if len(keys) != 1 and ctx.message.author != val:
    if (str(ctx.message.author) in keys):
      most_similar = ""
      most_answers_in_common = 0
      user_data = db[str(ctx.message.author)]
      for key in keys:
        if str(ctx.message.author) != key:
          answers_in_common = 0
          for answer in range(len(db[key])):
            testing_user = db[key]
            if testing_user[answer] == user_data[answer]:
              answers_in_common+=1
          if (answers_in_common > most_answers_in_common):
            most_answers_in_common = answers_in_common
            most_similar = key

      
      percentage = (most_answers_in_common / len(db[str(ctx.message.author)])) * 100
      
      embed=discord.Embed(title="You should get in touch with `@{}`".format(most_similar), description="{}% of your interests are alike!".format(round(percentage,2)), color=0xFBFF00)

      await ctx.message.author.send(embed = embed)
    else:
      await channel.send("Please create your profile first")
  else:
    await channel.send("Sorry, but no one else has created a profile :(")
    
    
@client.command(name="delete_profile")
async def deleter(ctx):
  try:
    del db[str(ctx.message.author)]
    await ctx.send("Your profile has been successfully deleted!")
  except:
    await ctx.send("Sorry, no profile exists for you.")

keep_running()
client.run(os.environ['TOKENS'])
