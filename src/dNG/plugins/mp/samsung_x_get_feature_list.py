# -*- coding: utf-8 -*-

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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpPluginsSamsungVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error,no-name-in-module,unused-argument

from dNG.data.upnp.resources.mp_entry import MpEntry
from dNG.data.xml_resource import XmlResource
from dNG.database.connection import Connection
from dNG.plugins.hook import Hook
from dNG.runtime.value_exception import ValueException

def get_children(params, last_return = None):
    """
Called for "mp.upnp.HookResource.getChildren"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.01
    """

    _return = [ ]

    if (last_return is not None): _return = last_return
    elif ("id" not in params): raise ValueException("Missing required argument")
    elif (params['id'] == "mp_plugins_samsung_feature_list_container"):
        containers = _get_samsung_categorized_root_containers()
        _type = params['type']

        if (_type in containers): _return = containers[_type]
    #

    return _return
#

def get_features(params, last_return = None):
    """
Called for "dNG.pas.upnp.services.ContentDirectory.getFeatures"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
    """

    if ("xml_resource" in params):
        xml_resource = params['xml_resource']

        xml_base_path = "Features Feature#{0:d}".format(xml_resource.count_node("Features Feature"))

        xml_resource.add_node(xml_base_path, attributes = { "name": "samsung.com_BASICVIEW", "version": "1" })

        with Connection.get_instance():
            containers = _get_samsung_categorized_root_containers()

            for _type in containers:
                entries = containers[_type]

                attributes = { "id": (entries[0].get_resource_id()
                                      if (len(entries) == 1) else
                                      "hook-resource:///mp_plugins_samsung_feature_list_container/type%3d{0}".format(_type)
                                     ),
                               "type": _type
                             }

                xml_resource.add_node("{0} container".format(xml_base_path), attributes = attributes)
            #
        #
    #

    return last_return
#

def get_resource_data(params, last_return = None):
    """
Called for "mp.upnp.HookResource.getResourceData"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.01
    """

    _return = None

    if (last_return is not None): _return = last_return
    elif ("id" not in params): raise ValueException("Missing required argument")
    elif (params['id'] == "mp_plugins_samsung_feature_list_container"):
        _return = { "name": params['type'],
                    "type": MpEntry.TYPE_CDS_CONTAINER,
                    "type_name": "object.container.genre.movieGenre"
                  }
    #

    return _return
#

def _get_samsung_categorized_root_containers():
    """
Returns UPnP root containers categorized by type for Samsung devices.

:return: (dict) Dict with type as key and resource(s) as value
:since:  v0.1.01
    """

    _return = { }

    for entry in MpEntry.load_root_containers():
        entry_type = entry.get_type()

        if (entry_type & MpEntry.TYPE_CDS_CONTAINER_AUDIO == MpEntry.TYPE_CDS_CONTAINER_AUDIO): _type = "object.item.audioItem"
        elif (entry_type & MpEntry.TYPE_CDS_ITEM_AUDIO == MpEntry.TYPE_CDS_ITEM_AUDIO): _type = "object.item.audioItem"
        elif (entry_type & MpEntry.TYPE_CDS_CONTAINER_IMAGE == MpEntry.TYPE_CDS_CONTAINER_IMAGE): _type = "object.item.imageItem"
        elif (entry_type & MpEntry.TYPE_CDS_ITEM_IMAGE == MpEntry.TYPE_CDS_ITEM_IMAGE): _type = "object.item.imageItem"
        elif (entry_type & MpEntry.TYPE_CDS_CONTAINER_VIDEO == MpEntry.TYPE_CDS_CONTAINER_VIDEO): _type = "object.item.videoItem"
        elif (entry_type & MpEntry.TYPE_CDS_ITEM_VIDEO == MpEntry.TYPE_CDS_ITEM_VIDEO): _type = "object.item.videoItem"
        elif (entry_type & MpEntry.TYPE_CDS_CONTAINER == MpEntry.TYPE_CDS_CONTAINER): _type = "object.container"
        else: _type = "object.item"

        if (_type in _return): _return[_type].append(entry)
        else: _return[_type] = [ entry ]
    #

    return _return
#

def init_host(params, last_return = None):
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
        params['service'].add_host_action("X_GetFeatureList",
                                          return_variable = { "name": "FeatureList",
                                                              "variable": "FeatureList"
                                                            }
                                         )
    #

    return last_return
#

def register_plugin():
    """
Register plugin hooks.

:since: v0.1.00
    """

    Hook.register("mp.upnp.HookResource.getChildren", get_children)
    Hook.register("mp.upnp.HookResource.getResourceData", get_resource_data)
    Hook.register("dNG.pas.upnp.services.ContentDirectory.getFeatures", get_features)
    Hook.register("dNG.pas.upnp.services.ContentDirectory.handle.x_get_feature_list", x_get_feature_list)
    Hook.register("dNG.pas.upnp.Service.initHost", init_host)
#

def unregister_plugin():
    """
Unregister plugin hooks.

:since: v0.1.00
    """

    Hook.unregister("mp.upnp.HookResource.getChildren", get_children)
    Hook.unregister("mp.upnp.HookResource.getResourceData", get_resource_data)
    Hook.unregister("dNG.pas.upnp.services.ContentDirectory.getFeatures", get_features)
    Hook.unregister("dNG.pas.upnp.services.ContentDirectory.handle.x_get_feature_list", x_get_feature_list)
    Hook.unregister("dNG.pas.upnp.Service.initHost", init_host)
#

def x_get_feature_list(params, last_return = None):
    """
Called for "dNG.pas.upnp.services.ContentDirectory.handle.x_get_feature_list"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
    """

    if (last_return is not None): _return = last_return
    else:
        xml_resource = XmlResource()
        xml_resource.set_cdata_encoding(False)

        xml_resource.add_node("Features",
                              attributes = { "xmlns": "urn:schemas-upnp-org:av:avs",
                                             "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                             "xsi:schemaLocation": "urn:schemas-upnp-org:av:avs http://www.upnp.org/schemas/av/avs.xsd"
                                           }
                             )

        xml_resource.set_cached_node("Features")

        Hook.call("dNG.pas.upnp.services.ContentDirectory.getFeatures", xml_resource = xml_resource)

        _return = "<?xml version='1.0' encoding='UTF-8' ?>{0}".format(xml_resource.export_cache(True))
    #

    return _return
#
