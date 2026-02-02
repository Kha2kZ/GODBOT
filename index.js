require('dotenv').config();
const { Client, GatewayIntentBits, Partials } = require('discord.js');

const token = process.env.DISCORD_TOKEN;
if (!token) {
  console.error('Missing DISCORD_TOKEN in environment');
  process.exit(1);
}

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
  partials: [Partials.Channel]
});

client.once('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'chat') {
    const content = interaction.options.getString('message', true);

    const channel = interaction.channel;
    if (!channel || !channel.isTextBased || !channel.isTextBased()) {
      await interaction.reply({ content: 'Không tìm thấy kênh hợp lệ để gửi.', ephemeral: true });
      return;
    }

    await interaction.reply({ content: 'Đang gửi tin nhắn...', ephemeral: true });

    try {
      await channel.send(content);
      await interaction.followUp({ content: 'Đã gửi tin nhắn vào kênh.', ephemeral: true });
    } catch (err) {
      console.error('Lỗi khi gửi tin nhắn:', err);
      await interaction.followUp({ content: 'Gửi thất bại: kiểm tra quyền của bot trong kênh.', ephemeral: true });
    }
  }
});

client.login(token);