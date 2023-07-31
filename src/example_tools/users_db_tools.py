# Import things that are needed generically
from langchain.tools import BaseTool
from shapely import from_wkt
from typing import Any, Optional
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from .users_database import UsersDb

class AddUserTool(BaseTool):
    """Allows adding a user to the farmers' database.
    """
    name = "add_user"

    description = "use this tool when you need to add a user to the database.\
                   You should ask the user for his full name and email. After adding the user you should \
                    tell them that they can now add a plot or a vegetation bed."

    def _run(self, full_name:str, email:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_user(full_name, email)
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class AddPlotTool(BaseTool):
    """Allows adding a plot to a specific user in the database.
    """
    name = "add_plot"

    description = "use this tool when you need to add a plot to the database using a user email.\
                   you should ask the user for their email.\
                   you should add a user to the database only if their email is not in the database.\
                   Don't add the user again if their email is already in the database."

    def _run(self, name:str, delimitation:str, email:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_plot(name, delimitation, email)
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class AddVegetationBedTool(BaseTool):
    """Allows adding a vegetation bed to a specific user in the databse.
    """
    name = "add_veg_bed"

    description = "use this tool when you need to add a veg_bed to the database.\
                   you should ask the user for their email.\
                   you should add a user to the database only if their email is not in the database.\
                   Don't add the user again if their email is already in the database."

    def _run(self, name:str, delimitation:str, email:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_plot(name, delimitation, email)
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class AddPlotSeasonTool(BaseTool):
    """Allows adding a plot season to a users' plot in the database.
    """
    name = "add_plot_season"

    description = "use this tool when you need to add a plot season to the database. \
                    The plot should already exist.\
                    Ask the user if they want to add the plot if you can't find it."

    def _run(self, start_date:str, end_date:str, variety_name:str, plot_name:str, email:str,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_plot_season(start_date, end_date, variety_name, plot_name, email)
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class AddPlantSeasonTool(BaseTool):
    """Allows adding a specific season to a single or multiple plants in the database for a vegetation bed.
    """
    name = "add_plant_season"

    description = "use this tool when you need to add the plant season to the database.\
                    The vegetation bed should already exist.\
                    Ask the user if they want to add the vegetation bed if you can't find it. "

    def _run(self, start_date:str, end_date:str, position:str, variety_name:str, veg_bed_name:str, email:str,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_plant_season(start_date, end_date, position, variety_name, veg_bed_name, email)
    
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
class AddSpeciesTool(BaseTool):
    """Allows adding new species to the database.
    """
    name = "add_species"

    description = "use this tool when you need to add species to the database.\
                   Check if the species already exist before adding them."

    def _run(self, name:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_species(name)
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class AddVarietyTool(BaseTool):
    """Allows adding a new variety to the database.
    """
    name = "add_variety"

    description = "use this tool to add varieties to the database.\
                   Check if the varieties already exist before adding them."

    def _run(self, variety_name:str, species_name:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.add_variety(variety_name, species_name)
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class FetchPolygonWkt(BaseTool):
    """Allows converting a polygon to wkt -well known text- format.
    """
    name = 'polygon_wkt'

    description = 'use this tool when you want to convert polygons in the database to text format.'

    def _run(self, name:str, user_email:str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Any:
        """Use the tool."""
        users_db = UsersDb()
        users_db.get_plot_wkt(name, user_email)
    async def _arun(self):
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
