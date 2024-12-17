import telebot
import subprocess
import os
import zipfile

bot = telebot.TeleBot("6756113703:AAGM6-gxSF93t1pPIiPFL7kpXmDNObNKXas")
BASE_UPLOAD_DIR = "uploaded_files"
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)
@bot.message_handler(commands=['start'])
def welcome_user(message):
    markup = telebot.types.InlineKeyboardMarkup()
    upload_btn = telebot.types.InlineKeyboardButton("📤 رفع ملف", callback_data="upload")
    install_btn = telebot.types.InlineKeyboardButton("📦 تحميل مكتبة", callback_data="install")
    markup.add(upload_btn, install_btn)
    bot.reply_to(message, "اهلا بك عزيزي المستخدم", reply_markup=markup)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        user_id = str(message.from_user.id)
        user_dir = os.path.join(BASE_UPLOAD_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        if not (file_name.endswith('.py') or file_name.endswith('.zip')):
            bot.reply_to(message, "• ارسل ملف مضغوط او .py")
            return
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(user_dir, file_name)

        with open(file_path, 'wb') as file:
            file.write(downloaded_file)
        
        bot.reply_to(message, "✅ تم تحميل الملف بنجاح!")
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(user_dir)
            bot.reply_to(message, "📂 تم فك ضغط الملف بنجاح!")
        
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء معالجة الملف: {str(e)}")
@bot.message_handler(func=lambda message: message.text == "📦 تحميل مكتبة")
def request_library_name(message):
    bot.reply_to(message, "📝 أرسل اسم المكتبة التي تريد تحميلها:")

@bot.message_handler(func=lambda message: True)
def install_library(message):
    if message.text.startswith("pip install"):
        bot.reply_to(message, "❌ لا تحتاج لإدخال الأمر كامل. فقط أرسل اسم المكتبة.")
        return
    
    library_name = message.text.strip()
    if library_name:
        bot.reply_to(message, f"⏳ جاري تحميل المكتبة: {library_name}")
        try:
            result = subprocess.run(["pip", "install", library_name], capture_output=True, text=True)
            if result.returncode == 0:
                bot.reply_to(message, f"✅ تم تحميل المكتبة {library_name} بنجاح!")
            else:
                bot.reply_to(message, f"❌ حدث خطأ أثناء تحميل المكتبة:\n{result.stderr}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")
@bot.callback_query_handler(func=lambda call: call.data == "upload")
def handle_upload_button(call):
    bot.send_message(call.message.chat.id, "📝 الرجاء إرسال الملف الذي تريد رفعه.")

@bot.callback_query_handler(func=lambda call: call.data == "install")
def handle_install_button(call):
    bot.send_message(call.message.chat.id, "📝 أرسل اسم المكتبة التي تريد تحميلها:")
bot.polling()