# ═══════════════════════════════════════════════════════════
# BGMI PRICE ANALYZER BOT — FINAL COMPLETE VERSION
# Screenshot auto-analyze + Channel verification + Fixed prices
# ═══════════════════════════════════════════════════════════

import os
import json
import base64
import logging
import httpx
from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler,
    ContextTypes, filters
)

# ═══════════════════════════════════════════
# ⚙️ CONFIG
# ═══════════════════════════════════════════

BOT_TOKEN = "8873305917:AAHjvSJHuJpz3BUta9fu6x6eoWkU1hCfzHk"
OWNER_ID = 1257888659
CHANNEL_ID = -1002719155814
CHANNEL_LINK = "https://t.me/+FrEKPHXrMhliY2Fl"
OPENROUTER_API_KEY = "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"

VISION_MODEL = "google/gemini-2.0-flash-exp:free"
BOT_NAME = "BGMI Price Analyzer Bot"
VERSION = "3.0 FINAL"

# ═══════════════════════════════════════════
# 💰 PRICES DATABASE (Real Market Rates)
# ═══════════════════════════════════════════

X_SUIT_PRICES = {
    "Aelon":          {1: 800,  2: 1200, 3: 1800, 4: 2500, 5: 3500, 6: 5000},
    "Silvanus":       {1: 800,  2: 1200, 3: 1800, 4: 2500, 5: 3500, 6: 5000},
    "Poseidon":       {1: 900,  2: 1300, 3: 1900, 4: 2700, 5: 3700, 6: 5200},
    "Blood Raven":    {1: 1000, 2: 1500, 3: 2200, 4: 3000, 5: 4200, 6: 5800},
    "Mummy":          {1: 1000, 2: 1500, 3: 2200, 4: 3000, 5: 4200, 6: 5800},
    "Golden Pharaoh": {1: 1100, 2: 1600, 3: 2400, 4: 3300, 5: 4500, 6: 6200},
    "Frost Wing":     {1: 1000, 2: 1500, 3: 2200, 4: 3000, 5: 4200, 6: 5800},
    "Nebula":         {1: 900,  2: 1300, 3: 1900, 4: 2700, 5: 3700, 6: 5200},
    "Wave Whisperer": {1: 800,  2: 1200, 3: 1800, 4: 2500, 5: 3500, 6: 5000},
    "Arcane Jester":  {1: 800,  2: 1200, 3: 1800, 4: 2500, 5: 3500, 6: 5000},
}
DEFAULT_X_SUIT = {1: 800, 2: 1200, 3: 1800, 4: 2500, 5: 3500, 6: 5000}

GUN_SKIN_PRICES = {
    "M416 Glacier":     {1: 500, 2: 700, 3: 1000, 4: 1400, 5: 1900, 6: 2500, 7: 3300},
    "AKM Glacier":      {1: 400, 2: 550, 3: 800,  4: 1100, 5: 1500, 6: 2000, 7: 2700},
    "M416 Fool's Gold": {1: 350, 2: 500, 3: 700,  4: 950,  5: 1300, 6: 1700, 7: 2300},
    "M762 Glacier":     {1: 450, 2: 600, 3: 850,  4: 1200, 5: 1600, 6: 2200, 7: 2900},
    "Kar98k Glacier":   {1: 400, 2: 550, 3: 750,  4: 1000, 5: 1400, 6: 1900, 7: 2500},
    "UMP45 Glacier":    {1: 350, 2: 500, 3: 700,  4: 950,  5: 1300, 6: 1700, 7: 2300},
    "AWM Glacier":      {1: 450, 2: 600, 3: 850,  4: 1200, 5: 1600, 6: 2200, 7: 2900},
    "Groza Glacier":    {1: 450, 2: 600, 3: 850,  4: 1200, 5: 1600, 6: 2200, 7: 2900},
}
DEFAULT_GUN_SKIN = {1: 350, 2: 500, 3: 700, 4: 950, 5: 1300, 6: 1700, 7: 2300}

VEHICLE_PRICES = {
    "McLaren 570S": 1200, "McLaren P1": 1800,
    "Aston Martin DBS": 1000, "Aston Martin Vantage": 900,
    "Lamborghini Aventador": 1800, "Lamborghini Urus": 2200,
    "Bugatti Veyron": 3000, "Porsche 911": 800,
    "Ducati": 600, "Harley Davidson": 700,
    "Tesla Cybertruck": 1500, "Ferrari": 2000,
}
DEFAULT_VEHICLE = 600

