from calendar import c
import discord
from discord.ext import commands
import requests 
import json 

# Server ID to copy paste 
# 1014614022231961600 Discrete Math 
# 1012190919589646358 Compsci 112


description = '''Juniper's commands!!!'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='?', description=description, intents=intents)


@client.event #this woorks no matter what runs so event isn't affected by the amount of commands etc 
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})') #print sou Junipr#6092434246098 or something along the lines of that and the user ID 
    print('Juniper is ready!')
    channel = client.get_channel( 711341537942044715 ) 
    await channel.send( "I'm online!" ) 

@client.event 
async def on_member_join( member ): 
    print( f'{member.mention} joined {discord.utils.format_dt(member.joined_at)}')

# when creating a command we can have an unidentified number of arguments by doing <name>( ctx, *arg ) 
# when wanting to merge all arguments into one arg we do <name>( ctx, *, arg ) 

"""
@client.command() 
async def changeExamGrade(ctx, key: int, arg: int) :  


@client.command() 
async def gradeSimulation( ctx, key: int, arg: int, arg2: int ): 

@client.command() 
async def getGrade( ctx, arg ): 
"""
class Grade():
    members = [] 
    members_gradebooks = [] 
    current_assignments = []
    channels = [] 
    Courses = []
    categories = [] 


"""
personal notes to make before I start redoing everything
we're going to be having a big array and it's going to be based on the names of the user that called upon Gradebook 
    - first nested array will consist of courses 
    - within the courses will contain weights 
    - within the weights will contain the actual points and the total points 
    we'll navigate through this through index system 
"""        

@client.command() 
async def createGradebook( ctx, *arg ): 
    """ creates a Gradebook for the member """
    name = ctx.author 
    if not arg : 
        await name.send( "please retry again with the fromat ?createGradebook <course1> <course2> ... " )
        return 
    if name in Grade.members : 
        await ctx.send( "you already have a Gradebook!" ) 
    else : 
        Grade.members.append( name ) 
        Grade.members_gradebooks.append( [] ) # adding the courses into the the gradebook dedicated soley to that member 
        Grade.channels.append( [] ) 
        Grade.categories.append( [] ) 
        Grade.current_assignments.append( [] ) 
        Grade.Courses.append( [] ) 
        key = Grade.members.index( name ) 
        guild = ctx.guild
        overwrites = { 
            guild.default_role: discord.PermissionOverwrite( view_channel = False ), 
            ctx.author: discord.PermissionOverwrite( view_channel = True ) 
        }
        category = await guild.create_category( '🔒' + str(name) , overwrites = overwrites )
        survey = await category.create_text_channel( 'Survey' ) 
        for Course_Names in arg : 
            Grade.members_gradebooks[key].append( [] ) # determined by amount of courses 
            Grade.current_assignments[key].append( [] ) # determined by amount of courses
            Grade.categories[key].append( [] ) # determined by amount of courses
            Grade.Courses[key].append( Course_Names ) 
            Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ].append( [] ) # 0 will be dedicated for actual points 
            Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ].append( [] ) # 1 will be dedicated for total points 
            Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ].append( [] ) # 2 will be decidated for names 
            Grade.current_assignments[key][Grade.Courses[key].index( Course_Names )].append( [] ) # 0 is the name of the assignment 
            Grade.current_assignments[key][Grade.Courses[key].index( Course_Names )].append( [] ) # 1 is the date of the assignment 
            Grade.current_assignments[key][Grade.Courses[key].index( Course_Names )].append( [] ) # 2 is the category associated to the assignment (will not be used for final calculation) 
            Grade.categories[key][Grade.Courses[key].index( Course_Names ) ].append( [] ) # 0 will be dedicated to the name 
            Grade.categories[key][Grade.Courses[key].index( Course_Names ) ].append( [] ) # 1 will be dedicated to the value 
            await survey.send( f"How many assignment groups are there for {Course_Names} ex: test, hw, lab, etc.")
            def check(m): 
                return m.author == ctx.author and m.channel == survey
            msg = await client.wait_for( 'message', check = check )
            num = int( msg.content ) 
            for x in range( num ) : 
                await survey.send( f"Group {x + 1}\'s name: " ) 
                msg2 = await client.wait_for( 'message', check = check ) 
                Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ][0].append( [] ) # this will be the list of actual points associated to each cateogry 
                Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ][1].append( [] ) # this will be the list of total points associated to the category 
                Grade.members_gradebooks[key][Grade.Courses[key].index( Course_Names ) ][2].append( [] ) # this will be the list of names associated to the category 
                Grade.categories[key][Grade.Courses[key].index( Course_Names ) ][0].append( msg2.content ) # categories[key][course] will go through all the category names 
                await survey.send( f"{msg2.content}\'s weight by percentage: " )
                msg3 = await client.wait_for( 'message', check = check )   
                Grade.categories[key][Grade.Courses[key].index( Course_Names )][1].append( int(msg3.content)) #create 2 lists 
                sum_of_numbers = sum( Grade.categories[key][Grade.Courses[key].index( Course_Names ) ][1] ) 
                await survey.send( f"weight percentage at: {sum_of_numbers} ")
            check = sum( Grade.categories[key][Grade.Courses[key].index( Course_Names ) ][1] ) 
            if  check != 100 : 
                await ctx.send( "total amount of weights doesn't match up" ) 
                return 
        await survey.delete()  
        currenthw = await guild.create_text_channel( name = 'Current_Assignments', category = category , topic = 'List of assignments or exams due' ) # this will be all the 1's
        ExamScores = await guild.create_text_channel( name = 'Scores', category = category, topic = 'List of Scores for all assignment groups' ) # this will be all the 2's
        OverallGrade = await guild.create_text_channel( name = 'Grade', category = category, topic = 'Overall Grade' ) # this will be all the 3's 
        Grade.channels[key].append( currenthw ) 
        Grade.channels[key].append( ExamScores ) 
        Grade.channels[key].append( OverallGrade ) 
        for Course_Names in arg : 
            embed2 = discord.Embed( title = f"{Course_Names}\'s Scores", color = discord.Colour.random() ) 
            embed3 = discord.Embed( title = f"{Course_Names}\'s grade", color = discord.Colour.random() ) 
            await ExamScores.send( embed = embed2 ) 
            await OverallGrade.send( embed = embed3 )  
        await name.send( f'I have created a Gradebook for you at **{guild}**! \n\n Here are the methods that you can use \n?addAssignment <course_name> <category> <name of the homework> <total points> <date> <- this is for all assignments including homework, exmas, etc !\nex: ?addAssignment science lab lab01 10 09/03/22\n?gradeAssignment <course_name> <category> < name > <actual points> \nkeep in mind that category is word sensitive so put in the category like how you put it in during the survey! \n\nif you need a list of categories then do ?getCategories <course_name> \n\nI\'ll be implementing alert system later, but until then enjoy!' )
# finished all the way here 
# tomorrow redo all the commands using the new lists         

""" 
This bot will later on send a message to the user on how to use it 
it wil contain 
- commands that the user can use 
    - parameters 
    - functionality 


Grade.members_gradebooks[key][course_name index][cateogry_name index][0 for name, 1 for value, 2 to add in points][** IF 2 IS CALLED ** 0 for actual points, 1 for total points, 2 for name ] 
Grade.current_assignments[key][Courses.index][ 0 for name 1 for date ]

msg.embeds[#] 

0 is the most recent 
and the later numbers are after 

for this example we're going to be looking at the course Names but instead of seeing if it contains the name 
we can do the course number 
all channels are going to have embeds based on the order of Course_Names so we can call upon the course 
"""
@client.command() # this will change the embed in current homework 
async def addAssignment( ctx, course_name, category, name, total_points: int, date): 
    """ adds an assignment to the homework """
    user_name = ctx.author
    key = Grade.members.index( user_name ) 
    course = Grade.Courses[key].index( course_name ) 
    category_index = Grade.categories[key][course][0].index( category ) 
    Grade.current_assignments[key][course][0].append( name ) 
    Grade.current_assignments[key][course][1].append( date ) 
    Grade.members_gradebooks[key][course][1][category_index].append( total_points ) 
    Grade.members_gradebooks[key][course][2][category_index].append( name ) 
    Grade.current_assignments[key][course][2].append( category ) 
    embed = discord.Embed( title = "Current Assignments" , color = discord.Colour.random() )
    for i in Grade.Courses[key] : 
        course_key = Grade.Courses[key].index( i ) 
        for names in Grade.current_assignments[key][course_key][0] : 
            common_index = Grade.current_assignments[key][course_key][0].index( names ) 
            embed.add_field( name = Grade.current_assignments[key][course_key][0][common_index] , value = '\u200b', inline = True ) 
            embed.add_field( name = Grade.current_assignments[key][course_key][1][common_index] , value = '\u200b', inline = True ) 
            embed.add_field( name = Grade.current_assignments[key][course_key][2][common_index] , value = '\u200b', inline = True ) 
    await ctx.send( "list updated!" ) 
    channel = Grade.channels[key][0]
    await channel.purge( limit = 2 ) 
    await channel.send( embed = embed ) 
    
@client.command() # this will change the embed in the Grade channel and Scores 
async def gradeAssignment( ctx, course_name, category, name, actual_points: int  ): 
    """ adds in the actual grade to the gradebook """
    user_name = ctx.author 
    key = Grade.members.index( user_name ) 
    course = Grade.Courses[key].index( course_name ) 
    category_index = Grade.categories[key][course][0].index( category ) 
    if Grade.current_assignments[key][course][0].__contains__( name ) == False : 
        await ctx.send( "please enter a valid name" ) 
        return 
    final_index = Grade.current_assignments[key][course][0].index( name )
    Grade.current_assignments[key][course][0].remove( Grade.current_assignments[key][course][0][final_index])
    Grade.current_assignments[key][course][1].remove( Grade.current_assignments[key][course][1][final_index]) 
    Grade.current_assignments[key][course][2].remove( Grade.current_assignments[key][course][2][final_index]) 
    Grade.members_gradebooks[key][course][0][category_index].append( actual_points ) 
    channel = Grade.channels[key][1] 
    channel2 = Grade.channels[key][2] 
    channel3 = Grade.channels[key][0] 
    embed = discord.Embed( title = "Scores" , color = discord.Colour.random() )
    embed2 = discord.Embed( title = "Grades" , color = discord.Colour.random() ) 
    embed3 = discord.Embed( title = "Current Assignments" , color = discord.Colour.random() ) 
    for i in Grade.Courses[key] : 
        course_key = Grade.Courses[key].index( i ) 
        for names in Grade.current_assignments[key][course_key][0] : 
            common_index = Grade.current_assignments[key][course_key][0].index( names ) 
            embed3.add_field( name = Grade.current_assignments[key][course_key][0][common_index] , value = '\u200b', inline = True ) 
            embed3.add_field( name = Grade.current_assignments[key][course_key][1][common_index] , value = '\u200b', inline = True ) 
            embed3.add_field( name = Grade.current_assignments[key][course_key][2][common_index] , value = '\u200b', inline = True )  
    weight = 0 
    final_score = 0 
    for c in Grade.Courses[key] : 
        index1 = Grade.Courses[key].index( c )  
        for weights in Grade.categories[key][index1][1] : 
            weights_index = Grade.categories[key][index1][1].index( weights ) 
            if Grade.members_gradebooks[key][index1][0][weights_index] : 
                continue 
            else : 
                weight += Grade.categories[key][index1][1][weights_index] 
    for a in Grade.Courses[key] : 
        actual_points_combined = 0 
        total_points_combined = 0
        index2 = Grade.Courses[key].index( a ) 
        for b in Grade.categories[key][index2][1] : 
            weight_index = Grade.categories[key][index2][1].index( b ) 
            for e in Grade.members_gradebooks[key][index2][0][weight_index] :
                index3 = Grade.members_gradebooks[key][index2][0][weight_index].index( e ) 
                actual_points_combined += Grade.members_gradebooks[key][index2][0][weight_index][index3] 
                total_points_combined += Grade.members_gradebooks[key][index2][1][weight_index][index3] 
                if not Grade.members_gradebooks[key][index2][0][weight_index][index3] or Grade.members_gradebooks[key][index2][1][weight_index][index3] :
                    final_score += Grade.categories[key][index2][1][weight_index] 
                else : 
                    final_score += float( actual_points_combined / total_points_combined ) * Grade.categories[key][index2][1][weight_index]
        embed2.add_field( name = f"**{Grade.Courses[key][index2]}**" , value = str(final_score), inline = False ) 
        final_score = 0  
    # score should be similar to current assignments but has assignment_name actual_points total_points 
    for courses in Grade.Courses[key] : 
        courses_index = Grade.Courses[key].index( courses ) 
        for categories in Grade.categories[key][courses_index][0] : 
            categories_index = Grade.categories[key][courses_index][0].index( categories )
            for names in Grade.members_gradebooks[key][courses_index][2][categories_index] : 
                names_index = Grade.members_gradebooks[key][courses_index][2][categories_index].index( names ) 
                title = Grade.members_gradebooks[key][courses_index][2][categories_index][names_index] 
                if Grade.members_gradebooks[key][courses_index][0][categories_index] :     
                    actual_point = Grade.members_gradebooks[key][courses_index][0][categories_index][names_index] 
                    total_point = Grade.members_gradebooks[key][courses_index][1][categories_index][names_index] 
                    embed.add_field( name = str(title) , value = str(categories) , inline = True )
                    embed.add_field( name = str( actual_point), value = '\u200b' , inline = True )
                    embed.add_field( name = str( total_point ), value = '\u200b' , inline = True ) 
                else : 
                    continue
    await channel.purge( limit = 2 )  
    await channel2.purge( limit = 2 ) 
    await channel3.purge( limit = 2 ) 
    await channel.send( embed = embed ) #score
    await channel2.send( embed = embed2 ) #grades
    await channel3.send( embed = embed3 ) #currenthw

#Grade.members_gradebooks[key][course_name index][cateogry_name index][0 for name, 1 for value, 2 to add in points][** IF 2 IS CALLED ** 0 for actual points, 1 for total points, 2 for name ] 

@client.command() 
async def getCategories( ctx, course_name ): 
    message = "" 
    name = ctx.author
    key = Grade.members.index( name ) 
    index = Grade.Courses[key].index( course_name ) 
    for i in Grade.categories[key][index][0] : 
        message += i 
    await ctx.send( message ) 

@client.command() #DONT DELETE THIS USE FOR LATER 
async def test(ctx) :   
    username = ctx.author 
    key = Grade.members.index( username ) 
    for i in Grade.current_assignments[key] : 
        index1 = Grade.current_assignments[key].index( i ) 
        for j in Grade.current_assignments[key][index1] : 
            index2 = Grade.current_assignments[key][index1].index( j ) 
            for h in Grade.current_assignments[key][index1][index2] : 
                index3 = Grade.current_assignments[key][index1][index2].index( h ) 
                await ctx.send( Grade.current_assignments[key][index1][index2][index3]  + str(index1) + str(index2) + str(index3)) 

#@client.command()
#async def reset( ctx, arg ): 
    

#WHAT TO ADD 
# ?addGrade 
# ?calculate grade 
# @client.command() 
# async def addGrade( ctx,  ) 


@client.command()
async def add(ctx, left: int, right: int): # so if I run ?add 3 7 then it will run as intended and give me 10 
    """Adds two numbers together."""
    await ctx.send(left + right)


@client.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@client.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# This is for when I'm going to start inputting the help function where if someone presses help then it's going to send a dm me
# the user, message on what they need help on, and what server 
# @client.command(pass_context=True)
# async def getguild(ctx):
# id = ctx.message.guild.id
#main purpose of this is to add categories for people's grades / planner on discord (when making this public) 

class Wordle() : 
    users = [] 
    channels = [] 

@client.command() 
async def Wordle(ctx) : 
    author = ctx.author 
    if author not in Wordle.users : 
        guild = ctx.guild 
        overwrites = { 
            guild.default_role: discord.PermissionOverwrite( view_channel = False ), 
            ctx.author: discord.PermissionOverwrite( view_channel = True ) 
        }
        category = await guild.create_category( f"{author}'s Wordle!", overwrites = overwrites ) 
        channel = await category.create_text_channel('Guess here!') 
        Wordle.channels.append(channel) 
        Wordle.users.append(author) 
    channel = Wordle.channels.index(Wordle.users.get(author)) 
    channel.send()

@client.command() 
async def listOfcommands( ctx ): 
    """ a list of commands but specify how to call upon the command """
    channel = ctx.channel 
    message = "**.?add # #** \n **.?addCategories # <string>** \n **.?joined @ member** \n **.?repeat # String ** \n **.?bulkdelte #** \n **.?addhw # <string>** \n **.?test** \n **reset** \n **word commands** \n **- hi Juniper!** \n **-@ Juniper#0759 :heart:** "
    await channel.send( message )

@client.command() 
async def bulkdelete( ctx, times: int ):
    """ bulk deletes messages from channel """
    channel = ctx.channel 
    await channel.purge(limit=times)
# currently only prints out the first input      

@client.command() 
async def AItest1(ctx) : 
    name = ctx.author 
    if name not in AItest1.users : 
        guild = ctx.guild
        overwrites = { 
            guild.default_role: discord.PermissionOverwrite( view_channel = False ), 
            ctx.author: discord.PermissionOverwrite( view_channel = True ) 
        }
        category = await guild.create_category( f"understanding {ctx.author}", overwrites = overwrites )
        tests = await category.create_text_channel( 'test' ) 
        AItest1.channel.append(tests) 
        AItest1.users.append(name) 
    channel = AItest1.channel[AItest1.users.index(name)]
    current_answers = [[],[],[],[],[],[]] 
    index = 0 
    for questions in AItest1.basic_convo : 
        await channel.send(questions) 
        def check(m) : 
            return m.author == ctx.author and m.channel == channel 
        msg = await client.wait_for('message', check = check) 
        current_answers[index].append(msg) 
        index += 1
    AItest1.check(current_answers) 
    ctx.send("thank you for the daily survey") 

@client.command() 
async def AIresponse1(ctx) : 
    name = ctx.author 
    

class AItest1():  
    users = [] 
    channel = [] 
    basic_convo = ["Hello", "how are you feeling?", "why?", "what are you doing?", "is it interesting?", "what are your plans for today?" ] 
    previous_answers = [[],[],[],[],[],[]]         
    
    def check(current_answers): 
        array_index = 0
        for question in AItest1.previous_answers :
            for previous_answer in question : 
                count = 0 
                str = current_answers[array_index][0]
                for letter in previous_answer : 
                    letter_index = previous_answer.index(letter) 
                    if str[letter_index] == letter : 
                        count += 1
                if count < (len(previous_answer) / 2) : 
                    question.append(str) 
            array_index += 1

@client.event 
async def on_message( message ):
    if message.content.startswith( 'Hi Juniper!' ):     
        await message.reply( 'Hello!', mention_author = True )
    if client.user.mentioned_in( message ): 
        if 'what\'s the current weather in' in message.content :
            # city will be named substring 29 and on 
            newmessage = message.content
            city = newmessage[ 53 : ]
            city_nows = "" 
            lst = [] 
            for letter in city: 
                lst.append( letter ) 
            for letters in lst : 
                if letters != " " : 
                    city_nows = city_nows + letters 
                else :
                    city_nows = city_nows + "%20"
            geo_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_nows + ",US-CA,840&limit=1&appid=a4540734ce6addba418ba65e71f080c5"   
            geo_response = requests.get( geo_url ) 
            geo_json = geo_response.json() 
            lat = geo_json[0]["lat"] 
            lon = geo_json[0]["lon"] 
            url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=a4540734ce6addba418ba65e71f080c5"
            response = requests.get( url ) 
            api_response = response.json() 
            if api_response["cod"] == "404" : 
                message.reply( "city not found." )
            x = api_response["main"] 
            get_temp = x["temp"]
            get_tempmin = x["temp_min"] 
            get_tempmax = x["temp_max"] 
            current_temp_Celsius = get_temp - 273.15 
            current_temp = str(round( current_temp_Celsius * 1.8 ) + 32)
            temp_min_Celsius = get_tempmin - 273.15 
            temp_max_Celsius = get_tempmax - 273.15 
            temp_min = str(round( temp_min_Celsius * 1.8 ) + 32 ) 
            temp_max = str(round( temp_max_Celsius * 1.8 ) + 32 )
            # temp min and temp max is going to be added notes to myself 
            current_humidity = x["humidity"] 
            y = api_response["weather"] 
            weather_description = y[0]["description"] 
            embed = discord.Embed( title = f"Weather in {city}", color = 665599)
            embed.add_field( name = "Description", value  = f"**{weather_description}**", inline = False ) 
            embed.add_field( name = "Temperature", value = f"**{current_temp}**", inline = False )
            embed.add_field( name = "Humidity", value = f"**{current_humidity}**", inline = False ) 
            embed.add_field( name = "Temp Max", value = f"**{temp_max}**", inline = False )
            embed.add_field( name = "Temp Min", value = f"**{temp_min}**", inline = False ) 
            embed.set_thumbnail( url = "https://i.ibb.co/CMrsxdX/weather.png")
            await message.reply( embed=embed ) # the first embed is  a keyword like content the second embed is the embed we set up
                
        if '❤️' in message.content : 
            await message.reply( '🥰' )    
    await client.process_commands(message)

client.run('MTAxODQyMDcyMzU1NzA4OTM3MA.GYqPoV.zk7y6LMvA0mxpSaLEd6jxDbRleXNvcRxIdZ8Vw')