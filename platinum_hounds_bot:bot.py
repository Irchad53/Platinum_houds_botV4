import asyncio
from telegram import Bot
from scraper_courses import get_upcoming_races
from ml_predictor import train_model, predict_proba
from itertools import combinations
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

TOKEN = "7511519301:AAFnkZ5jwLuNfN5kQwm_-0h-seyeQS0rw90"
CHAT_ID = "123456789"  # à remplacer

bot = Bot(token=TOKEN)

def compute_combined_confidence(df, combo):
    return df.loc[combo[0], "proba"] * df.loc[combo[1], "proba"] * df.loc[combo[2], "proba"]

async def send_prediction(race):
    model = train_model()
    df = predict_proba(model, race["dogs"])
    df.reset_index(inplace=True)

    # Générer les combinaisons de 3
    best_combos = []
    for combo in combinations(df.index, 3):
        conf = compute_combined_confidence(df, combo)
        if conf >= 0.95:
            dogs = [df.loc[i]["dog_name"] for i in combo]
            best_combos.append((dogs, conf))

    best_combos = sorted(best_combos, key=lambda x: x[1], reverse=True)[:3]

    if not best_combos:
        return

    msg = f"🎯 *Tiercé Platinum — {race['start_time'].strftime('%H:%M')}*\n"
    for i, (dogs, conf) in enumerate(best_combos, 1):
        msg += f"\n#{i} — 🧠 *{conf*100:.1f}%*\n🥇 {dogs[0]}\n🥈 {dogs[1]}\n🥉 {dogs[2]}\n"

    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

async def schedule_races():
    scheduler = AsyncIOScheduler()
    races = get_upcoming_races()
    now = datetime.datetime.now()

    for race in races:
        send_time = race["start_time"] - datetime.timedelta(minutes=5)
        if send_time > now:
            scheduler.add_job(send_prediction, 'date', run_date=send_time, args=[race])
    scheduler.start()

if __name__ == "__main__":
    asyncio.run(schedule_races())