MYTHIC_OUTFIT_PRICES = {
    "Godzilla": 700, "Blood Raven": 600, "Golden Dragon": 500,
    "Pharaoh": 500, "Poseidon": 550, "Silvanus": 550,
    "Mummy": 600, "Mythic Fashion": 300,
}
DEFAULT_MYTHIC = 300

TIER_BONUS = {
    "Conqueror": 800, "Ace": 400, "Crown": 200,
    "Diamond": 100, "Platinum": 50, "Gold": 0,
}

# ═══════════════════════════════════════════
# 🧠 ANALYZER FUNCTIONS
# ═══════════════════════════════════════════

def get_x_suit_price(name, level):
    table = X_SUIT_PRICES.get(name.strip().title(), DEFAULT_X_SUIT)
    level = max(1, min(6, level))
    return table.get(level, DEFAULT_X_SUIT[level])

def get_gun_price(name, level):
    for key in GUN_SKIN_PRICES:
        if key.lower() == name.lower() or key.lower() in name.lower():
            level = max(1, min(7, level))
            return GUN_SKIN_PRICES[key][level]
    level = max(1, min(7, level))
    return DEFAULT_GUN_SKIN[level]

def get_vehicle_price(name):
    for key in VEHICLE_PRICES:
        if key.lower() in name.lower() or name.lower() in key.lower():
            return VEHICLE_PRICES[key]
    return DEFAULT_VEHICLE

def get_mythic_price(name):
    for key in MYTHIC_OUTFIT_PRICES:
        if key.lower() in name.lower():
            return MYTHIC_OUTFIT_PRICES[key]
    return DEFAULT_MYTHIC

def get_age_bonus(years, has_og=False):
    bonus = 0
    if years >= 6: bonus = 500
    elif years >= 4: bonus = 250
    elif years >= 2: bonus = 100
    if has_og: bonus += 500
    return bonus

def uc_return(uc, years):
    rate = 0.02
    if years >= 4: rate = 0.04
    elif years >= 2: rate = 0.03
    return int(uc * rate)

