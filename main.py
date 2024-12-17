import telebot
import os
import subprocess

# توكن البوت
TOKEN = '6756113703:AAF4L6hr6flqP26_lqZUfRa5gney40jLRz0'
# الايدي الخاص بك (Admin ID)
ADMIN_ID = 7243681318
# قائمة الأدمن (يمكن تخزينها في ملف أو قاعدة بيانات)
admins = [ADMIN_ID]

# إنشاء البوت باستخدام التوكن
bot = telebot.TeleBot(TOKEN)

# دالة للتحقق إذا كان المستخدم أدمن
def is_admin(user_id):
    return user_id in admins

# تنفيذ الأوامر على النظام
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# التعامل مع الرسائل الواردة
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! يمكنك إرسال أوامر النظام هنا. فقط تذكر أن تكون أدمن!")

# التعامل مع أوامر إضافة وحذف الأدمن
@bot.message_handler(commands=['add', 'delete'])
def manage_admins(message):
    if is_admin(message.from_user.id):
        cmd = message.text.split()
        if len(cmd) == 2:
            action = cmd[0]
            user_id = int(cmd[1])

            if action == '/add':
                if user_id not in admins:
                    admins.append(user_id)
                    bot.reply_to(message, f"تم إضافة {user_id} كأدمن.")
                else:
                    bot.reply_to(message, "هذا المستخدم هو بالفعل أدمن.")
            elif action == '/delete':
                if user_id in admins:
                    admins.remove(user_id)
                    bot.reply_to(message, f"تم حذف {user_id} من الأدمن.")
                else:
                    bot.reply_to(message, "هذا المستخدم ليس أدمن.")
        else:
            bot.reply_to(message, "استخدم الأمر بالشكل الصحيح: /add + id أو /delete + id")
    else:
        bot.reply_to(message, "ليس لديك صلاحيات لإضافة أو حذف أدمن.")

# التعامل مع الأوامر المرسلة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if is_admin(message.from_user.id):
        # تنفيذ الأوامر في النظام
        command = message.text
        output = execute_command(command)
        bot.reply_to(message, output)
    else:
        bot.reply_to(message, "ليس لديك صلاحيات لتنفيذ الأوامر.")

# بدء البوت
bot.polling()
