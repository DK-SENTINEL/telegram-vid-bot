import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('হ্যালো! আমাকে ফেসবুক, ইনস্টাগ্রাম, টিকটক বা ইউটিউবের ভিডিও লিংক দিন।')

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "http" in url:
        await update.message.reply_text('ভিডিও ডাউনলোড হচ্ছে, একটু অপেক্ষা করুন... ⏳')
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_video.mp4'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('downloaded_video.mp4', 'rb') as video_file:
                await update.message.reply_video(video=video_file)
            os.remove('downloaded_video.mp4')
        except Exception as e:
            await update.message.reply_text('দুঃখিত, এই লিংক থেকে ভিডিওটি ডাউনলোড করা সম্ভব হচ্ছে না।')
    else:
        await update.message.reply_text('দয়া করে একটি সঠিক ভিডিও লিংক দিন।')

def main():
    app = Application.builder().token("8702844610:AAGPtr8EGNHq7Fzs-mYynUAsYKpdSRYwaZk").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    print("বট চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
