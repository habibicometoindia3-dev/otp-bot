# main.py v2 
import requests
import time
import asyncio
from datetime import datetime
import re
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

# ============================================================
API_URL            = "http://51.77.216.195/crapi/lamix/viewstats"
API_TOKEN          = "h4lSYnuBWGp4i1hnR4N0fXyGc3leYVdjSpaNVlaEeWs="
TELEGRAM_BOT_TOKEN = "8843473690:AAGXbaAtxtpVct2jpzo41oqQHJYhYcsDif8"
TELEGRAM_GROUP_ID  = -1004376576526
CHANNEL_USERNAME   = "crimeotpnumbers"
GET_NUMBER_URL     = "https://t.me/crimeotpnumbers"
# ============================================================

params = {"token": API_TOKEN, "records": ""}

country_map = {
    "1":    ("US",  "🇺🇸", "English"),
    "1242": ("BS",  "🇧🇸", "English"),
    "1246": ("BB",  "🇧🇧", "English"),
    "1264": ("AI",  "🇦🇮", "English"),
    "1268": ("AG",  "🇦🇬", "English"),
    "1284": ("VG",  "🇻🇬", "English"),
    "1340": ("VI",  "🇻🇮", "English"),
    "1345": ("KY",  "🇰🇾", "English"),
    "1441": ("BM",  "🇧🇲", "English"),
    "1473": ("GD",  "🇬🇩", "English"),
    "1649": ("TC",  "🇹🇨", "English"),
    "1664": ("MS",  "🇲🇸", "English"),
    "1670": ("MP",  "🇲🇵", "English"),
    "1671": ("GU",  "🇬🇺", "English"),
    "1684": ("AS",  "🇦🇸", "English"),
    "1721": ("SX",  "🇸🇽", "English"),
    "1758": ("LC",  "🇱🇨", "English"),
    "1767": ("DM",  "🇩🇲", "English"),
    "1784": ("VC",  "🇻🇨", "English"),
    "1787": ("PR",  "🇵🇷", "Spanish"),
    "1809": ("DO",  "🇩🇴", "Spanish"),
    "1868": ("TT",  "🇹🇹", "English"),
    "1869": ("KN",  "🇰🇳", "English"),
    "1876": ("JM",  "🇯🇲", "English"),
    "501":  ("BZ",  "🇧🇿", "English"),
    "502":  ("GT",  "🇬🇹", "Spanish"),
    "503":  ("SV",  "🇸🇻", "Spanish"),
    "504":  ("HN",  "🇭🇳", "Spanish"),
    "505":  ("NI",  "🇳🇮", "Spanish"),
    "506":  ("CR",  "🇨🇷", "Spanish"),
    "507":  ("PA",  "🇵🇦", "Spanish"),
    "509":  ("HT",  "🇭🇹", "Haitian Creole"),
    "53":   ("CU",  "🇨🇺", "Spanish"),
    "51":   ("PE",  "🇵🇪", "Spanish"),
    "52":   ("MX",  "🇲🇽", "Spanish"),
    "54":   ("AR",  "🇦🇷", "Spanish"),
    "55":   ("BR",  "🇧🇷", "Portuguese"),
    "56":   ("CL",  "🇨🇱", "Spanish"),
    "57":   ("CO",  "🇨🇴", "Spanish"),
    "58":   ("VE",  "🇻🇪", "Spanish"),
    "591":  ("BO",  "🇧🇴", "Spanish"),
    "592":  ("GY",  "🇬🇾", "English"),
    "593":  ("EC",  "🇪🇨", "Spanish"),
    "594":  ("GF",  "🇬🇫", "French"),
    "595":  ("PY",  "🇵🇾", "Spanish"),
    "596":  ("MQ",  "🇲🇶", "French"),
    "597":  ("SR",  "🇸🇷", "Dutch"),
    "598":  ("UY",  "🇺🇾", "Spanish"),
    "599":  ("CW",  "🇨🇼", "Dutch"),
    "7":    ("RU",  "🇷🇺", "Russian"),
    "30":   ("GR",  "🇬🇷", "Greek"),
    "31":   ("NL",  "🇳🇱", "Dutch"),
    "32":   ("BE",  "🇧🇪", "French"),
    "33":   ("FR",  "🇫🇷", "French"),
    "34":   ("ES",  "🇪🇸", "Spanish"),
    "36":   ("HU",  "🇭🇺", "Hungarian"),
    "39":   ("IT",  "🇮🇹", "Italian"),
    "40":   ("RO",  "🇷🇴", "Romanian"),
    "41":   ("CH",  "🇨🇭", "German"),
    "43":   ("AT",  "🇦🇹", "German"),
    "44":   ("GB",  "🇬🇧", "English"),
    "45":   ("DK",  "🇩🇰", "Danish"),
    "46":   ("SE",  "🇸🇪", "Swedish"),
    "47":   ("NO",  "🇳🇴", "Norwegian"),
    "48":   ("PL",  "🇵🇱", "Polish"),
    "49":   ("DE",  "🇩🇪", "German"),
    "298":  ("FO",  "🇫🇴", "Faroese"),
    "299":  ("GL",  "🇬🇱", "Greenlandic"),
    "350":  ("GI",  "🇬🇮", "English"),
    "351":  ("PT",  "🇵🇹", "Portuguese"),
    "352":  ("LU",  "🇱🇺", "Luxembourgish"),
    "353":  ("IE",  "🇮🇪", "English"),
    "354":  ("IS",  "🇮🇸", "Icelandic"),
    "355":  ("AL",  "🇦🇱", "Albanian"),
    "356":  ("MT",  "🇲🇹", "Maltese"),
    "357":  ("CY",  "🇨🇾", "Greek"),
    "358":  ("FI",  "🇫🇮", "Finnish"),
    "359":  ("BG",  "🇧🇬", "Bulgarian"),
    "370":  ("LT",  "🇱🇹", "Lithuanian"),
    "371":  ("LV",  "🇱🇻", "Latvian"),
    "372":  ("EE",  "🇪🇪", "Estonian"),
    "373":  ("MD",  "🇲🇩", "Romanian"),
    "374":  ("AM",  "🇦🇲", "Armenian"),
    "375":  ("BY",  "🇧🇾", "Belarusian"),
    "376":  ("AD",  "🇦🇩", "Catalan"),
    "377":  ("MC",  "🇲🇨", "French"),
    "378":  ("SM",  "🇸🇲", "Italian"),
    "380":  ("UA",  "🇺🇦", "Ukrainian"),
    "381":  ("RS",  "🇷🇸", "Serbian"),
    "382":  ("ME",  "🇲🇪", "Montenegrin"),
    "383":  ("XK",  "🇽🇰", "Albanian"),
    "385":  ("HR",  "🇭🇷", "Croatian"),
    "386":  ("SI",  "🇸🇮", "Slovenian"),
    "387":  ("BA",  "🇧🇦", "Bosnian"),
    "389":  ("MK",  "🇲🇰", "Macedonian"),
    "420":  ("CZ",  "🇨🇿", "Czech"),
    "421":  ("SK",  "🇸🇰", "Slovak"),
    "423":  ("LI",  "🇱🇮", "German"),
    "20":   ("EG",  "🇪🇬", "Arabic"),
    "27":   ("ZA",  "🇿🇦", "English"),
    "211":  ("SS",  "🇸🇸", "English"),
    "212":  ("MA",  "🇲🇦", "Arabic"),
    "213":  ("DZ",  "🇩🇿", "Arabic"),
    "216":  ("TN",  "🇹🇳", "Arabic"),
    "218":  ("LY",  "🇱🇾", "Arabic"),
    "220":  ("GM",  "🇬🇲", "English"),
    "221":  ("SN",  "🇸🇳", "French"),
    "222":  ("MR",  "🇲🇷", "Arabic"),
    "223":  ("ML",  "🇲🇱", "French"),
    "224":  ("GN",  "🇬🇳", "French"),
    "225":  ("CI",  "🇨🇮", "French"),
    "226":  ("BF",  "🇧🇫", "French"),
    "227":  ("NE",  "🇳🇪", "French"),
    "228":  ("TG",  "🇹🇬", "French"),
    "229":  ("BJ",  "🇧🇯", "French"),
    "230":  ("MU",  "🇲🇺", "English"),
    "231":  ("LR",  "🇱🇷", "English"),
    "232":  ("SL",  "🇸🇱", "English"),
    "233":  ("GH",  "🇬🇭", "English"),
    "234":  ("NG",  "🇳🇬", "English"),
    "235":  ("TD",  "🇹🇩", "French"),
    "236":  ("CF",  "🇨🇫", "French"),
    "237":  ("CM",  "🇨🇲", "French"),
    "238":  ("CV",  "🇨🇻", "Portuguese"),
    "239":  ("ST",  "🇸🇹", "Portuguese"),
    "240":  ("GQ",  "🇬🇶", "Spanish"),
    "241":  ("GA",  "🇬🇦", "French"),
    "242":  ("CG",  "🇨🇬", "French"),
    "243":  ("CD",  "🇨🇩", "French"),
    "244":  ("AO",  "🇦🇴", "Portuguese"),
    "245":  ("GW",  "🇬🇼", "Portuguese"),
    "248":  ("SC",  "🇸🇨", "English"),
    "249":  ("SD",  "🇸🇩", "Arabic"),
    "250":  ("RW",  "🇷🇼", "Kinyarwanda"),
    "251":  ("ET",  "🇪🇹", "Amharic"),
    "252":  ("SO",  "🇸🇴", "Somali"),
    "253":  ("DJ",  "🇩🇯", "French"),
    "254":  ("KE",  "🇰🇪", "Swahili"),
    "255":  ("TZ",  "🇹🇿", "Swahili"),
    "256":  ("UG",  "🇺🇬", "English"),
    "257":  ("BI",  "🇧🇮", "French"),
    "258":  ("MZ",  "🇲🇿", "Portuguese"),
    "260":  ("ZM",  "🇿🇲", "English"),
    "261":  ("MG",  "🇲🇬", "Malagasy"),
    "262":  ("RE",  "🇷🇪", "French"),
    "263":  ("ZW",  "🇿🇼", "English"),
    "264":  ("NA",  "🇳🇦", "English"),
    "265":  ("MW",  "🇲🇼", "English"),
    "266":  ("LS",  "🇱🇸", "Sesotho"),
    "267":  ("BW",  "🇧🇼", "English"),
    "268":  ("SZ",  "🇸🇿", "Swati"),
    "269":  ("KM",  "🇰🇲", "Comorian"),
    "290":  ("SH",  "🇸🇭", "English"),
    "291":  ("ER",  "🇪🇷", "Tigrinya"),
    "961":  ("LB",  "🇱🇧", "Arabic"),
    "962":  ("JO",  "🇯🇴", "Arabic"),
    "963":  ("SY",  "🇸🇾", "Arabic"),
    "964":  ("IQ",  "🇮🇶", "Arabic"),
    "965":  ("KW",  "🇰🇼", "Arabic"),
    "966":  ("SA",  "🇸🇦", "Arabic"),
    "967":  ("YE",  "🇾🇪", "Arabic"),
    "968":  ("OM",  "🇴🇲", "Arabic"),
    "970":  ("PS",  "🇵🇸", "Arabic"),
    "971":  ("AE",  "🇦🇪", "Arabic"),
    "972":  ("IL",  "🇮🇱", "Hebrew"),
    "973":  ("BH",  "🇧🇭", "Arabic"),
    "974":  ("QA",  "🇶🇦", "Arabic"),
    "98":   ("IR",  "🇮🇷", "Persian"),
    "60":   ("MY",  "🇲🇾", "Malay"),
    "61":   ("AU",  "🇦🇺", "English"),
    "62":   ("ID",  "🇮🇩", "Indonesian"),
    "63":   ("PH",  "🇵🇭", "Filipino"),
    "65":   ("SG",  "🇸🇬", "English"),
    "66":   ("TH",  "🇹🇭", "Thai"),
    "81":   ("JP",  "🇯🇵", "Japanese"),
    "82":   ("KR",  "🇰🇷", "Korean"),
    "84":   ("VN",  "🇻🇳", "Vietnamese"),
    "86":   ("CN",  "🇨🇳", "Chinese"),
    "91":   ("IN",  "🇮🇳", "Hindi"),
    "92":   ("PK",  "🇵🇰", "Urdu"),
    "93":   ("AF",  "🇦🇫", "Pashto"),
    "94":   ("LK",  "🇱🇰", "Sinhala"),
    "95":   ("MM",  "🇲🇲", "Burmese"),
    "960":  ("MV",  "🇲🇻", "Dhivehi"),
    "975":  ("BT",  "🇧🇹", "Dzongkha"),
    "976":  ("MN",  "🇲🇳", "Mongolian"),
    "977":  ("NP",  "🇳🇵", "Nepali"),
    "992":  ("TJ",  "🇹🇯", "Tajik"),
    "993":  ("TM",  "🇹🇲", "Turkmen"),
    "994":  ("AZ",  "🇦🇿", "Azerbaijani"),
    "995":  ("GE",  "🇬🇪", "Georgian"),
    "996":  ("KG",  "🇰🇬", "Kyrgyz"),
    "998":  ("UZ",  "🇺🇿", "Uzbek"),
    "850":  ("KP",  "🇰🇵", "Korean"),
    "852":  ("HK",  "🇭🇰", "Cantonese"),
    "853":  ("MO",  "🇲🇴", "Cantonese"),
    "855":  ("KH",  "🇰🇭", "Khmer"),
    "856":  ("LA",  "🇱🇦", "Lao"),
    "880":  ("BD",  "🇧🇩", "Bengali"),
    "886":  ("TW",  "🇹🇼", "Chinese"),
    "64":   ("NZ",  "🇳🇿", "English"),
    "670":  ("TL",  "🇹🇱", "Tetum"),
    "673":  ("BN",  "🇧🇳", "Malay"),
    "674":  ("NR",  "🇳🇷", "Nauruan"),
    "675":  ("PG",  "🇵🇬", "English"),
    "676":  ("TO",  "🇹🇴", "Tongan"),
    "677":  ("SB",  "🇸🇧", "English"),
    "678":  ("VU",  "🇻🇺", "Bislama"),
    "679":  ("FJ",  "🇫🇯", "English"),
    "680":  ("PW",  "🇵🇼", "Palauan"),
    "681":  ("WF",  "🇼🇫", "French"),
    "682":  ("CK",  "🇨🇰", "English"),
    "683":  ("NU",  "🇳🇺", "Niuean"),
    "685":  ("WS",  "🇼🇸", "Samoan"),
    "686":  ("KI",  "🇰🇮", "English"),
    "687":  ("NC",  "🇳🇨", "French"),
    "688":  ("TV",  "🇹🇻", "Tuvaluan"),
    "689":  ("PF",  "🇵🇫", "French"),
    "691":  ("FM",  "🇫🇲", "English"),
    "692":  ("MH",  "🇲🇭", "Marshallese"),
    "500":  ("FK",  "🇫🇰", "English"),
    "297":  ("AW",  "🇦🇼", "Papiamento"),
}

