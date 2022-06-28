import asyncio
from typing import Tuple, Union

from discord import User

from .base import Base
from .exceptions import NotFoundException

class Client:
    """
    This class is used to interact with the botblock.org API using discord.py bot instance.
    
    Parameters
    ----------
    bot:
        An instance of a discord.pt Bot or Client object.
    interval: int[Optional]
        Seconds between each automatic posting of server/guild count. Defaults to 1800 seconds (30 minutes).
    """
    
    def __init__(self, bot, interval: int = 30 * 60):
        self.bot = bot
        self.interval = interval
        self.base = Base()
        
    @property
    def guild_count(self) -> int:
        """
        Gets the guild count from the bot.
        
        Returns
        -------
        count: int
            The current number of guilds the bot is in.
        """
        
        try:
            count = len(self.bot.guilds)
        except AttributeError:
            count = len(self.bot.servers)
            
        return count
    
    @property
    def server_count(self) -> int:
        """
        Gets the server count from the bot.
        
        Returns
        -------
        count: int
            The current number of servers the bot is in.
        """
        
        return self.guild_count
    
    def set_creds(self, list_id: str, auth_token: str):
        """
        Sets an authorization token for the given list ID from botblock.org.
        
        Parameter
        ---------
        list_id: str
            The ID of the list from botblock.org.
        auth_token: str
            The authorization token this list provided you to use their API.
        """
        
        self.base.set_creds(list_id, auth_token)
        
    def remove_creds(self, list_id: str):
        """
        Removes an authorization token for the given list ID from botblock.org.
        
        Parameter
        ---------
        list_id: str
            The ID of the list from botblock.org.
        """
        
        self.base.remove_creds(list_id)
        
    async def post_count(self) -> dict:
        """
        POST current server/guild count based on bot data.
        
        Returns
        -------
        json: dict
            The response from the API endpoint.
        """
        
        return await self.base.post_guild_count(self.bot.user.id, self.guild_count)
    
    def start_loop(self):
        """
        Start a loop that automatically updates the server/guild count for the bot.
        """
        
        self.bot.loop.create_task(self._loop(self.interval))
        
    async def _loop(self, interval: float):
        """
        The internal loop used for automatically post server/guild count stats.
        """
        
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.post_count()
            await asyncio.sleep(interval)
            
    async def get_bot(self, bot_id: int) -> Tuple[Union[User, None], dict]:
        """
        Get information about a bot.
        
        Parameter
        ---------
        bot_id: int
            The ID of the bot you want to fetch from the API.
            
        Returns
        -------
        user: Union[User, None]
            The User object from discord.py if found or None.
        json: dict
            The response from the API endpoint.
        """
        
        try:
            user_info = await self.bot.get_user_info(str(bot_id))
        except AttributeError:
            user_info = await self.bot.fetch_user(bot_id)
        except:
            user_info = None
            
        api_result = await self.base.get_bot_info(bot_id)
        
        if user_info and api_result:
            api_result['username'] = user_info.name
            api_result['discriminator'] = str(user_info.discriminator)
            
        if not user_info and not api_result['username']:
            raise NotFoundException()
        
        return (user_info, api_result)
        