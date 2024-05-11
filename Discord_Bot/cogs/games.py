import asyncio
import discord
from discord.ext import commands
from captcha.image import ImageCaptcha
import random
import string
import os


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_scores = {}
        self.captcha_texts = {}
        self.Game_Going_On = False
        self.questions = [
            {"question": "Question 1?", "answer": "Answer 1"},
            {"question": "Question 2?", "answer": "Answer 2"},
            {"question": "Question 3?", "answer": "Answer 3"},
            {"question": "Question 4?", "answer": "Answer 4"},
            {"question": "Question 5?", "answer": "Answer 5"},
        ]
        #self.hidden_message = "https://www.youtube.com/watch?v=Fqo-vzP8aco"
        self.hidden_message = "tblhy://nwj.baclmhv.cbp/iilun?m=Fdr-hhH8sif"
        
        
    
    @commands.command(
        aliases=["g"],
        help="This is games command",
        description="Commands for games",        
        enabled=True,
        hidden=False
    )
    async def games(self, ctx):
        if self.Game_Going_On:
            await ctx.send("Complete ongoing game!")
            return

        self.Game_Going_On = True      

        try:
            self.player_scores[ctx.author.id] = 0
            await ctx.send("Let's start the game!")

            # Generate a captcha image
            image_captcha = ImageCaptcha()

            # Generate a random string of 20 alphanumeric characters
            captcha_text = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

            data = image_captcha.generate(captcha_text)
            image_captcha.write(captcha_text, 'captcha.png')

            # Store the captcha text
            self.captcha_texts[ctx.author.id] = captcha_text

            await ctx.send(self.questions[0]["question"])
            await ctx.send(file=discord.File('captcha.png'))  # corrected line
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(
        aliases=["a"],
        help="This is answer command",
        description="Commands for answer the question from games",        
        enabled=True,
        hidden=False
    )
    async def answer(self, ctx, *, player_answer):
        try:
            if self.player_scores[ctx.author.id] < len(self.questions):
                # Compare the player's answer with the stored captcha text
                if player_answer == self.captcha_texts[ctx.author.id]:
                    self.player_scores[ctx.author.id] += 1
                    if self.player_scores[ctx.author.id] < len(self.questions):
                        await ctx.send("Correct! Moving to the next question.")

                        # Generate a new captcha image for the next question
                        image_captcha = ImageCaptcha()
                        captcha_text = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
                        data = image_captcha.generate(captcha_text)
                        image_captcha.write(captcha_text, 'captcha.png')

                        # Store the new captcha text
                        self.captcha_texts[ctx.author.id] = captcha_text
                        await ctx.send(self.questions[self.player_scores[ctx.author.id]]["question"])
                        await ctx.send(file=discord.File('captcha.png'))  # send the new captcha image
                    else:
                        await ctx.send("Congratulations, you've answered all questions correctly!")
                        asyncio.sleep(5)
                        await ctx.send("Here is your reward: " + self.hidden_message)
                else:
                    self.player_scores[ctx.author.id] = 0
                    await ctx.send("Incorrect answer, let's start over.")
                    await ctx.send("This hint might help: tblhy://nwj.baclmhv.cbp/iilun?m=dDz4i9EyPiH")
                    await ctx.send("Please type '>games' to start over.")
                    await ctx.send("Good luck at the next attempt!")
                    self.Game_Going_On = False
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            self.Game_Going_On = False

async def setup(bot):
    await bot.add_cog(Games(bot))