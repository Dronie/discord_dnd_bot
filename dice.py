# dice.py
import os

import numpy as np
import re
import operator

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


#current_save = 1000

# ops dictionary, used to apply approriate operations for subsequent terms
ops = { "+": operator.add, "-": operator.sub }

permissions = {
    0 : ('Admin'),
    1 : ('DM'),
    2 : ('Player')
}

securities = {
    'fumble' : (1),
    'set_save' : (1),
    'display_initiative_order' : (1),
    'roll' : (2),
    'save' : (2),
    'erdric_help' : (2),
    'initiative' : (2)
}

emo_table = { "str": ("Strength", ":Strength_Success:", ":Strength_Fail:"), 
              "dex": ("Dexterity", ":Dexterity_Success:", ":Dexterity_Fail:"),
              "con": ("Constitution", ":Constitution_Success:", ":Constitution_Fail:"),
              "int": ("Intelligence", ":Intelligence_Success:", ":Intelligence_Fail:"),
              "wis": ("Wisdom", ":Wisdom_Success:", ":Wisdom_Fail:"),
              "cha": ("Charisma", ":Charisma_Success:", ":Charisma_Fail:")}



class DiceRollClient(discord.Client):
    def __init__(self):
        super().__init__()

        self.bot = commands.Bot(command_prefix='?')

        self.roll = self.bot.command(name='/')(self.roll)
        self.save = self.bot.command(name='t')(self.save)
        self.set_save = self.bot.command(name='#')(self.set_save)
        self.fumble = self.bot.command(name='f')(self.fumble)
        self.erdric_help = self.bot.command(name='h')(self.erdric_help)
        self.initiative = self.bot.command(name='i')(self.initiative)
        self.display_initiative_order = self.bot.command(name='di')(self.display_initiative_order)
    
    def generate_report(self, ctx):
        print("Author: " + str(ctx.message.author))
        print("  Content: " + ctx.message.content + "\n")

    def has_permission(self, permission, security):
        if int(permission) <= security:
            return True
        else:
            return False
    
    def get_permission(self, person):
        permission = ''

        with open('permissions.txt', 'r') as f:
            for line in f:
                if str(person) in line:
                    permission = line.split('|')[1]

        if not permission:
            with open('permissions.txt', 'a') as f:
                f.write(f'{str(person)} | 2')
                permission = '2'
                print(permission)
        
        return permission

    def get_permission_msg(self, permission, security):
        return (f'**Oops!**\n :no_entry_sign: It seems you don\'t have permission to use that command! :no_entry_sign: \n'
                f'Only a **{permissions[security]}** or above can use that command and you are a **{permissions[permission]}**\n'
                f'Maybe if you give Erdric a **backrub** he\'ll promote you!'
        )

    def process_roll_msg(self, message):
        roll = message.content[3:]
        roll_tokens = re.split(r'\W+', roll)
        roll_signs = []
        for i in roll:
            if i == '-' or i == '+':
                roll_signs.append(i)
        
        return roll_tokens, roll_signs
    
    def get_error_msg(self, message, exception):

        if exception == 'np':
            exception = 'Permission Denied'

        print(' ----- ERROR ----- \n')
        print(f'  Author: {str(message.author)}')
        print(f'  Content: {message.content}\n')
        print('  Error output:')
        print(f'    {str(exception)}\n')
        print(' ----------------- \n')

        return (
            f'**Oops**!\nThe following command seems to have'
            f':skull_crossbones: **disrupted** :skull_crossbones:'
            f'the chance cubes\' magic:\n \n    `{ message.content }`\n'
            f'\n<@{ str(message.author.id) }>, you better get Erdric to :sparkles:'
            f'**re-enchant** :sparkles: them for you!'
        )

    def stringify(self, roll, min = 1, max = 20, use_bold=False):
        # stringify takes a list as input and formats it
        # into an 'Innkeeper-like' string, ready to send in chat
            roll_as_string = '('

            last_roll = roll[-1]

            roll = roll[:-1]

            if use_bold:
                for i in roll:
                    if int(i) == min or int(i) == max:
                        roll_as_string += '**' + str(int(i)) + '**, '
                    else:
                        roll_as_string += str(int(i)) + ', '
                
                if int(last_roll) == min or int(last_roll) == max:
                    last_roll = '**' + str(int(last_roll)) + '**'
                else:
                    last_roll = str(int(last_roll))
                
                roll_as_string += last_roll
                    
            else:
                for i in roll:
                    roll_as_string += str(int(i)) + ', '
                roll_as_string += str(int(last_roll))

            roll_as_string += ')'

            return roll_as_string
    
    async def fumble(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['fumble']):
            roll = np.random.randint(1, 101)
            print(roll)
            response = self.get_fumble(roll)
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['fumble']))


    def get_fumble(self, roll, space='|   '):
        if roll < 11:
            return '**Embarrassed**. No effect'
        elif roll < 21:
            return '**Miss Wide**. Hit a nearby object instead'
        if roll < 31:
            return '**Distracted**. Saving throws have disadvantage and attack rolls against have advantage for 1 round'
        if roll < 41:
            return '**Clumsy**. DC15 Dexterity saving throw or fall prone'
        if roll < 51:
            return '**Very Clumsy**. Fall prone'
        if roll < 61:
            return f'**Twisted Ankle**. Speed is 10 feet for {str(int(np.random.randint(1, 5)))} rounds and Dexterity saving throws have disadantage'
        if roll < 66:
            return '**Stinger**. Incapacitated for 1 round'
        if roll < 71:
            return '**Shell Shock**. Stunned for 1 round'
        if roll < 76:
            return f'**PTSD**. Frightened by all enemies for {str(int(np.random.randint(1, 5)))} rounds'
        if roll < 81:
            return '**Burden**. Hit an ally adjacent to self or target'
        if roll < 91:
            return '**Self-Flagellation**. Hit self'
        if roll < 96:
            return '**Liability**. Critical hit an ally adjacent to self or target'
        if roll < 98:
            return '**Suicide**. Critical hit self'
        if roll < 99:
            return '**Shattered**. Nonmagical weapon breaks, magical weapon loses magical properties for 1 day, or expend all slots'
        if roll < 100:
            return f'**Misfortune**. :poo: Roll fumble table twice\n{ space }1. { self.get_fumble(np.random.randint(1, 101), space="      "+space) }\n{ space }2. { self.get_fumble(np.random.randint(1, 101), space="      "+space) }'
        else:
            return f'**Tragedy**. :skull: Roll fumble table three times\n{ space }1. { self.get_fumble(np.random.randint(1, 101), space="      "+space) }\n{ space }2. { self.get_fumble(np.random.randint(1, 101), space="      "+space) }\n{ space }3. { self.get_fumble(np.random.randint(1, 101), space="      "+space) }'

    async def erdric_help(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['erdric_help']):
            response = '**You see a a frayed square of parchment lying beside a curious pair of glowing cubes.**\n'
            response += '**The parchment is marked with, what you assumed was once black, ink which has now**\n'
            response += '**nearly completely faded into the frayed and disintegrating page**.\n'
            response += '**It reads**:\n \n'
            response += '  To whomever finds themselves upon these cubes,\n'
            response += '    If you are reading this then it can only be that you\'ve\n'
            response += '    stumbled accross my treasured **Magic Cubes of Chance**.\n'
            response += '    How you quite managed to do so is beyond me, but I suppose\n'
            response += '    fair is fair and by the will of the gods of luck - they are *yours to keep*...\n' 
            response += '\n'
            response += '    I shall now detail some instructions for their proper operation,\n'
            response += '    (I recommend you follow these to the letter as I don\'t have the time, patience \n'  
            response += '    or supply of reagents to constantly re-enchant them if you blow yourself up by mistake)\n'  
            response += '\n'
            response += '\n'
            response += '    **COMMANDS**:\n'
            response += '     - \'?h\'..........................This **H**elp Message\n'
            response += '     - \'?/\'..........................Standard Roll\n'
            response += '     - \'?t\'..........................Saving **T**hrow Roll\n'
            response += '     - \'?#\'...........................Set Save DC\n'
            response += '     - \'?f\'...........................**F**umble Roll\n'
            response += '     - \'?i\'...........................**I**nitiative Roll\n'
            response += '     - \'?di\'...........................**D**isplay **I**nitiative Order\n'
            response += '\n'
            response += '\n'
            response += '    If you should encounter any problems whilst using these magical cubes, seek me out as\n'
            response += '    I am ,unfortunately, bound against my will to mend them for you.\n'
            response += '\n'
            response += '  Yours begrudgingly,\n'
            response += '    Erdric, Hero of Phandalin'
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['erdric_help']))

    async def roll(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['roll']):
            response = self.get_roll_message(ctx.message)
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['roll']))
    
    async def save(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['save']):
            response = self.get_save_message(ctx.message)
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['save']))
    
    async def initiative(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['initiative']):
            response = self.get_initiative_roll_message(ctx.message)
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['initiative']))
    
    async def display_initiative_order(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['display_initiative_order']):
            response = self.get_initiative_order_message()
            await ctx.send(response)
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['display_initiative_order']))
    

    def get_initiative_order_message(self):
        players = []
        with open('initiative_order.txt', 'r') as f:
            for line in f:
                name, roll = line.split('|')
                players.append((name, int(roll)))
        sorted_players = players.sort(reverse=True, key=lambda x: x[1])

        response = '**Here is the initiative order from higest to lowest**:\n'
        
        for i in range(0, len(players)):
            response += f'{i+1}. '
            if i == 0:
                response += f':trophy: '
            elif i == len(players) - 1:
                response += f':poo: '
            response += f'{players[i][0]} | {players[i][1]}\n'
        
        return response
    
    def get_initiative_roll_message(self, message):
        roll_tokens, roll_signs = self.process_roll_msg(message)

        initial_dice = roll_tokens[0].split('d')
        additional_tokens = roll_tokens[1:]

        try:
            additional_response, initial_roll, add, sum_add, add_mod = self.process_roll(initial_dice, roll_tokens, roll_signs, additional_tokens)
            
            roll = int(max(initial_roll + add + add_mod))

            initiative = ''
            person_line = ''

            with open('initiative_order.txt', 'r') as f:
                for line in f:
                    if str(message.author.display_name) in line:
                        person_line = line.strip()
                        initiative = line.split('|')[1]

            if not initiative:
                with open('initiative_order.txt', 'a') as f:
                    f.write(f'{str(message.author.display_name)} | {str(roll)}\n')
            else:
                new_file_content = ""
                with open('initiative_order.txt', 'r') as f:
                    for line in f:
                        stripped_line = line.strip()
                        new_line = stripped_line.replace(person_line, f'{str(message.author.display_name)} | {str(roll)}')
                        new_file_content += new_line +"\n"

                writing_file = open('initiative_order.txt', 'w')
                writing_file.write(new_file_content)
                writing_file.close()

            
            return (f'<@{str(message.author.id)}>  :game_die:\n'
                    f'**Result**:  {roll_tokens[0]}  {str(self.stringify(initial_roll, 1, int(initial_dice[1]), use_bold=True))}  {additional_response}'
                    f'\n**Totals**:  :bulb:  { self.stringify(initial_roll + add + add_mod) } [{roll}]'
            )

        except (ValueError, TypeError, IndexError) as ve:
            return self.get_error_msg(message, ve)

    async def set_save(self, ctx):
        self.generate_report(ctx)
        permission = self.get_permission(ctx.message.author)
        if self.has_permission(permission, securities['set_save']):
            try:
                int(ctx.message.content[3:])
                with open("current_save.txt", "w") as f:
                    f.write(ctx.message.content[3:])

                if ctx.message.guild.id == 694868403730776087:
                    channel = ctx.message.guild.get_channel(694869608011661313)
                    await channel.send(':zap:**The DM has prepared a new challenge!**:zap:')
                    #for i in ctx.message.guild.channels:
                    #    print(i, i.id)
                
                else:
                    await ctx.send(':zap:**The DM has prepared a new challenge!**:zap:')

            except (ValueError, TypeError, IndexError) as ve:
                await ctx.send(self.get_error_msg(ctx.message, ve))
        else:
            await ctx.send(self.get_permission_msg(int(permission), securities['set_save']))

    
    def process_roll(self, initial_dice, roll_tokens, roll_signs, additional_tokens):
        add = np.zeros(int(initial_dice[0]))
        sum_add = 0
        add_mod = 0
        response = ''

        initial_roll = np.asarray(np.random.randint(1, int(initial_dice[1])+1, size=int(initial_dice[0])))
        for i in range(0, len(additional_tokens)):
            if 'd' in additional_tokens[i]:
                response += f'{roll_signs[i]}{str(additional_tokens[i])}  '
                tokens_tokens = additional_tokens[i].split('d')
                rand_adds = np.asarray(np.random.randint(1, int(tokens_tokens[1])+1, size=int(tokens_tokens[0])))
                response += f'{self.stringify(rand_adds, 1, int(tokens_tokens[1]), use_bold=True)}[{str(sum(rand_adds))}]  '

                add = ops[roll_signs[i]](add, sum(rand_adds))
                sum_add = ops[roll_signs[i]](sum_add, sum(rand_adds))
            else:
                response += f'{roll_signs[i]}{additional_tokens[i]}  '
                add_mod = ops[roll_signs[i]](add_mod, int(additional_tokens[i])) 
        
        return response, initial_roll, add, sum_add, add_mod

    def get_roll_message(self, message):
        roll_tokens, roll_signs = self.process_roll_msg(message)

        initial_dice = roll_tokens[0].split('d')
        additional_tokens = roll_tokens[1:]

        try:
            additional_response, initial_roll, add, sum_add, add_mod = self.process_roll(initial_dice, roll_tokens, roll_signs, additional_tokens)
            return (f'<@{str(message.author.id)}>  :game_die:\n'
                    f'**Result**:  {roll_tokens[0]}  {str(self.stringify(initial_roll, 1, int(initial_dice[1]), use_bold=True))}  {additional_response}'
                    f'\n**Totals**:  :crossed_swords:  { self.stringify(initial_roll + add + add_mod) }  :boom:  { str(int(sum(initial_roll) + sum_add + add_mod ))}'
            )

        except (ValueError, TypeError, IndexError) as ve:
            return self.get_error_msg(message, ve)
    
    def get_save_message(self, message):
        roll_tokens, roll_signs = self.process_roll_msg(message)

        initial_dice = roll_tokens[0].split('d')
        additional_tokens = roll_tokens[1:]

        try:
            with open("current_save.txt", "r") as f:
                SAVE = f.read()
            
            additional_response, initial_roll, add, sum_add, add_mod = self.process_roll(initial_dice, roll_tokens, roll_signs, additional_tokens)

            if int(sum(initial_roll) + sum_add + add_mod ) > int(SAVE):
                outcome = "\nYou **Succeed** the save!"
            else:
                outcome = "\nYou **Fail** the save!"

            return (f'<@{str(message.author.id)}>  :game_die:\n'
                    f'**Result**:  {roll_tokens[0]}  {str(self.stringify(initial_roll, 1, int(initial_dice[1]), use_bold=True))}  {additional_response}'
                    f'\n**Total**:  :pray:  {str(int(sum(initial_roll) + sum_add + add_mod ))}{outcome}'
            )

        except (ValueError, TypeError, IndexError) as ve:
            return self.get_error_msg(message, ve)

client = DiceRollClient()

client.bot.run(TOKEN)