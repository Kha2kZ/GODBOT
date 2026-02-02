// index.js

const { Client, Intents } = require('discord.js');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});

client.on('guildCreate', async (guild) => {
    const guildId = guild.id;
    const commands = [
        {
            name: 'chat',
            description: 'Chat interaction command',
            options: [{
                name: 'message',
                type: 'STRING',
                description: 'Your message',
                required: true,
            }],
        },
    ];

    const rest = new REST({ version: '9' }).setToken(process.env.DISCORD_BOT_TOKEN);
    try {
        console.log(`Started refreshing application (/) commands for guild: ${guild.name}`);
        await rest.put(Routes.applicationGuildCommands(client.user.id, guildId), { body: commands });
        console.log('Successfully reloaded application (/) commands.');
    } catch (error) {
        console.log(error);
    }
});

client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) return;

    const { commandName, options } = interaction;

    if (commandName === 'chat') {
        const message = options.getString('message');
        await interaction.reply(`You said: ${message}`);
    }
});

client.login(process.env.DISCORD_BOT_TOKEN);