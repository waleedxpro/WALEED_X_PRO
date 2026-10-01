from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest
import random, datetime, json, os
from PIL import Image, ImageDraw

TOKEN = "8762834861:AAHtfyFCZjxh-qNBCtJNP5mNS1zUqbVFpi0"
OWNER_NAME = "Waleed mirza804"
OWNER_USERNAME = "@WALEEDMIRZA8044"
OWNER_BOT = "@waleedxpro_signal_bot"
REFERRAL_LINK = "https://broker-qx.pro/sign-up/?lid=123456"
DAILY_FREE_LIMIT = 5
DATA_FILE = "users_data.json"
PREMIUM_PASSWORDS = {"WALEED5000": True, "WALEEDXPRO": True, "WM8044": True}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f: return json.load(f)
    return {}
def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f)

def check_limit(uid, username):
    if username and username.lower() == "waleedmirza8044":
        return True, 999
    data=load_data()
    today=datetime.date.today().isoformat()
    s=str(uid)
    if s not in data: data[s]={"date":today,"count":0,"premium":False}
    if data[s]["date"]!=today and not data[s].get("premium"):
        data[s]={"date":today,"count":0,"premium":False}
    if data[s].get("premium"): return True, data[s]["count"]
    if data[s]["count"]>=DAILY_FREE_LIMIT:
        save_data(data)
        return False, data[s]["count"]
    data[s]["count"]+=1
    save_data(data)
    return True, data[s]["count"]

def create_heavy_chart(asset, direction):
    W,H=1000,500
    img=Image.new('RGB',(W,H),'#081222')
    d=ImageDraw.Draw(img)
    d.rectangle([0,0,W-1,H-1],outline='#00FF88',width=3)
    d.rectangle([10,10,280,480],fill='#12233F',outline='#00FF88',width=2)
    is_put="PUT" in direction
    box_col='#FF2222' if is_put else '#00FF88'
    d.rectangle([15,15,275,45],fill='#1A345A')
    d.text((20,18), "WALEED X PRO", fill='#00FF88')
    d.text((20,50), asset, fill='#FFD700')
    d.rectangle([20,90,265,135],fill='#330000' if is_put else '#003300',outline=box_col,width=2)
    d.text((65,98), "▼ PUT ↓" if is_put else "▲ BUY ↑", fill=box_col)
    d.text((20,145), f"Conf: {random.randint(94,99)}%", fill='white')
    d.text((20,165), f"Entry: {datetime.datetime.now().strftime('%H:%M')}", fill='white')
    d.text((20,185), f"Payout: 93%", fill='#FFD700')
    d.text((20,230), f"Owner: {OWNER_NAME}", fill='#00FF88')
    x=310
    base=280
    for i in range(32):
        base+=random.uniform(-10,10)
        if is_put and i>22: base-=6
        if not is_put and i>22: base+=6
        oy=base
        cy=base+random.uniform(-10,10)
        hy=min(oy,cy)-random.uniform(2,6)
        ly=max(oy,cy)+random.uniform(2,6)
        col='#00FF88' if cy<oy else '#FF2222'
        d.line([x,hy,x,ly],fill=col,width=2)
        d.rectangle([x-6, min(oy,cy), x+6, max(oy,cy)], fill=col, outline='white')
        x+=21
    d.line([(310,200),(980,230)], fill='#FFD700', width=2)
    d.line([(310,260),(980,290)], fill='#00BFFF', width=2)
    p=f"/tmp/w_{random.randint(1000,9999)}.png"
    img.save(p)
    return p

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 START LIVE SESSION", callback_data='start_live')],
        [InlineKeyboardButton("🔮 FUTURE SIGNAL", callback_data='future'), InlineKeyboardButton("💥 BIG SIGNAL", callback_data='big_signal')],
        [InlineKeyboardButton("💰 OTC MARKET %", callback_data='otc_market')],
        [InlineKeyboardButton("🎯 APNI MARZI KA PAIR", callback_data='select_pair'), InlineKeyboardButton("🤖 AUTO PAIR", callback_data='auto_pair')],
        [InlineKeyboardButton("📊 MY LIMIT (5 Free Daily)", callback_data='my_limit')],
        [InlineKeyboardButton("💎 PREMIUM 5000 PKR", callback_data='premium')],
        [InlineKeyboardButton("🔗 CREATE ACCOUNT - BONUS", callback_data='referral')],
    ])

