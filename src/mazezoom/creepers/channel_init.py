# -*- coding:utf-8 -*-


import position
from base import PositionSpider
from orm import ORMManager

model_attrs = dir(position)

manager = ORMManager()
for attr in model_attrs:
	model = getattr(position, attr) 
	if hasattr(model, '__base__'):
		if issubclass(model, PositionSpider) and hasattr(model, 'name'):
			name = model.name
			if name:
				domain = model.domain
				manager.get_or_create_channel(
					name=name,
					domain=domain
				)
				
