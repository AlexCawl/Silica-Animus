from config import *
from Standart import StandartModule
from Directory import DirectoryModule
from Rating import RatingModule
from Survey import SurveyModule


if __name__ == "__main__":
    db.create(User, Role, Survey, Directory)
    bot.add_cog(StandartModule(bot))
    bot.add_cog(DirectoryModule(bot))
    bot.add_cog(RatingModule(bot))
    bot.add_cog(SurveyModule(bot))
    bot.run(bot_token)