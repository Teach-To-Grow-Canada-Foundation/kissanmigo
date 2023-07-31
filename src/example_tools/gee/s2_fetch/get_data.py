from ..config import config
import numpy as np
from shapely.geometry import MultiPolygon, Polygon
import matplotlib.pyplot as plt
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from datetime import datetime

ee = config()
        


class S2Data:
    """Class enabling to retrieve satellite imagery data.
    """
    def __init__(self, start_date, end_date, vi, dataset='COPERNICUS/S2_SR_HARMONIZED'):
        self.start = start_date
        self.end = end_date
        self.dataset = dataset
        self.vi = vi

    @staticmethod
    def geometry_to_polygon(geometry, ee):
        """Method allowing to convert a geometry to google earth engine polygon or multipolygon format.

        Args:
            geometry (shapely.geometry.Polygon or shapely.geometry.MultiPolygon): Sheply polygon or multipolygon.
            ee (earth engine instance): Earth engine initialized object.

        Raises:
            ValueError: A geometry can be either Polygon or MultiPolygon.

        Returns:
            ee.Geometry.Polygon or ee.Geometry.MultiPolygon: Earth engine polygon or mulyipolygon.
        """
        if isinstance(geometry, Polygon):

            coords = geometry.exterior.coords
            polygon = ee.Geometry.Polygon([list(item) for item in coords])

            return polygon
        
        elif isinstance(geometry, MultiPolygon):

            multipolygon = ee.Geometry.MultiPolygon([[list(item) for item in list(polygon.exterior.coords)] \
                                                 for polygon in geometry.geoms])
            return multipolygon
        
        else:
            raise ValueError('Supported geometries are Polygon and Multipolygon.')
        
        
    
    @staticmethod
    def get_utm_zone(geometry):
        """Method allowing to retrieve the UTM zone of a specific location.

        Args:
            geometry (shapely.geometry): Shapely geometry.

        Returns:
            int: Integer value of the corresponding EPSG of the UTM zone.
        """
        centroid = geometry.centroid
        lon, lat = centroid.x, centroid.y
        utm_zone = int(round((lon + 180) / 6, 0))

        if lat > 0:
            utm_zone = 32600 + utm_zone
        else:
            utm_zone = 32700 + utm_zone
        
        return utm_zone
    
    @staticmethod
    def _dataset_to_images(dataset):
        """Method allowing to convert earth engine dataset to images.

        Args:
            dataset (ee.ImageCollection): Earth engine image collection object.

        Returns:
            list: List of ee.Image objects.
        """
        length = dataset.size().getInfo()
        images = dataset.toList(length)
        images = [ee.Image(images.get(i)) for i in range(length)]

        return images

    @staticmethod
    def mask_plot(geometry, shape, value=1):
        """Method allowing to generate a mask in raster format based on geometry.

        Args:
            geometry (shapely.geometry.Polygon or shapely.geometry.MultiPolygon): Shapely geometry to generate the mask.
            shape (tuple): Tuple of width and height of the desired output.
            value (int, optional): Value to be burnt into the geometry._. Defaults to 1.

        Returns:
            ndarray: Raster data with the desired value and shape.
        """
        transform = from_bounds(*geometry.bounds, shape[1], shape[0]) # type: ignore
        rasterized_shape = rasterize([(geometry, value)], out_shape=shape, transform=transform,
                                       fill=np.nan, all_touched=False, dtype='float') # type: ignore
        return rasterized_shape
        
    def get_data(self, geometry, img_index=-1):
        """Method allowing to retrieve data based on the input geometry. 

        Args:
            geometry (ee.geometry): Polygon or MultiPolygon 
            img_index (int, optional): The timestamp of the requested image we consider the latest image by default. Defaults to -1.

        Returns:
            tuple(ndarray, datetime.datetime): Tuple of the retrieved image and its corresponding timestamp.
        """
        polygon = self.geometry_to_polygon(geometry, ee)
        dataset = ee.ImageCollection(self.dataset).filterDate(self.start, self.end).filterBounds(polygon)
        dataset = dataset.sort('CLOUDY_PIXEL_PERCENTAGE', False)
        images = self._dataset_to_images(dataset)

        if self.vi=='NDVI':
            B1, B2 = ('B8', 'B4') # type: ignore

        if self.vi=='NDWI':
            B1, B2 = ('B8', 'B12') # type: ignore

        image_date = datetime.fromtimestamp(images[img_index].get('system:time_start').getInfo() / 1000)
        vi_result = images[img_index].normalizedDifference([B1, B2]) # type: ignore
        vi_array = vi_result.sampleRectangle(region=polygon)
        result = np.array(vi_array.getInfo()['properties']['nd'])

        return result, image_date

    def map_result(self, geometry, **kwargs):
        """Method allowing to generate a vegetation index map.

        Args:
            geometry (shapely.geometry): Polygon or Multipolygon to generate the NDVI or NDWI map.
        """
        result, image_date = self.get_data(geometry, **kwargs)
        masked_result = self.mask_plot(geometry, result.shape) * result
        _, ax = plt.subplots()
        array = ax.imshow(masked_result)
        plt.colorbar(array)
        ax.set_title('{} : {}'.format(self.vi, str(image_date)[:10]))
        #plt.savefig('./fig.jpg', bbox_inches='tight')
        plt.show()