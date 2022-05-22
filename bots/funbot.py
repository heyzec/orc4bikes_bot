import logging
import random
import requests
from requests.exceptions import RequestException, JSONDecodeError

from telegram import (
    ChatAction,
)
from telegram.ext import (
    CommandHandler,
)

from bot_text import (
    CHEER_LIST,
    FUN_TEXT,
    FUN_URLS,
    OHNO_LIST,
    OHYES_LIST,
)

logger = logging.getLogger()


def fun_command(update, context):
    """Show user list of fun commands."""
    update.message.reply_text(FUN_TEXT)

def get_pic_url(l):
    """Repeated tries a list of URLs"""
    while len(l) != 0:
        url, key = l.pop(0)
        try:
            img_url = requests.get(url).json()[key]
            return img_url
        except (RequestException, JSONDecodeError) as e:
            logger.exception(e)
    return None

def chat_action(action):
    def decorator(func):
        def new_func(update, context, *args, **kwargs):
            update.message.reply_chat_action(action)
            return func(update, context, *args, **kwargs)
        return new_func
    return decorator


def send_user(
        update, context, *,
        pic_url,
        caption,
        error_text):
    """Replies user with either a photo or an error message"""
    if not pic_url:
        update.message.reply_text(error_text)
        return

    update.message.reply_photo(
        photo=pic_url,
        caption=caption)

@chat_action(ChatAction.TYPING)
def doggo_command(update, context):
    """Shows you a few cute dogs!"""
    pic_url = get_pic_url(FUN_URLS['dog'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, all the dogs are out playing... Please try again later!")

@chat_action(ChatAction.TYPING)
def shibe_command(update, context):
    """Shows you a few cute shibe!"""
    pic_url = get_pic_url(FUN_URLS['shibe'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, doge is doge... Please try again later!")

@chat_action(ChatAction.TYPING)
def neko_command(update, context):
    """Shows you a few cute cats!"""
    pic_url = get_pic_url(FUN_URLS['neko'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, all the cats are asleep... Please try again later!")

@chat_action(ChatAction.TYPING)
def kitty_command(update, context):
    """Shows you a few cute kittens!"""
    pic_url = get_pic_url(FUN_URLS['cat'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, all the cats are asleep... Please try again later!")

@chat_action(ChatAction.TYPING)
def foxy_command(update, context):
    """Shows you a few cute foxes!"""
    pic_url = get_pic_url(FUN_URLS['fox'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, all the foxes are asleep... Please try again later!")

@chat_action(ChatAction.TYPING)
def birb_command(update, context):
    """Shows you a few cute birbs!"""
    pic_url = get_pic_url(FUN_URLS['bird'])
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Sorry, the birbs flew away... Please try again later!")

def get_random_pic():
    return get_pic_url(random.choice(list(FUN_URLS.values())))

@chat_action(ChatAction.TYPING)
def random_command(update, context):
    """Sends a random animal!"""
    pic_url = get_random_pic()
    send_user(
        update, context,
        pic_url=pic_url,
        caption=random.choice(CHEER_LIST),
        error_text="Hmm, I can't seem to find any animals... Maybe they're all asleep?")

@chat_action(ChatAction.CHOOSE_STICKER)
def pika_command(update, context):
    """Sends a pikachu sticker"""
    if random.random() < 0.1:
        update.message.reply_text("Pika... boo? 🙂")
        return
    PIKA_LIST = [
        'pikachu',
        'pikachu2',
        'PikachuDetective',
        'pikachu6',
        'pikach',
        'pikach_memes',
    ]
    pikas = []
    for pika in PIKA_LIST:
        pikas.extend(context.bot.get_sticker_set(pika).stickers)
    pikas.extend(context.bot.get_sticker_set('uwumon').stickers[:20])
    pika = random.choice(pikas)
    update.message.reply_sticker(sticker=pika)

def quote_command(update, context):
    """Sends an inspirational quote"""
    try:
        url = requests.get('https://type.fit/api/quotes').json()
    except RequestException as e:
        logger.exception(e)
        update.message.reply_text(random.choice(CHEER_LIST))
    else:
        url = random.choice(url)
        update.message.reply_text(
            f'"{url["text"]}" - {url["author"]}')

@chat_action(ChatAction.CHOOSE_STICKER)
def brawl_command(update, context):
    """Sends a brawl stars sticker"""
    brawls = context.bot.get_sticker_set('BrawlStarsbyHerolias')
    brawl = random.choice(brawls.stickers)
    update.message.reply_sticker(sticker=brawl)

@chat_action(ChatAction.CHOOSE_STICKER)
def bangday_command(update, context):
    """Sends a bang don sticker"""
    bangdongs = context.bot.get_sticker_set('happybangday')
    bangdong = random.choice(bangdongs.stickers)
    update.message.reply_sticker(sticker=bangdong)

def ohno_command(update, context):
    """Sends a version of "Oh no"..."""
    text = random.choice(OHNO_LIST)
    update.message.reply_text(text)
    raise ZeroDivisionError("This function is for testing. If you see this line, that means"
                            " a mock error has been triggered.")

def ohyes_command(update, context):
    """Sends a version of "Oh yes"..."""
    text = random.choice(OHYES_LIST)
    update.message.reply_text(text)
    logger.info("YAYYYY!")


fun_command_handler = CommandHandler('fun', fun_command)
doggo_command_handler = CommandHandler('doggo', doggo_command)
neko_command_handler = CommandHandler('neko', neko_command)
kitty_command_handler = CommandHandler('kitty', kitty_command)
birb_command_handler = CommandHandler('birb', birb_command)
shibe_command_handler = CommandHandler('shibe', shibe_command)
foxy_command_handler = CommandHandler('foxy', foxy_command)
random_command_handler = CommandHandler('random', random_command)

pika_command_handler = CommandHandler('pika', pika_command)                # pika sticker
brawl_command_handler = CommandHandler('brawl', brawl_command)             # brawl sticker
bangday_command_handler = CommandHandler('happybangday', bangday_command)  # bangday sticker

ohno_command_handler = CommandHandler('ohno', ohno_command)
ohyes_command_handler = CommandHandler('ohyes', ohyes_command)

# quote_command_handler = CommandHandler('quote', quote_command)  # doesn't work on web...

fun_command_handlers = [
    fun_command_handler,
    doggo_command_handler,
    neko_command_handler,
    kitty_command_handler,
    birb_command_handler,
    shibe_command_handler,
    foxy_command_handler,
    random_command_handler,
    pika_command_handler,
    brawl_command_handler,
    bangday_command_handler,
    ohno_command_handler,
    ohyes_command_handler,
]
