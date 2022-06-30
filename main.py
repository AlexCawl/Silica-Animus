from BotEvents import *
from BotRoles import *
from BotRating import *
from BotDirectory import *
from BotStrange import *
from BotSurvey import *


if __name__ == "__main__":
    db_create()
    bot.run(bot_token)