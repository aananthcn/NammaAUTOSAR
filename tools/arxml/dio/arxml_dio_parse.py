#
# Created on Tue Sep 13 2022 10:00:03 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import xml.etree.ElementTree as ET
import arxml.core.lib as lib
import arxml.core.lib_conf as lib_conf
import arxml.core.lib_defs as lib_defs



def parse_arxml_diochannelgroup(subctnr, dio_port_id):
    dio_grp = {}
    nodes = lib_conf.findall_subcontainers_with_name("DioChannelGroup", subctnr)
    if nodes != None:
        for node in nodes:
            params = lib_conf.get_param_list(node)
            for par in params:
                dio_grp[par["tag"]] = par["val"]
        dio_grp["DioPortId"] = dio_port_id["DioPortId"]
    return dio_grp



def parse_arxml_diochannel(subctnr, dio_port_id):
    dio_chan = None

    # let us search DioChannel sub container to fetch DioChannelId
    subctnr2_list = lib_conf.findall_subcontainers_with_name("DioChannel", subctnr)
    if subctnr2_list == None:
        return dio_chan

    dio_chan = {}
    # fetch DioChannelId corresponding to DioPortId
    for subctnr2 in subctnr2_list:
        params = lib_conf.get_param_list(subctnr2)
        for par in params:
            dio_chan[par["tag"]] = par["val"]
        dio_chan["DioPortId"] = dio_port_id["DioPortId"]

    return dio_chan
 


def parse_arxml_dioportid(subctnr):
    dio_port_id = {}

    if lib_conf.get_tag(subctnr) != "ECUC-CONTAINER-VALUE":
        return dio_chan

    params = lib_conf.get_param_list(subctnr)
    for par in params:
        dio_port_id[par["tag"]] = par["val"]

    return dio_port_id;



def parse_arxml_dioconfig(containers):
    dio_n_pins = 0
    dio_configs = []
    dio_groups = []
    
    # locate DioConfig
    ctnrname = "DioConfig"
    ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
    if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None

    # parse all all DioPort subcontainer
    dioport_ctnr = None
    subctnr_list = lib_conf.findall_subcontainers_with_name("DioPort", ctnrblk)
    for subctnr in subctnr_list:
        dio_n_pins += 1

        # fetch DioPort Parameters (DioPortId)
        dio_port_id = parse_arxml_dioportid(subctnr)
    
        # parse DioChannel subcontainer
        dio_chan = parse_arxml_diochannel(subctnr, dio_port_id)
        if dio_chan == None:
            continue
        dio_configs.append(dio_chan)
    
    
        # parse DioChannelGroup from subcontainer
        dio_grp = parse_arxml_diochannelgroup(subctnr, dio_port_id)
        dio_groups.append(dio_grp)

    return dio_n_pins, dio_configs, dio_groups



# This function parses ARXML and extract the Dio information
# Returns: No of dio_configs, Dio pin dictionary
def parse_arxml(ar_file):
    if ar_file == None:
        return None, None, None
    dio_n_pins = None
    dio_configs = []
    dio_general = {}
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_conf_values("Dio", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return
    
    dio_n_pins, dio_configs, dio_groups = parse_arxml_dioconfig(containers)

    # locate & parse DioGeneral
    ctnrname = "DioGeneral"
    ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
    if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        dio_general[par["tag"]] = par["val"]
    
    return dio_n_pins, dio_configs, dio_groups, dio_general