def broker_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("QUOTEX 93%", callback_data='broker_QUOTEX')], [InlineKeyboardButton("TRADOWIX 95%", callback_data='broker_TRADOWIX')], [InlineKeyboardButton("Back", callback_data='main')]])
def tf_menu(s="signal"): return InlineKeyboardMarkup([[InlineKeyboardButton("M1", callback_data=f'{s}_M1'), InlineKeyboardButton("M5", callback_data=f'{s}_M5')], [InlineKeyboardButton("Back", callback_data='main')]])
def pair_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("EURUSD_otc", callback_data='pair_EURUSD_otc'), InlineKeyboardButton("XAUUSD_otc", callback_data='pair_XAUUSD_otc')], [InlineKeyboardButton("DASUSD_otc", callback_data='pair_DASUSD_otc'), InlineKeyboardButton("BTCUSD_otc", callback_data='pair_BTCUSD_otc')], [InlineKeyboardButton("Back", callback_data='main')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uname = update.effective_user.username or "No Username"
    is_owner = uname.lower() == "waleedmirza8044"
    tag = "💎 OWNER - UNLIMITED" if is_owner else "5 Free Daily | /redeem se Premium"
    await update.message.reply_text(f"👑 WALEED X PRO BOT\n\n👤 @{uname}\nStatus: {tag}\nOwner: {OWNER_USERNAME}\nBot: {OWNER_BOT}", reply_markup=main_menu())

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔑 Password:\n/redeem WALEED5000\n\nPassword ke liye:\n@WALEEDMIRZA8044 se rabta kro\nPrice: 5000 PKR")
        return
    password = context.args[0].strip()
    uid=str(update.effective_user.id)
    if password in PREMIUM_PASSWORDS:
        data=load_data()
        if uid not in data: data[uid]={"date":datetime.date.today().isoformat(),"count":0,"premium":False}
        data[uid]["premium"]=True
        save_data(data)
        await update.message.reply_text(f"✅ CONGRATULATIONS!\n💎 PREMIUM ACTIVE!\nUnlimited Signals!\n\n{OWNER_NAME}\n{OWNER_USERNAME}")
    else:
        await update.message.reply_text(f"❌ Galat Password!\nSahi password ke liye:\n{OWNER_USERNAME}\nPrice: 5000 PKR")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    data=q.data
    uid=q.from_user.id
    uname=q.from_user.username or ""
    if data=='main':
        await q.edit_message_text(f"👑 {OWNER_NAME}\n{OWNER_USERNAME}", reply_markup=main_menu())
    elif data=='my_limit':
        if uname.lower() == "waleedmirza8044":
            await q.edit_message_text(f"💎 OWNER - UNLIMITED\n{OWNER_NAME}\nAapko limit nahi!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data='main')]]))
            return
        d=load_data().get(str(uid),{"count":0,"premium":False})
        if d.get("premium"): txt=f"💎 PREMIUM - Unlimited!"
        else: txt=f"📊 Aaj: {d.get('count',0)}/{DAILY_FREE_LIMIT}\nBache: {DAILY_FREE_LIMIT-d.get('count',0)}\nKal phir 5 milenge!\n\nPremium: /redeem WALEED5000"
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💎 Premium 5000", callback_data='premium')], [InlineKeyboardButton("Back", callback_data='main')]]))
    elif data in ['select_broker','start_live','auto_pair']:
        if data=='auto_pair': context.user_data['asset']=random.choice(["EURUSD_otc","XAUUSD_otc","DASUSD_otc"])
        await q.edit_message_text("SELECT BROKER", reply_markup=broker_menu())
    elif data.startswith('broker_'):
        context.user_data['broker']=data.split('_')[1]
        await q.edit_message_text("Pair Select Kro", reply_markup=pair_menu())
    elif data=='select_pair':
        await q.edit_message_text("PAIR SELECT:", reply_markup=pair_menu())
    elif data.startswith('pair_'):
        context.user_data['asset']=data.split('_',1)[1]
        await q.edit_message_text(f"Pair: {context.user_data['asset']}", reply_markup=tf_menu("signal"))
    elif data in ['future','big_signal']:
        await q.edit_message_text(f"{data.upper()} SIGNAL", reply_markup=tf_menu(data))
    elif data=='otc_market':
        await q.edit_message_text("💰 OTC PAYOUT %\nEURUSD_otc 93%\nUSDINR_otc 95%\nXAUUSD_otc 92%", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data='main')]]))
    elif data=='referral':
        await q.edit_message_text(f"🔗 HAMARI LINK SE ACCOUNT BNAO\nBonus + Discount!\n\nLink:\n{REFERRAL_LINK}\n\nBana ke screenshot bhejo:\n{OWNER_USERNAME}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 CREATE ACCOUNT", url=REFERRAL_LINK)], [InlineKeyboardButton("📩 Owner Se Rabta", url="https://t.me/WALEEDMIRZA8044")], [InlineKeyboardButton("Back", callback_data='main')]]))
    elif data.startswith('signal_') or data.startswith('future_') or data.startswith('big_'):
        allowed,count=check_limit(uid, uname)
        if not allowed:
            await q.edit_message_text(f"❌ 5 FREE KHATAM!\n\nKal phir 5 milenge!\n\n💎 UNLIMITED OPTIONS:\n1️⃣ Premium 5000 PKR - /redeem PASSWORD\n2️⃣ Referral Link Se Account Bnao\n\nOwner: {OWNER_USERNAME}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💎 Premium 5000", callback_data='premium')], [InlineKeyboardButton("🔗 Referral Account", callback_data='referral')], [InlineKeyboardButton("📩 Owner Rabta", url="https://t.me/WALEEDMIRZA8044")], [InlineKeyboardButton("Back", callback_data='main')]]))
            return
        parts=data.split('_')
        type_s=parts[0]
        tf=parts[1]
        broker=context.user_data.get('broker','QUOTEX')
        asset=context.user_data.get('asset','EURUSD_otc')
        direction=random.choice(["BUY ↑","PUT ↓"])
        entry=(datetime.datetime.now()+datetime.timedelta(minutes=1)).strftime("%H:%M")
        img=create_heavy_chart(asset,direction)
        show_count = "UNLIMITED" if uname.lower()=="waleedmirza8044" or load_data().get(str(uid),{}).get("premium") else f"{count}/{DAILY_FREE_LIMIT}"
        cap=f"👑 {OWNER_NAME} - {type_s.upper()}\n📊 {asset}\n🏦 {broker}\n🎯 {direction}\n⏰ {tf} | {entry}\n📈 {show_count} | Daily 5 Free\n\n⏳ Result 1 min"
        await q.message.reply_photo(photo=open(img,'rb'), caption=cap)
        context.job_queue.run_once(send_result_job, 65, data={"chat_id":q.message.chat_id, "asset":asset, "direction":direction, "tf":tf, "entry":entry}, name=f"res_{uid}_{random.randint(1,99999)}")
    elif data=='premium':
        await q.edit_message_text(f"💎 PREMIUM 5000 PKR\n\nFREE: 5 Daily (Har Roz)\nPREMIUM: Unlimited\n\nOption 1: Direct 5000 PKR\nPassword: WALEED5000\n/redeem WALEED5000\n\nOption 2: Referral Link Se Account Bnao\nDiscount Me Premium!\n\nOwner: {OWNER_USERNAME}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Referral Link", callback_data='referral')], [InlineKeyboardButton("📩 Rabta Kro", url="https://t.me/WALEEDMIRZA8044")], [InlineKeyboardButton("Back", callback_data='main')]]))

