from bots.adminbot import admin_handlers
from bots.convobot import conversation_handler
from bots.feedbackbot import feedback_conversation
from bots.funbot import fun_command_handlers
from bots.userbot import user_command_handlers

all_handlers = [
    *user_command_handlers,
    conversation_handler,
    *admin_handlers,
    feedback_conversation,
    *fun_command_handlers,
]
