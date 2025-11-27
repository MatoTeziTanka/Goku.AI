# Discord Bot Development & REST APIs Complete Guide (2025-2026)
## Community Automation, APIs, & Integration Mastery

**Goal**: Build Discord bots for automation, moderation, and potential monetization  
**Stack**: Discord.py, Discord.js, REST APIs, WebSockets, OAuth2  
**Deployment**: Dell R730 VMs, 24/7 uptime

## DISCORD BOT BASICS

### What is a Discord Bot?
- Automated user that responds to commands and events
- Moderates servers, provides info, plays music, games, etc.
- Uses Discord API (REST + Gateway/WebSocket)
- Can be monetized (premium features, server boosting)

### Bot Use Cases
1. **Moderation**: Auto-mod, spam filter, warnings
2. **Utility**: Reminders, polls, role management
3. **Entertainment**: Music, games, memes
4. **Integration**: GitHub, Twitter, Twitch notifications
5. **Economy**: Virtual currency, shops, gambling
6. **Analytics**: Server stats, user tracking

## DISCORD BOT SETUP

### Create Bot Account
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Go to "Bot" tab → "Add Bot"
4. Copy token (keep secret!)
5. Enable "Message Content Intent" (required for reading messages)
6. Generate invite link:
   - OAuth2 → URL Generator
   - Scopes: `bot`, `applications.commands`
   - Permissions: Administrator (or specific permissions)

## PYTHON DISCORD BOT (DISCORD.PY)

### Installation
```bash
pip install discord.py
```

### Basic Bot
```python
import discord
from discord.ext import commands

# Create bot with command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

# Run bot
bot.run('YOUR_BOT_TOKEN')
```

### Slash Commands (Modern)
```python
import discord
from discord import app_commands

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyBot()

@client.tree.command(name='hello', description='Say hello')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.mention}!')

@client.tree.command(name='serverinfo', description='Get server info')
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, color=discord.Color.blue())
    embed.add_field(name='Members', value=guild.member_count)
    embed.add_field(name='Created', value=guild.created_at.strftime('%Y-%m-%d'))
    await interaction.response.send_message(embed=embed)

client.run('YOUR_BOT_TOKEN')
```

### Moderation Bot
```python
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Deleted {amount} messages.', delete_after=5)

# Auto-moderation
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Spam filter
    if len(message.content) > 500:
        await message.delete()
        await message.channel.send(f'{message.author.mention} Please don\'t spam!')
    
    # Bad word filter
    bad_words = ['badword1', 'badword2']
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        await message.author.send('Please watch your language!')
    
    await bot.process_commands(message)
```

### Economy System
```python
import json

# Load/save economy data
def load_economy():
    try:
        with open('economy.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_economy(data):
    with open('economy.json', 'w') as f:
        json.dump(data, f, indent=4)

economy = load_economy()

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    balance = economy.get(user_id, 0)
    await ctx.send(f'{ctx.author.mention} has ${balance}')

@bot.command()
async def daily(ctx):
    user_id = str(ctx.author.id)
    economy[user_id] = economy.get(user_id, 0) + 100
    save_economy(economy)
    await ctx.send(f'{ctx.author.mention} claimed $100 daily reward!')

@bot.command()
async def pay(ctx, member: discord.Member, amount: int):
    user_id = str(ctx.author.id)
    target_id = str(member.id)
    
    if economy.get(user_id, 0) < amount:
        await ctx.send('Insufficient funds!')
        return
    
    economy[user_id] = economy.get(user_id, 0) - amount
    economy[target_id] = economy.get(target_id, 0) + amount
    save_economy(economy)
    await ctx.send(f'{ctx.author.mention} paid ${amount} to {member.mention}')
```

## JAVASCRIPT DISCORD BOT (DISCORD.JS)

### Installation
```bash
npm install discord.js
```

### Basic Bot
```javascript
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;
    
    if (message.content === '!ping') {
        message.reply('Pong!');
    }
    
    if (message.content === '!serverinfo') {
        const embed = {
            title: message.guild.name,
            fields: [
                { name: 'Members', value: message.guild.memberCount.toString() },
                { name: 'Created', value: message.guild.createdAt.toDateString() }
            ]
        };
        message.channel.send({ embeds: [embed] });
    }
});

client.login('YOUR_BOT_TOKEN');
```

### Slash Commands (Discord.js v14)
```javascript
const { REST, Routes, SlashCommandBuilder } = require('discord.js');

const commands = [
    new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Replies with Pong!'),
    new SlashCommandBuilder()
        .setName('hello')
        .setDescription('Say hello')
].map(command => command.toJSON());

const rest = new REST({ version: '10' }).setToken('YOUR_BOT_TOKEN');

(async () => {
    await rest.put(
        Routes.applicationCommands('YOUR_CLIENT_ID'),
        { body: commands }
    );
    console.log('Commands registered!');
})();

// Handle interactions
client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
    
    if (interaction.commandName === 'ping') {
        await interaction.reply('Pong!');
    }
    
    if (interaction.commandName === 'hello') {
        await interaction.reply(`Hello ${interaction.user}!`);
    }
});
```

## ADVANCED BOT FEATURES

