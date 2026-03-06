import os
import telebot
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# তোমার বটের টোকেন
API_TOKEN = '8702844610:AAGPtr8EGNHq7Fzs-mYynUAsYKpdSRYwaZk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url:
        bot.reply_to(message, "ভিডিওটি প্রসেস হচ্ছে, দয়া করে অপেক্ষা করুন... ⏳")
        
        try:
            # ভিডিও ডাউনলোড সেটিংস (দ্রুত প্রসেসিংয়ের জন্য 480p রেজোলিউশন)
            ydl_opts = {
                'format': 'best[height<=480]', 
                'outtmpl': 'video.mp4'
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # ভিডিও লোড করা
            video = VideoFileClip("video.mp4")
            
            # লোগো সেটআপ (ভিডিওর প্রস্থের ১৫% সাইজ এবং ওপরের ডান কোণায় পজিশন)
            logo = (ImageClip("logo.png")
                    .set_duration(video.duration)
                    .resize(width=video.w * 0.15) 
                    .margin(right=10, top=10, opacity=0) 
                    .set_pos(("right", "top")))

            # ভিডিও এবং লোগো যুক্ত করা
            final_video = CompositeVideoClip([video, logo])
            
            # নতুন ভিডিও ফাইল তৈরি (রেন্ডারিং)
            final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")

            # ভিডিও পাঠানো
            with open("output.mp4", 'rb') as v:
                bot.send_video(message.chat.id, v)

            # ফাইলগুলো মুছে ফেলা (যাতে মেমোরি ফুল না হয়)
            video.close()
            final_video.close()
            os.remove("video.mp4")
            os.remove("output.mp4")

        except Exception as e:
            bot.reply_to(message, f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

bot.polling()
