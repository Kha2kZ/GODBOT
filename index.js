// index.js - Discord.js v14, auto-register slash command cho mọi guild và xử lý /chat
require('dotenv').config();
const {
  Client,
  GatewayIntentBits,
  Partials,
  PermissionsBitField,
  ChannelType,
  SlashCommandBuilder
} = require('discord.js');

const token = process.env.DISCORD_TOKEN;
if (!token) {
  console.error('Missing DISCORD_TOKEN in environment (.env or Secrets).');
  process.exit(1);
}

// Định nghĩa command
const commands = [
  new SlashCommandBuilder()
    .setName('chat')
    .setDescription('Bot gửi tin nhắn vào kênh hiện tại')
    .addStringOption(option =>
      option.setName('message')
        .setDescription('Nội dung cần gửi')
        .setRequired(true)
    )
    .toJSON()
];

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
  partials: [Partials.Channel]
});

client.once('ready', async () => {
  console.log(`Logged in as ${client.user.tag}`);

  // Đăng command cho mọi guild hiện có trong cache (hiển thị ngay)
  try {
    if (!client.guilds.cache.size) {
      console.log('Bot chưa có guild trong cache (chưa join server nào).');
    } else {
      for (const [, guild] of client.guilds.cache) {
        try {
          await guild.commands.set(commands);
          console.log(`Registered commands for guild ${guild.name} (${guild.id})`);
        } catch (err) {
          console.error(`Failed to register commands for guild ${guild.id}:`, err);
        }
      }
    }
  } catch (err) {
    console.error('Error while registering commands:', err);
  }
});

// Khi bot được add vào guild mới -> đăng command cho guild đó luôn
client.on('guildCreate', async (guild) => {
  try {
    await guild.commands.set(commands);
    console.log(`Registered commands for newly joined guild ${guild.name} (${guild.id})`);
  } catch (err) {
    console.error(`Failed to register commands for new guild ${guild.id}:`, err);
  }
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'chat') {
    const content = interaction.options.getString('message', true);
    const channel = interaction.channel;

    // Không cho phép chạy trong DM
    if (!channel || channel.type === ChannelType.DM) {
      await interaction.reply({ content: 'Lệnh này chỉ dùng trong kênh server (không dùng trong DM).', ephemeral: true });
      return;
    }

    // Kiểm tra quyền của bot trong kênh
    const botMember = interaction.guild?.members?.me ?? (await interaction.guild.members.fetch(client.user.id));
    const botPermissions = channel.permissionsFor(botMember);
    if (!botPermissions || !botPermissions.has(PermissionsBitField.Flags.SendMessages)) {
      await interaction.reply({ content: 'Bot không có quyền gửi tin nhắn trong kênh này.', ephemeral: true });
      return;
    }

    // Defer để có thêm thời gian xử lý
    await interaction.deferReply({ ephemeral: true });

    try {
      await channel.send(content);
      await interaction.editReply('Đã gửi tin nhắn vào kênh.');
    } catch (err) {
      console.error('Lỗi khi gửi tin nhắn:', err);
      await interaction.editReply('Gửi thất bại: lỗi hoặc bot không có quyền.');
    }
  }
});

client.login(token);