async def send_result_job(context: ContextTypes.DEFAULT_TYPE):
    d=context.job.data
    roll=random.random()
    direction=d["direction"]
    open_p=round(random.uniform(61,62),4)
    if roll < 0.70:
        close_p=round(open_p+0.02,4) if "BUY" in direction else round(open_p-0.02,4)
        msg=f"👑 {OWNER_NAME} RESULT\n📊 {d['asset']} | {d['tf']}\n⏰ {d['entry']} || {direction}\n\n✅✅✅ SURESHOT ✅✅✅\n\nOpen: {open_p}\nClose: {close_p}\n\n{OWNER_USERNAME}"
        await context.bot.send_message(chat_id=d["chat_id"], text=msg)
    elif roll < 0.90:
        close_p1=round(open_p-0.01,4) if "BUY" in direction else round(open_p+0.01,4)
        await context.bot.send_message(chat_id=d["chat_id"], text=f"📉 {d['asset']} LOSS - MTG 1\nOpen: {open_p} Close: {close_p1}")
        context.job_queue.run_once(send_mtg_win, 65, data=d, name=f"mtg_{random.randint(1,99999)}")
    else:
        close_p=round(open_p-0.02,4) if "BUY" in direction else round(open_p+0.02,4)
        msg=f"👑 {OWNER_NAME} RESULT\n📊 {d['asset']} | {d['tf']}\n\n❌❌❌ LOSS ❌❌❌\n\nOpen: {open_p} Close: {close_p}"
        await context.bot.send_message(chat_id=d["chat_id"], text=msg)

async def send_mtg_win(context: ContextTypes.DEFAULT_TYPE):
    d=context.job.data
    open_p=round(random.uniform(61,62),4)
    close_p=round(open_p+0.03,4) if "BUY" in d["direction"] else round(open_p-0.03,4)
    msg=f"👑 {OWNER_NAME} RESULT\n📊 {d['asset']} | {d['tf']}\n⏰ {d['entry']} || {d['direction']}\n\n✅ MTG 1 WIN ✅\n\nOpen: {open_p} Close: {close_p}\n\n{OWNER_USERNAME}"
    await context.bot.send_message(chat_id=d["chat_id"], text=msg)

request=HTTPXRequest(connect_timeout=30, read_timeout=30)
app=ApplicationBuilder().token(TOKEN).request(request).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('redeem', redeem))
app.add_handler(CallbackQueryHandler(button_handler))
print("WALEED DAILY 5 FREE + PASSWORD PREMIUM BOT STARTED...")
app.run_polling()
