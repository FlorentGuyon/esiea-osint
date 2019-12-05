# -*- coding: utf-8 -*-

import os, sys

from .utils.run import h8mail

class Namespace:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

def callh8mail(address):

	user_args = Namespace(
		bc_path 			= None, 
		chase_limit			= None,
		cli_apikeys 		= None,
		config_file 		= None,
		debug				= False,
		gen_config			= False,
		hide				= True,
		local_breach_src 	= None,
		local_gzip_src		= None,
		loose				= False,
		output_file			= None,
		power_chase			= False,
		single_file			= False,
		skip_defaults		= False,
		user_query			= None,
		user_targets		= ['"' + address + '"']
	)

	breached_targets = h8mail(user_args, verbose = False)

	return breached_targets[0].data