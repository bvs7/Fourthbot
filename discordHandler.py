import sys
import os
import json
import discord


class DiscordHandler:
    def __init__(self, config_filename):
        if not os.path.exists(config_filename):
            print("Config File not found.")
            return
        else:
            with open(config_filename,'rb') as config_file:
                self.config = json.load(config_file)
        self.client = discord.Client()
        @self.client.event
        async def on_ready():
            print(self.client.user.name + ' is now online!')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            else:
                self.parse(message)
    def parse(self, message):
        print('Message received:')
        print(message.content)
    def run(self):
        self.client.run(self.config['token'])

if __name__ == '__main__':
    D = DiscordHandler('config\discord.json')
    D.run()