service_icons = {
    "whatsapp":  "📱", "telegram": "✈️",  "google":    "🔍",
    "facebook":  "📘", "instagram":"📸",  "twitter":   "🐦",
    "tiktok":    "🎵", "shopee":   "🛒",  "lazada":    "🛍️",
    "grab":      "🚗", "gojek":    "🟢",  "uber":      "🚕",
    "imo":       "💬", "viber":    "📲",  "line":      "💚",
    "snapchat":  "👻", "wechat":   "🟩",  "linkedin":  "💼",
    "amazon":    "📦", "netflix":  "🎬",  "paypal":    "💰",
    "binance":   "🟡", "coinbase": "🔵",  "discord":   "🎮",
    "microsoft": "🪟", "apple":    "🍎",  "yahoo":     "💜",
    "airbnb":    "🏠",
}


def detect_country(phone):
    clean = phone.lstrip('+')
    for code in sorted(country_map.keys(), key=len, reverse=True):
        if clean.startswith(code):
            return country_map[code]
    return ("??", "🌍", "Unknown")


def mask_phone(phone):
    phone = phone.strip()
    if len(phone) >= 10:
        return phone[:5] + "••" + phone[-4:]
    return phone


def extract_otp(message):
    match = re.search(
        r'(?:code|كود|رمز|código|код|验证码|verification code|'
        r'WhatsApp code|code is|OTP|pin|kode|passcode|'
        r'confirmation code|access code|security code)[\s\W:-]*(\d{3,8})',
        message, re.IGNORECASE | re.UNICODE
    )
    if match:
        return re.sub(r'[- ]', '', match.group(1))
    match = re.search(r'\b(\d{4,8})\b', message)
    return re.sub(r'[- ]', '', match.group(1)) if match else "N/A"