def analyze_account(data):
    breakdown = {}
    total = 0

    x_total = 0
    x_details = []
    for x in data.get("x_suits", []):
        p = get_x_suit_price(x["name"], x["level"])
        x_total += p
        x_details.append(f"{x['name']} Lv{x['level']} — ₹{p:,}")
    if x_total:
        breakdown["👕 X-Suits"] = x_total
        breakdown["   ↳"] = x_details
        total += x_total

    g_total = 0
    g_details = []
    for g in data.get("gun_skins", []):
        p = get_gun_price(g["name"], g["level"])
        g_total += p
        g_details.append(f"{g['name']} Lv{g['level']} — ₹{p:,}")
    if g_total:
        breakdown["🔫 Gun Skins"] = g_total
        breakdown["   ↳"] = g_details
        total += g_total

    v_total = 0
    v_details = []
    for v in data.get("vehicle_skins", []):
        p = get_vehicle_price(v["name"])
        v_total += p
        v_details.append(f"{v['name']} — ₹{p:,}")
    if v_total:
        breakdown["🚗 Vehicle Skins"] = v_total
        breakdown["   ↳"] = v_details
        total += v_total

    m_total = 0
    m_details = []
    for m in data.get("mythic_outfits", []):
        p = get_mythic_price(m["name"])
        m_total += p
        m_details.append(f"{m['name']} — ₹{p:,}")
    if m_total:
        breakdown["🦸 Mythic Outfits"] = m_total
        breakdown["   ↳"] = m_details
        total += m_total

    uc_val = uc_return(data.get("uc_spent", 0), data.get("account_age_years", 0))
    if uc_val:
        breakdown["💎 UC Return"] = uc_val
        total += uc_val

    age_bonus = get_age_bonus(data.get("account_age_years", 0), data.get("has_og_seasons", False))
    if age_bonus:
        breakdown["📅 OG Bonus"] = age_bonus
        total += age_bonus

    tier = data.get("tier", "").capitalize()
    tier_bonus = TIER_BONUS.get(tier, 0)
    if tier_bonus:
        breakdown[f"🏆 {tier} Bonus"] = tier_bonus
        total += tier_bonus

    level_bonus = min((data.get("level", 0) // 10) * 30, 500)
    if level_bonus:
        breakdown["🎯 Level Bonus"] = level_bonus
        total += level_bonus

    low = int(total * 0.60)
    high = int(total * 0.85)
    return {"base": int(total), "low": low, "high": high, "breakdown": breakdown}

def worth_it_verdict(result, uc_spent):
    avg = (result["low"] + result["high"]) // 2
    original = uc_spent * 1.2
    if original <= 0:
        return "⚠️ UC data missing."
    ratio = avg / original
    if ratio >= 0.3: return "🔥 EXCELLENT — बहुत अच्छी resale value!"
    elif ratio >= 0.2: return "✅ WORTH IT — Good account."
    elif ratio >= 0.12: return "⚖️ AVERAGE — ठीक-ठाक value."
    elif ratio >= 0.06: return "⚠️ BELOW AVERAGE — पैसे ज़्यादा डूबे।"
    else: return "❌ NOT WORTH — बहुत कम resale value।"

# ═══════════════════════════════════════════
# 👁️ OPENROUTER VISION FUNCTION
# ═══════════════════════════════════════════

VISION_PROMPT = """You are analyzing a BGMI (Battlegrounds Mobile India) inventory screenshot.

Extract ALL visible items from this screenshot and return ONLY valid JSON.

Format:
{
  "level": 65,
  "uc_spent": 25000,
  "tier": "Ace",
  "x_suits": [{"name": "Blood Raven", "level": 4}],
  "gun_skins": [{"name": "M416 Glacier", "level": 5}],
  "vehicle_skins": [{"name": "McLaren 570S"}],
  "mythic_outfits": [{"name": "Godzilla"}],
  "has_og_seasons": false
}

Rules:
1. X-Suits: Look for "Mythic" or "X-Suit" tagged outfits. Names: Blood Raven, Poseidon, Silvanus, Aelon, Mummy, Golden Pharaoh, Frost Wing, Nebula, Wave Whisperer, Arcane Jester. Level 1-6 shown as "Lv.X" or "Lv X".
2. Gun Skins: Upgradable guns like "M416 Glacier", "AKM Glacier", "M762 Glacier", "Kar98k Glacier", "UMP45 Glacier", "AWM Glacier", "Groza Glacier", "M416 Fool's Gold". Level 1-7.
3. Vehicle Skins: "McLaren 570S", "McLaren P1", "Aston Martin DBS", "Lamborghini Aventador", "Bugatti Veyron", "Porsche 911", "Ducati", "Tesla Cybertruck".
4. Mythic Outfits: "Godzilla", "Blood Raven", "Golden Dragon", "Pharaoh", "Poseidon", "Silvanus", "Mummy".
5. Look at top-right corner of inventory for account level.
6. Only include items you can clearly identify.
7. Return ONLY the JSON, no markdown, no backticks, no extra text."""

async def analyze_screenshot(image_bytes):
    image_b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "model": VISION_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }],
        "max_tokens": 2048,
        "temperature": 0.2
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/account_price_bot",
        "X-Title": "BGMI Price Bot"
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload, headers=headers
            )
            if response.status_code != 200:
                return {"error": f"API error {response.status_code}: {response.text[:200]}"}
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            content = content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            content = content.strip()
            return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "AI didn't return valid JSON. Try clearer screenshot or /manual"}
    except httpx.TimeoutException:
        return {"error": "API timeout. Try again or use /manual."}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)[:200]}"}

# ═══════════════════════════════════════════
# 🤖 BOT LOGIC
# ═══════════════════════════════════════════

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
user_stats = {}
processing_users = set()

(WAITING_JOIN, CHOOSE_MODE,
 LEVEL, UC_SPENT, AGE, OG_SEASON, TIER,
 X_SUIT_COUNT, X_SUIT_NAME, X_SUIT_LEVEL,
 GUN_COUNT, GUN_NAME, GUN_LEVEL,
 VEHICLE_COUNT, VEHICLE_NAME,
 MYTHIC_COUNT, MYTHIC_NAME) = range(17)

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Joined — Verify Me", callback_data="verify_join")]
    ])

