from functools import wraps

from telegram import ChatAction


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def new_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=action)
            return func(update, context, *args, **kwargs)
        return new_func
    return decorator

send_typing_action = send_action(ChatAction.TYPING)
