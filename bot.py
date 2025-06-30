import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("📎 أرسل رابط فيديو صالح.")
        return
    await message.reply("🔄 جاري التحميل...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'بدون عنوان')
            description = info.get('description', '❌ لا يوجد وصف.')
            filename = ydl.prepare_filename(info)

        await bot.send_video(
            message.chat.id,
            video=InputFile(filename),
            caption=f"🎬 <b>{title}</b>\n\n📝 <i>{description}</i>",
            parse_mode="HTML"
        )
        os.remove(filename)

    except Exception as e:
        await message.reply(f"❌ خطأ:\n<code>{e}</code>", parse_mode="HTML")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