### Music Bot (YouTube)
```python
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send('You must be in a voice channel!')
        return
    
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()
    
    ydl_opts = {'format': 'bestaudio/best'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))
    
    await ctx.send(f'Now playing: {info["title"]}')

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()
```

### Reaction Roles
```python
@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == '🎮':
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name='Gamer')
        member = guild.get_member(payload.user_id)
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.name == '🎮':
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name='Gamer')
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
```

### Webhook Integration (GitHub, Twitter)
```python
@bot.command()
async def github(ctx, repo: str):
    import requests
    url = f'https://api.github.com/repos/{repo}'
    response = requests.get(url)
    data = response.json()
    
    embed = discord.Embed(title=data['name'], url=data['html_url'])
    embed.add_field(name='Stars', value=data['stargazers_count'])
    embed.add_field(name='Forks', value=data['forks_count'])
    embed.add_field(name='Language', value=data['language'])
    
    await ctx.send(embed=embed)
```

## REST API INTEGRATION

### What is a REST API?
- **RE**presentational **S**tate **T**ransfer
- HTTP-based (GET, POST, PUT, DELETE)
- Stateless (no session)
- JSON/XML data format

### HTTP Methods
- **GET**: Retrieve data
- **POST**: Create data
- **PUT**: Update data
- **DELETE**: Delete data
- **PATCH**: Partial update

### Python Requests Library
```python
import requests

# GET request
response = requests.get('https://api.example.com/users')
data = response.json()

# POST request
payload = {'name': 'Seth', 'age': 30}
response = requests.post('https://api.example.com/users', json=payload)

# Authentication
headers = {'Authorization': 'Bearer YOUR_API_KEY'}
response = requests.get('https://api.example.com/protected', headers=headers)
```

### Popular APIs for Bots

#### OpenWeather API
```python
@bot.command()
async def weather(ctx, city: str):
    api_key = 'YOUR_OPENWEATHER_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    
    await ctx.send(f'Weather in {city}: {temp}°C, {desc}')
```

#### CoinGecko API (Crypto Prices)
```python
@bot.command()
async def crypto(ctx, coin: str):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    price = data[coin]['usd']
    await ctx.send(f'{coin.upper()}: ${price}')
```

#### NASA API
```python
@bot.command()
async def apod(ctx):
    api_key = 'YOUR_NASA_API_KEY'
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    embed = discord.Embed(title=data['title'], description=data['explanation'])
    embed.set_image(url=data['url'])
    await ctx.send(embed=embed)
```

## BUILDING YOUR OWN REST API

### Flask REST API
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

users = []

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    users.append(data)
    return jsonify(data), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id < len(users):
        return jsonify(users[user_id])
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
```

### FastAPI REST API (Modern)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

users = []

@app.get('/api/users')
async def get_users():
    return users

@app.post('/api/users')
async def create_user(user: User):
    users.append(user)
    return user

@app.get('/api/users/{user_id}')
async def get_user(user_id: int):
    if user_id < len(users):
        return users[user_id]
    raise HTTPException(status_code=404, detail='User not found')

# Run: uvicorn main:app --reload
```

## WEBHOOKS

### Discord Webhooks
```python
import requests

webhook_url = 'https://discord.com/api/webhooks/...'

data = {
    'content': 'Hello from webhook!',
    'username': 'Custom Bot'
}

requests.post(webhook_url, json=data)
```

### GitHub Webhooks (Flask)
```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    secret = b'YOUR_WEBHOOK_SECRET'
    hash_obj = hmac.new(secret, request.data, hashlib.sha256)
    expected_signature = 'sha256=' + hash_obj.hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        return 'Invalid signature', 403
    
    # Process event
    event = request.headers.get('X-GitHub-Event')
    data = request.json
    
    if event == 'push':
        print(f"Push to {data['repository']['name']}")
    
    return 'OK', 200
```

## DEPLOYMENT ON DELL R730

### systemd Service (Linux)
```bash
# /etc/systemd/system/discord-bot.service
[Unit]
Description=Discord Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/bot
ExecStart=/usr/bin/python3 /home/botuser/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

```bash
docker build -t discord-bot .
docker run -d --name bot --restart unless-stopped discord-bot
```

## MONETIZATION STRATEGIES

### Premium Bot Features
- Free tier: Basic commands
- Premium tier ($5/month): Advanced features, custom commands, priority support

### Server Boosting
- Offer custom bots for server boosters

### Commission Work
- Fiverr, Upwork: Custom Discord bots ($50-$500+)

### Patreon
- Support for bot development, early access to features

## SECURITY BEST PRACTICES

1. **Never share bot token** (regenerate if leaked)
2. **Use environment variables** for secrets
3. **Rate limiting** (prevent spam abuse)
4. **Input validation** (prevent SQL injection, XSS)
5. **Permission checks** (verify user has required perms)

## LEARNING RESOURCES

- Discord.py Docs: discordpy.readthedocs.io
- Discord.js Guide: discordjs.guide
- Discord API Docs: discord.com/developers/docs
- FastAPI Docs: fastapi.tiangolo.com

**Complete Discord bot & REST API guide for SHENRON - Automation focused**

