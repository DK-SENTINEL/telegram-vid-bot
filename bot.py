import os
import telebot
from yt_dlp import YoutubeDL

# তোমার বটের টোকেন
API_TOKEN = '8702844610:AAGPtr8EGNHq7Fzs-mYynUAsYKpdSRYwaZk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    # সমর্থিত প্ল্যাটফর্মের তালিকা
    platforms = ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "tiktok.com"]
    
    if any(platform in url for platform in platforms):
        bot.reply_to(message, "ভিডিওটি বিশ্লেষণ করা হচ্ছে... ⏳")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'playlist_items': '1-10', # সর্বোচ্চ ১০টি ভিডিও
                'quiet': True,
                'no_warnings': True
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # চেক করা হচ্ছে এটি প্লেলিস্ট কি না
                if 'entries' in info:
                    videos = info['entries']
                    bot.reply_to(message, f"প্লেলিস্ট পাওয়া গেছে! প্রথম {len(videos)}টি ভিডিও প্রসেস হচ্ছে... 📚")
                else:
                    videos = [info]

                for index, video in enumerate(videos):
                    # ইউজারকে প্রগ্রেস জানানো
                    if len(videos) > 1:
                        bot.send_message(message.chat.id, f"ভিডিও {index+1}/{len(videos)} আপলোড হচ্ছে... 📤")
                    
                    file_name = ydl.prepare_filename(video)
                    title = video.get('title', 'Video')
                    
                    # টাইটেল থেকে স্পেশাল ক্যারেক্টার ক্লিন করা (এরর এড়াতে)
                    safe_title = title.replace('_', ' ').replace('*', ' ').replace('[', ' ').replace(']', ' ')
                    
                    # সুন্দর ক্যাপশন
                    caption_text = f"🎬 Title: {safe_title}\n\n📥 Downloaded by: @Dhumketu_Cyber_Community_Bot"
                    
                    if os.path.exists(file_name):
                        with open(file_name, 'rb') as v:
                            # এখানে parse_mode বাদ দেওয়া হয়েছে যাতে স্পেশাল ক্যারেক্টারে এরর না আসে
                            bot.send_video(message.chat.id, v, caption=caption_text)
                        
                        # ফাইল মুছে ফেলা (স্টোরেজ বাঁচানোর জন্য)
                        os.remove(file_name)

        except Exception as e:
            bot.reply_to(message, f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

bot.polling()
