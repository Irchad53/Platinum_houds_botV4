import discord
import asyncio
from scraper_courses import get_upcoming_races
from ml_predictor import train_model, predict_proba
from itertools import combinations
from datetime import datetime, timedelta

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = 123456789  # Remplace avec ton canal ID

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def compute_conf(df, combo):
    return df.loc[combo[0], "proba"] * df.loc[combo[1], "proba"] * df.loc[combo[2], "proba"]

async def send_prediction(channel, race):
    model = train_model()
    df = predict_proba(model, race["dogs"])
    df.reset_index(inplace=True)

    best_combos = []
    for combo in combinations(df.index, 3):
        conf = compute_conf(df, combo)
        if conf >= 0.95:
            dogs = [df.loc[i]["dog_name"] for i in combo]
            best_combos.append((dogs, conf))

    best_combos = sorted(best_combos, key=lambda x: x[1], reverse=True)[:3]
    if not best_combos:
        return

    msg = f"**🎯 Tiercé Discord — {race['start_time'].strftime('%H:%M')}**\n"
    for i, (dogs, conf) in enumerate(best_combos, 1):
        msg += f"\n#{i} — 🧠 {conf*100:.1f}%\n🥇 {dogs[0]}\n🥈 {dogs[1]}\n🥉 {dogs[2]}\n"
    await channel.send(msg)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
    races = get_upcoming_races()
    now = datetime.now()
    for race in races:
        delay = (race["start_time"] - timedelta(minutes=5) - now).total_seconds()
        if delay > 0:
            await asyncio.sleep(delay)
            channel = client.get_channel(CHANNEL_ID)
            await send_prediction(channel, race)

client.run(TOKEN)