def get_service_icon(app_name):
    name = app_name.lower()
    for key, icon in service_icons.items():
        if key in name:
            return icon
    return "💬"


def fetch_sms():
    try:
        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"❌ API fetch failed: {e}")
        return []


def parse_timestamp(ts_str):
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None


def build_otp_message(app, phone, full_msg):
    country_code, flag, language = detect_country(phone)
    masked   = mask_phone(phone)
    otp      = extract_otp(full_msg)
    svc_icon = get_service_icon(app)
    text     = f"{flag} {country_code} | {svc_icon} {masked} | 🌐 {language}"
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔔 Channel ↗", url=f"https://t.me/{CHANNEL_USERNAME}"),
            InlineKeyboardButton(f"🛡 📋 {otp}", callback_data=f"otp_{otp}"),
        ],
        [
            InlineKeyboardButton("📞 Get Number ↗", url=GET_NUMBER_URL),
        ]
    ])
    return text, keyboard, otp


# ── Command handlers ──────────────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "🤖 *CrimeOTP Bot is ACTIVE!* ✅\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📡 Fetching OTPs every *40 seconds*\n"
        "🌍 Supporting *200+ countries*\n"
        "📱 Supporting *30+ services*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 *Commands:*\n"
        "/start — Check bot status\n"
        "/test — Send a sample OTP message\n"
        "/status — Check API connection\n\n"
        "📣 Join: @crimeotpnumbers"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Sending sample OTP to channel...")

    sample_entries = [
        ("WhatsApp", "+923312345678", "Your WhatsApp code is 456-789. Don't share it."),
        ("WhatsApp", "+628812345678", "Kode WhatsApp Anda 170-854. Jangan bagikan."),
        ("Google",   "+919876543210", "Your Google verification code is 234567"),
        ("Shopee",   "+628891234567", "Shopee OTP: 8823. Valid 5 minutes."),
        ("Telegram", "+447712345678", "Your Telegram code: 12345"),
    ]

    bot = context.bot
    for app, phone, msg in sample_entries:
        text, keyboard, otp = build_otp_message(app, phone, msg)
        try:
            await bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=text,
                reply_markup=keyboard
            )
            print(f"✅ Test sent: {phone} | OTP: {otp}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Test failed: {e}")

    await update.message.reply_text("✅ 5 sample OTPs sent to channel! Check @crimeotpnumbers")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Checking API connection...")
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
        count = len(data) if isinstance(data, list) else 0
        await update.message.reply_text(
            f"✅ *API Connected!*\n\n"
            f"📊 OTPs in panel: *{count}*\n"
            f"🌐 API URL: `{API_URL}`\n"
            f"⚡ Status: Online",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ *API Error!*\n\n`{e}`", parse_mode="Markdown")


# ── OTP polling loop ──────────────────────────────────────────

async def otp_polling(bot: Bot):
    last_seen_time = None
    print("✅ OTP Bot Started — checking every 40 seconds...")

    while True:
        entries = fetch_sms()

        if not entries:
            await asyncio.sleep(40)
            continue

        new_entries = []

        if last_seen_time is None:
            new_entries    = entries[:8]
            first_ts       = parse_timestamp(new_entries[0][3]) if new_entries else None
            last_seen_time = first_ts
        else:
            for entry in entries:
                ts = parse_timestamp(entry[3])
                if ts and ts > last_seen_time:
                    new_entries.append(entry)

        if new_entries:
            latest = parse_timestamp(new_entries[0][3])
            if latest:
                last_seen_time = latest
            print(f"📨 {len(new_entries)} new OTP(s) | Latest: {new_entries[0][3]}")

        for entry in reversed(new_entries):
            app      = entry[0].strip()
            phone    = entry[1].strip()
            full_msg = entry[2].strip()
            text, keyboard, otp = build_otp_message(app, phone, full_msg)
            try:
                await bot.send_message(
                    chat_id=TELEGRAM_GROUP_ID,
                    text=text,
                    reply_markup=keyboard
                )
                print(f"✅ Sent → {mask_phone(phone)} | OTP: {otp}")
            except Exception as e:
                print(f"❌ Send failed: {e}")

        await asyncio.sleep(40)


# ── Main ──────────────────────────────────────────────────────

async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",  start_command))
    app.add_handler(CommandHandler("test",   test_command))
    app.add_handler(CommandHandler("status", status_command))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    print("✅ Bot commands active!")

    await otp_polling(app.bot)


if __name__ == "__main__":
    asyncio.run(main())
