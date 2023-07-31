# Import things that are needed generically
from langchain.tools import BaseTool
from shapely import from_wkt
from typing import Any, Optional
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from .gee import S2Data
from .users_database import UsersDb

class S2SearchTool(BaseTool):
    """Allows generating NDVI or NDWI maps using Sentinel 2 constellation for a plot in wkt -well known text- format.
    """
    name = "s2_image"

    description = "don't use this for plots in the database.\
                   use this tool when you need to return a vegetation index map from sentinel2 satellite imagery. \
                   the user needs to give you a Polygon or MultiPolygon of their farm or plot and a range of dates.\
                    "

    def _run(self, polygon:str, vi:str, start_date:str, end_date:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        s2_data = S2Data(start_date, end_date, vi)
        s2_data.map_result(from_wkt(polygon))
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class S2SearchDbTool(BaseTool):
    """Allows generating NDVI or NDWI maps using Sentinel 2 constellation for a plot in the farmers database.
    """

    name = "database_s2_image"

    description = "use this tool when you need to look for a plot in the database and return a vegetation index map \
                   from sentinel2 satellite imagery. \
                   the user provides an email address.\
                   check the database for wkt format of the polygon using the plot name.\
                   a date range should be provided."

    def _run(self, plot_name:str, user_email:str, vi:str, start_date:str, end_date:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        try:
            polygon = users_db.get_plot_wkt(plot_name, user_email)
        except:
            raise ValueError('Check the requested plot and user')
        
        s2_data = S2Data(start_date, end_date, vi)
        s2_data.map_result(from_wkt(polygon))
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")