# -*- coding: utf-8 -*-
##j## BOF

"""
MediaProvider
A device centric multimedia solution
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?mp;plugins_samsung

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpPluginsSamsungVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error,no-name-in-module,unused-argument

from dNG.data.xml_resource import XmlResource
from dNG.pas.data.upnp.resources.mp_entry import MpEntry
from dNG.pas.database.connection import Connection
from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.value_exception import ValueException

def init_host(params, last_return = None):
#
	"""
Called for "dNG.pas.upnp.Service.initHost"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	if ("device" not in params
	    or "service" not in params
	   ): raise ValueException("Missing required arguments")
	elif (params['service'].get_name() == "schemas-upnp-org:service:ContentDirectory"):
	#
		service = params['service']

		service.add_host_variable("A_ARG_TYPE_FeatureList", { "is_sending_events": False,
		                                                      "is_multicasting_events": False,
		                                                      "type": "string"
		                                                    }
		                         )

		service.add_host_action("X_GetFeatureList", return_variable = { "name": "FeatureList", "variable": "A_ARG_TYPE_FeatureList" })
	#

	return last_return
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.upnp.service.ContentDirectory.x_get_feature_list", x_get_feature_list)
	Hook.register("dNG.pas.upnp.Service.initHost", init_host)
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.upnp.service.ContentDirectory.x_get_feature_list", x_get_feature_list)
	Hook.unregister("dNG.pas.upnp.Service.initHost", init_host)
#

def x_get_feature_list(params, last_return = None):
#
	"""
Called for "dNG.pas.upnp.service.ContentDirectory.x_get_feature_list"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	if (last_return != None): _return = last_return
	else:
	#
		xml_resource = XmlResource()
		xml_resource.set_cdata_encoding(False)

		xml_resource.add_node("Features",
		                      attributes = { "xmlns": "urn:schemas-upnp-org:av:avs",
		                                     "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
		                                     "xsi:schemaLocation": "urn:schemas-upnp-org:av:avs http://www.upnp.org/schemas/av/avs.xsd"
		                                   }
		                     )

		xml_base_path = "Features Feature"
		xml_resource.add_node(xml_base_path, attributes = { "name": "samsung.com_BASICVIEW", "version": "1" })
		xml_resource.set_cached_node(xml_base_path)

		with Connection.get_instance():
		#
			for entry in MpEntry.load_root_containers():
			#
				entry_type = entry.get_type()

				if (entry_type & MpEntry.TYPE_CDS_CONTAINER_AUDIO == MpEntry.TYPE_CDS_CONTAINER_AUDIO): _type = "object.item.audioItem"
				elif (entry_type & MpEntry.TYPE_CDS_ITEM_AUDIO == MpEntry.TYPE_CDS_ITEM_AUDIO): _type = "object.item.audioItem"
				elif (entry_type & MpEntry.TYPE_CDS_CONTAINER_IMAGE == MpEntry.TYPE_CDS_CONTAINER_IMAGE): _type = "object.item.imageItem"
				elif (entry_type & MpEntry.TYPE_CDS_ITEM_IMAGE == MpEntry.TYPE_CDS_ITEM_IMAGE): _type = "object.item.imageItem"
				elif (entry_type & MpEntry.TYPE_CDS_CONTAINER_VIDEO == MpEntry.TYPE_CDS_CONTAINER_VIDEO): _type = "object.item.videoItem"
				elif (entry_type & MpEntry.TYPE_CDS_ITEM_VIDEO == MpEntry.TYPE_CDS_ITEM_VIDEO): _type = "object.item.videoItem"
				elif (entry_type & MpEntry.TYPE_CDS_CONTAINER == MpEntry.TYPE_CDS_CONTAINER): _type = "object.container"
				else: _type = "object.item"

				attributes = { "id": entry.get_id(), "type": _type }
				xml_resource.add_node("{0} container".format(xml_base_path), attributes = attributes)
			#
		#

		_return = "<?xml version='1.0' encoding='UTF-8' ?>{0}".format(xml_resource.export_cache(True))
	#

	return _return
#

##j## EOF