async def check_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ('creator', 'administrator', 'member')
    except Exception as e:
        logging.warning(f"Membership check failed: {e}")
        return False

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ctx.user_data.clear()
    if await check_membership(ctx.bot, user.id):
        await update.message.reply_text(
            f"✅ *Welcome {user.first_name}!*\n\n"
            "📸 *Screenshot bhejo* apne BGMI inventory ka\n"
            "OR\n"
            "⌨️ /manual type karo step-by-step input ke liye",
            parse_mode="Markdown"
        )
        return CHOOSE_MODE
    await update.message.reply_text(
        "🔒 *Channel Verification Required*\n\n"
        "Join our channel first:\n👉 LIGHTNING ⚡ SERVER⚡\n\n"
        "After joining, click *Verify Me*.",
        parse_mode="Markdown",
        reply_markup=join_keyboard()
    )
    return WAITING_JOIN

async def verify_join(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await check_membership(ctx.bot, query.from_user.id):
        await query.edit_message_text(
            "✅ *Verified!*\n\nScreenshot bhejo OR /manual type karo",
            parse_mode="Markdown"
        )
        return CHOOSE_MODE
    await query.edit_message_text(
        "❌ *Not verified yet.*\n\nJoin the channel, then click Verify again.",
        parse_mode="Markdown",
        reply_markup=join_keyboard()
    )
    return WAITING_JOIN

async def handle_screenshot(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in processing_users:
        return CHOOSE_MODE
    processing_users.add(user_id)
    try:
        msg = await update.message.reply_text("🔍 AI analyze kar raha hai... 10-20 sec")
        photo = update.message.photo[-1]
        file = await ctx.bot.get_file(photo.file_id)
        image_bytes = bytes(await file.download_as_bytearray())
        os.makedirs("uploads", exist_ok=True)
        with open(f"uploads/{user_id}.jpg", "wb") as f:
            f.write(image_bytes)
        result = await analyze_screenshot(image_bytes)
        try:
            await msg.delete()
        except:
            pass
        if "error" in result:
            await update.message.reply_text(
                f"⚠️ {result['error']}\n\nTry clearer screenshot or /manual",
                parse_mode="Markdown"
            )
            return CHOOSE_MODE
        for k, v in {"level": 1, "uc_spent": 0, "tier": "Gold",
                     "account_age_years": 1, "has_og_seasons": False,
                     "x_suits": [], "gun_skins": [],
                     "vehicle_skins": [], "mythic_outfits": []}.items():
            result.setdefault(k, v)
        await show_report(update, ctx, result)
        return ConversationHandler.END
    finally:
        processing_users.discard(user_id)

async def manual_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text(
        "⌨️ *Manual Mode*\n\n1️⃣ Account Level? (e.g. 65)",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return LEVEL

async def get_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return LEVEL
    ctx.user_data["level"] = int(t)
    await update.message.reply_text("2️⃣ Total UC spent?")
    return UC_SPENT

async def get_uc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip().replace(",", "")
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return UC_SPENT
    ctx.user_data["uc_spent"] = int(t)
    await update.message.reply_text("3️⃣ Account age in years?")
    return AGE

async def get_age(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return AGE
    ctx.user_data["account_age_years"] = int(t)
    await update.message.reply_text(
        "4️⃣ Season 1-5 OG items?",
        reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True, resize_keyboard=True)
    )
    return OG_SEASON

async def get_og(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["has_og_seasons"] = "yes" in update.message.text.lower()
    await update.message.reply_text(
        "5️⃣ Highest Tier?",
        reply_markup=ReplyKeyboardMarkup(
            [["Bronze", "Silver", "Gold"], ["Platinum", "Diamond", "Crown"], ["Ace", "Conqueror"]],
            one_time_keyboard=True, resize_keyboard=True)
    )
    return TIER

async def get_tier(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["tier"] = update.message.text.strip()
    ctx.user_data["x_suits"] = []
    ctx.user_data["gun_skins"] = []
    ctx.user_data["vehicle_skins"] = []
    ctx.user_data["mythic_outfits"] = []
    await update.message.reply_text(
        "👕 How many X-Suits? (0 if none)",
        reply_markup=ReplyKeyboardRemove()
    )
    return X_SUIT_COUNT

async def x_count(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return X_SUIT_COUNT
    ctx.user_data["x_total"] = int(t)
    ctx.user_data["x_current"] = 0
    if int(t) == 0:
        return await ask_guns(update, ctx)
    await update.message.reply_text("X-Suit #1 name? (e.g. Blood Raven)")
    return X_SUIT_NAME

async def x_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["current_x"] = update.message.text.strip()
    await update.message.reply_text(f"*{ctx.user_data['current_x']}* level? (1-6)", parse_mode="Markdown")
    return X_SUIT_LEVEL

async def x_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit() or not (1 <= int(t) <= 6):
        await update.message.reply_text("❌ 1-6 only")
        return X_SUIT_LEVEL
    ctx.user_data["x_suits"].append({"name": ctx.user_data["current_x"], "level": int(t)})
    ctx.user_data["x_current"] += 1
    if ctx.user_data["x_current"] < ctx.user_data["x_total"]:
        await update.message.reply_text(f"X-Suit #{ctx.user_data['x_current']+1} name?")
        return X_SUIT_NAME
    return await ask_guns(update, ctx)

async def ask_guns(update, ctx):
    await update.message.reply_text("🔫 How many Glacier/upgradable guns? (0 if none)")
    return GUN_COUNT

async def gun_count(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return GUN_COUNT
    ctx.user_data["g_total"] = int(t)
    ctx.user_data["g_current"] = 0
    if int(t) == 0:
        return await ask_vehicles(update, ctx)
    await update.message.reply_text("Gun #1 name? (e.g. M416 Glacier)")
    return GUN_NAME

async def gun_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["current_g"] = update.message.text.strip()
    await update.message.reply_text(f"*{ctx.user_data['current_g']}* level? (1-7)", parse_mode="Markdown")
    return GUN_LEVEL

async def gun_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit() or not (1 <= int(t) <= 7):
        await update.message.reply_text("❌ 1-7 only")
        return GUN_LEVEL
    ctx.user_data["gun_skins"].append({"name": ctx.user_data["current_g"], "level": int(t)})
    ctx.user_data["g_current"] += 1
    if ctx.user_data["g_current"] < ctx.user_data["g_total"]:
        await update.message.reply_text(f"Gun #{ctx.user_data['g_current']+1} name?")
        return GUN_NAME
    return await ask_vehicles(update, ctx)

async def ask_vehicles(update, ctx):
    await update.message.reply_text("🚗 How many vehicle skins? (0 if none)")
    return VEHICLE_COUNT

async def vehicle_count(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return VEHICLE_COUNT
    ctx.user_data["v_total"] = int(t)
    ctx.user_data["v_current"] = 0
    if int(t) == 0:
        return await ask_mythics(update, ctx)
    await update.message.reply_text("Vehicle #1 name? (e.g. McLaren 570S)")
    return VEHICLE_NAME

async def vehicle_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["vehicle_skins"].append({"name": update.message.text.strip()})
    ctx.user_data["v_current"] += 1
    if ctx.user_data["v_current"] < ctx.user_data["v_total"]:
        await update.message.reply_text(f"Vehicle #{ctx.user_data['v_current']+1} name?")
        return VEHICLE_NAME
    return await ask_mythics(update, ctx)

async def ask_mythics(update, ctx):
    await update.message.reply_text("🦸 How many Mythic outfits? (0 if none)")
    return MYTHIC_COUNT

async def mythic_count(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.strip()
    if not t.isdigit():
        await update.message.reply_text("❌ Number only")
        return MYTHIC_COUNT
    ctx.user_data["m_total"] = int(t)
    ctx.user_data["m_current"] = 0
    if int(t) == 0:
        return await final_report(update, ctx)
    await update.message.reply_text("Mythic #1 name? (e.g. Godzilla)")
    return MYTHIC_NAME

async def mythic_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["mythic_outfits"].append({"name": update.message.text.strip()})
    ctx.user_data["m_current"] += 1
    if ctx.user_data["m_current"] < ctx.user_data["m_total"]:
        await update.message.reply_text(f"Mythic #{ctx.user_data['m_current']+1} name?")
        return MYTHIC_NAME
    return await final_report(update, ctx)

async def final_report(update, ctx):
    await show_report(update, ctx, ctx.user_data.copy())
    return ConversationHandler.END

async def show_report(update, ctx, data):
    result = analyze_account(data)
    verdict = worth_it_verdict(result, data.get("uc_spent", 0))
    lines = []
    for k, v in result["breakdown"].items():
        if isinstance(v, list):
            for d in v:
                lines.append(f"      ◦ {d}")
        else:
            lines.append(f"   • {k}: ₹{v:,}")
    breakdown_text = "\n".join(lines)
    x_s = ", ".join([f"{x['name']} Lv{x['level']}" for x in data.get("x_suits", [])]) or "None"
    g_s = ", ".join([f"{g['name']} Lv{g['level']}" for g in data.get("gun_skins", [])]) or "None"
    v_s = ", ".join([v["name"] for v in data.get("vehicle_skins", [])]) or "None"
    m_s = ", ".join([m["name"] for m in data.get("mythic_outfits", [])]) or "None"
    msg = (
        "📊 *BGMI ACCOUNT — PRICE REPORT*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 Level: *{data.get('level')}*\n"
        f"🏆 Tier: *{data.get('tier')}*\n"
        f"💎 UC Spent: *{data.get('uc_spent'):,}*\n"
        f"📅 Age: *{data.get('account_age_years')} years*\n"
        f"⭐ OG Seasons: *{'Yes' if data.get('has_og_seasons') else 'No'}*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎒 *ITEMS:*\n"
        f"👕 X-Suits: {x_s}\n"
        f"🔫 Guns: {g_s}\n"
        f"🚗 Vehicles: {v_s}\n"
        f"🦸 Mythic: {m_s}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰 *BREAKDOWN:*\n"
        f"{breakdown_text}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📈 Base Value: ₹{result['base']:,}\n"
        f"💵 *Realistic Selling Price:*\n"
        f"      ₹{result['low']:,}  —  ₹{result['high']:,}\n\n"
        f"🧾 *Verdict:* {verdict}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ _Selling/buying BGMI accounts violates Krafton ToS — 10-year ban risk. Estimate only._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")
    try:
        user = update.effective_user
        await ctx.bot.send_message(
            chat_id=OWNER_ID,
            text=f"🔔 *New Analysis*\n👤 {user.first_name} (`{user.id}`)\n💵 ₹{result['low']:,} — ₹{result['high']:,}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.warning(f"Owner notify failed: {e}")
    user_stats[update.effective_user.id] = user_stats.get(update.effective_user.id, 0) + 1

async def stats_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only.")
        return
    total = sum(user_stats.values())
    msg = f"👑 *OWNER STATS*\n━━━━━━━━━━━━\nTotal: *{total}*\nUsers: *{len(user_stats)}*\n━━━━━━━━━━━━\n"
    for uid, c in sorted(user_stats.items(), key=lambda x: -x[1])[:5]:
        msg += f"• `{uid}` — {c}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def broadcast_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only.")
        return
    text = " ".join(ctx.args)
    if not text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    sent = 0
    for uid in user_stats.keys():
        try:
            await ctx.bot.send_message(chat_id=uid, text=f"📢 {text}")
            sent += 1
        except Exception:
            pass
    await update.message.reply_text(f"✅ Sent to {sent} users.")

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("❌ Cancelled. /start to begin again.")
    return ConversationHandler.END

async def post_init(app: Application):
    try:
        await app.bot.send_message(
            chat_id=OWNER_ID,
            text=f"✅ *{BOT_NAME} {VERSION}* is online!\n\nOpenRouter Vision active.",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"⚠️ Startup message failed: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("manual", manual_start),
        ],
        states={
            WAITING_JOIN: [CallbackQueryHandler(verify_join, pattern="^verify_join$")],
            CHOOSE_MODE: [
                MessageHandler(filters.PHOTO, handle_screenshot),
                CommandHandler("manual", manual_start),
            ],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_level)],
            UC_SPENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_uc)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            OG_SEASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_og)],
            TIER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tier)],
            X_SUIT_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, x_count)],
            X_SUIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, x_name)],
            X_SUIT_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, x_level)],
            GUN_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gun_count)],
            GUN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, gun_name)],
            GUN_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, gun_level)],
            VEHICLE_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_count)],
            VEHICLE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_name)],
            MYTHIC_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, mythic_count)],
            MYTHIC_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, mythic_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=True,
        per_user=True,
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    print(f"🤖 {BOT_NAME} {VERSION} started...")
    app.run_polling()

if __name__ == "__main__":
    main()