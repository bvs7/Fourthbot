// FourthBot - Designed for RBaG DnD Group
// Main function will init all code and call different commands

// Get other files
const Discord = require("discord.js")
const config = require("./config.json")

function parse(message_string){
    var args = message_string.split(/\s+/)
    console.log(args)

}

// Init bot
const FourthBot = new Discord.Client()
FourthBot.login(config.token)
FourthBot.on("ready",() => {
    console.log("FourthBot is on!")
})

FourthBot.on("message", (message) =>{
    if(!message.content.startsWith(config.prefix)) return;
    console.log(message.author.tag)
    console.log(message.content)
    parse(message.content)
    if(message.content == `${config.prefix}hi`){
        message.channel.send(`Hi <@${message.author.id}>`)
    }
})

