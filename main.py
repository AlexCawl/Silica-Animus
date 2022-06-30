from config import *
from modules import *


if __name__ == "__main__":
    db.create()
    bot.add_cog(Standart(bot))
    bot.add_cog(Directory(bot))
    bot.add_cog(Rating(bot))
    bot.add_cog(Survey(bot))
    bot.run(bot_token)