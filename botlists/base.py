import aiohttp
from typing import Union

from .exceptions import *

API_BASE = "https://botblock.org/api/"

class Base:
    """
    This class is used to directly interact with the botblock.org API via http requests.
    """
    
    def __init__(self):
        self.base = API_BASE
        self.session = None
        self.auth = {}
        
    def _session_init(self):
        """
        Starts up the aiohttp session if one does not exist.
        """
        
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
    def _headers(self) -> dict:
        """
        Gets standard headers used in an API request.
        
        Returns
        -------
        json: dict
            The http request headers.
        """
        
        return {
            "content-type": "application/json"
        }
        
    async def _handle_response(self, resp: aiohttp.ClientResponse) -> dict:
        """
        Handles all responses returned from any API request.
        
        Parameter
        ---------
        resp: aiohttp.ClientResponse
            The raw response from the aiohttp request to the API.
            
        Returns
        -------
        json: dict
            The formatted response from the API endpoint.
        """
        
        status = resp.status
        
        text = await resp.text()
        
        try:
            json = await resp.json()
        except:
            json = {}
            
        if json == {} and text.strip() == "":
            raise EmptyResponseException()
        
        if status == 429:
            raise RateLimitException(json)
        
        if status != 200:
            raise RequestFailureException(status, text)
        
        return json
    
    async def _post(self, endpoint: str, content: Union[list, dict]) -> dict:
        """
        POST data to an API endpoint.
        
        Parameter
        ---------
        endpoint: str
            The endpoint to access on the API.
        content: Union[list, dict]
            The data to be posted to the endpoint.
            
        Returns
        -------
        json: dict
            The formatted response from the API endpoint.
        """
        
        self._session_init()
        
        async with self.session.post(url=self.base + endpoint, json=content, headers=self._headers()) as resp:
            return await self._handle_response(resp)
        
    async def _get(self, endpoint: str) -> dict:
        """
        GET data from an API endpoint.
        
        Parameter
        ---------
        endpoint: str
            The endpoint to access on the API.
        
        Returns
        -------
        json: dict
            The formatted response from the API endpoint.
        """
        
        self._session_init()
        
        async with self.session.get(url=self.base + endpoint, headers=self._headers()) as resp:
            return await self._handle_response(resp)
        
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
        
        self.auth[list_id] = auth_token
        
    def remove_creds(self, list_id: str):
        """
        Removes an authorization token for the given list ID from botblock.org.
        
        Parameter
        ---------
        list_id: str
            The ID of the list from botblock.org.
        """
        
        if list_id in self.auth.keys():
            del self.auth[list_id]
            
    def _guild_count_body(self, bot_id: int, guild_count: int) -> dict:
        """
        Gets the body used for a server/guild count post API request.
        
        Parameter
        ---------
        bot_id: int
            The ID of the bot you want to update server/guild count for.
        guild_count: int
            The server/guild count for the bot.
            
        Returns
        -------
        json: dict
            The json body to send.
        """
        
        data = self.auth.copy()
        
        data["server_count"] = guild_count
        data["bot_id"] = str(bot_id)
        
        return data
    
    async def post_guild_count(self, bot_id: int, guild_count: int) -> dict:
        """
        POST server/guild count for a bot.
        
        Parameter
        ---------
        bot_id: int
            The ID of the bot you want to update server/guild count for.
        guild_count: int
            The server/guild count for the bot.
            
        Returns
        -------
        json: dict
            The response from the API endpoint.
        """
        
        return await self._post("count", self._guild_count_body(bot_id, guild_count))
    
    async def get_bot_info(self, bot_id: int) -> dict:
        """
        GET information about a bot.
        
        Parameter
        ---------
        bot_id: int
            The ID of the bot you want to fetch from the API.
        
        Returns
        -------
        json: dict
            The response from the API endpoint.
        """
        
        return await self._get("bots/{}".format(bot_id))
    