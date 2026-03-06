import os
import telebot
from yt_dlp import YoutubeDL

# তোমার বটের টোকেন
API_TOKEN = '8702844610:AAGPtr8EGNHq7Fzs-mYynUAsYKpdSRYwaZk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    # বিভিন্ন প্ল্যাটফর্মের লিঙ্ক চেক করা
    platforms = ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "tiktok.com"]
    
    if any(platform in url for platform in platforms):
        bot.reply_to(message, "ভিডিওটি বিশ্লেষণ করা হচ্ছে... ⏳")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'playlist_items': '1-10', # সর্বোচ্চ ১০টি ভিডিওর সীমাবদ্ধতা
                'quiet': True,
                'no_warnings': True
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # প্লেলিস্ট নাকি সিঙ্গেল ভিডিও চেক করা
                if 'entries' in info:
                    videos = info['entries']
                    bot.reply_to(message, f"প্লেলিস্ট পাওয়া গেছে! প্রথম ১০টি ভিডিও প্রসেস হচ্ছে... 📚")
                else:
                    videos = [info]

                for index, video in enumerate(videos):
                    # ইউজারকে আপডেট দেওয়া
                    if len(videos) > 1:
                        bot.send_message(message.chat.id, f"ভিডিও {index+1}/{len(videos)} আপলোড হচ্ছে... 📤")
                    
                    file_name = ydl.prepare_filename(video)
                    title = video.get('title', 'Video')
                    
                    # ক্যাপশন তৈরি
                    caption_text = f"🎬 **Title:** {title}\n\n📥 **Downloaded by:** @Dhumketu_Cyber_Community_Bot"
                    
                    if os.path.exists(file_name):
                        with open(file_name, 'rb') as v:
                            bot.send_video(message.chat.id, v, caption=caption_text, parse_mode='Markdown')
                        os.remove(file_name) # মেমোরি ক্লিয়ার করা

        except Exception as e:
            bot.reply_to(message, f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

bot.polling()
