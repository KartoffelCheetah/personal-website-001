"""Image Resource Manager"""
import os
import re
from pathlib import Path
from typing import Union, Final, Callable, Iterable, Tuple, List
from flask import current_app
from PIL import Image
from app.models.image_resource_entity import ImageResourceEntity

class ThumbnailConfig:
	def __init__(self, thid: str, folder: str, multiplier: float, thumbnails: List['ThumbnailConfig']):
		self.thid = thid
		self.folder = folder
		self._multiplier = multiplier
		self.thumbnails = thumbnails
	def calculate_size(self, orig_img_res: Iterable[int]) -> Tuple[int, ...]:
		return tuple(int(res//(1/self._multiplier)) for res in orig_img_res)
THID_ROOT = 'ROOT'
conf_thumbnail: Final[List[ThumbnailConfig]] = [
	ThumbnailConfig(
		thid=THID_ROOT,
		folder=os.environ['FOLDER_UPLOAD_ROOT'],
		multiplier=float(os.environ['UPLOAD_TYPE_ROOT']),
		thumbnails=[
			ThumbnailConfig(
				thid='ROOT_B',
				folder=os.environ['FOLDER_UPLOAD_ROOT_B'],
				multiplier=float(os.environ['UPLOAD_TYPE_ROOT_B']),
				thumbnails=[],
			),
			ThumbnailConfig(
				thid='ROOT_A',
				folder=os.environ['FOLDER_UPLOAD_ROOT_A'],
				multiplier=float(os.environ['UPLOAD_TYPE_ROOT_A']),
				thumbnails=[],
			),
		]
	)
]

class ImageMetaData:
	@staticmethod
	def get_image_meta_data_full_path(filename: str, thumbnail_conf: ThumbnailConfig):
		return os.path.join(thumbnail_conf.folder, filename)

	def __init__(self, filename: str, thumbnail_conf: ThumbnailConfig, original_width: int, original_height: int):
		if not re.sub('_|-|\.', '', filename).isalnum():
			raise ValueError(f'filename did not pass validation: {filename}')
		self.thid = thumbnail_conf.thid
		self.filename = filename
		self.full_path = ImageMetaData.get_image_meta_data_full_path(self.filename, thumbnail_conf)
		self.relative_url = Path(current_app.static_url_path)/Path(self.full_path).resolve().relative_to(current_app.static_folder)
		self.width, self.height = thumbnail_conf.calculate_size((original_width, original_height))
		self.children_image_meta_data = tuple(map(lambda x: ImageMetaData(filename=self.filename, thumbnail_conf=x, original_width=original_width, original_height=original_height), thumbnail_conf.thumbnails))

def save_image_thumbnails_to_fs(filename: str) -> None:
	"""Generates the thumbnails for an image already existing on the fs."""
	conf = get_thumbnail_conf_by_thid(THID_ROOT)
	if conf:
		fp = ImageMetaData.get_image_meta_data_full_path(filename, thumbnail_conf=conf)
		image = Image.open(fp)
		imd = ImageMetaData(filename=filename, thumbnail_conf=conf, original_width=image.size[0], original_height=image.size[1])

		for child_imd in imd.children_image_meta_data:
			thumbnail_image = image.copy()
			thumbnail_image.thumbnail((child_imd.width, child_imd.height))
			thumbnail_image.save(child_imd.full_path)
	else:
		raise ValueError(f'thumbnail config is not found {THID_ROOT}')

def get_image_resource_entity_from_fs(filename: str) -> ImageResourceEntity:
	"""Returns a corresponding ImageResourceEntity.
	Database commit required."""
	conf = get_thumbnail_conf_by_thid(THID_ROOT)
	if conf:
		fp = ImageMetaData.get_image_meta_data_full_path(filename, thumbnail_conf=conf)
		width, height = Image.open(fp).size
		return ImageResourceEntity(resource=filename, width=width, height=height)
	else:
		raise ValueError(f'thumbnail config is not found {THID_ROOT}')

def get_thumbnail_conf_by_thid (thid: str, tharr: List[ThumbnailConfig]=conf_thumbnail) -> Union[ThumbnailConfig, None]:
	find_by_thid: Callable[[ThumbnailConfig], bool] = lambda t: t.thid == thid
	result = next(filter(find_by_thid, tharr), None)
	if not result:
		for tc in tharr:
			result = get_thumbnail_conf_by_thid(thid, tc.thumbnails)
			if result:
				break
	return result
