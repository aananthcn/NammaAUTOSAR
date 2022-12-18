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





def parse_spi_general(cname, containers):
    spi_general = {}
    ctnrblk = lib_conf.find_ecuc_container_block(cname, containers)
    if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        spi_general[par["tag"]] = par["val"]
    
    return spi_general



def parse_spi_pubinfo(cname, containers):
    spi_pubinfo = {}
    ctnrblk = lib_conf.find_ecuc_container_block(cname, containers)
    if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        spi_pubinfo[par["tag"]] = par["val"]

    return spi_pubinfo



def getall_spidriver_2nd_subcontainer(sub_ctnr_name, item, par_dict):
    item_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, item)
    par_dict[sub_ctnr_name] = []
    for item in item_list:
        item_params = lib_conf.get_param_list(item)
        item_dict = {}
        for par in item_params:
            item_dict[par["tag"]] = par["val"]
        par_dict[sub_ctnr_name].append(item_dict)
    return par_dict


def getall_spidriver_subcontainer(sub_ctnr_name, ctnr):
    param_list = []
    ctnr_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, ctnr)
    for item in ctnr_list:
        params = lib_conf.get_param_list(item)
        par_dict = {}
        for par in params:
            par_dict[par["tag"]] = par["val"]

        if sub_ctnr_name == "SpiJob":
            par_dict = getall_spidriver_2nd_subcontainer("SpiChannelList", item, par_dict)
            # print("getall_spidriver_subcontainer()", par_dict)
        elif sub_ctnr_name == "SpiSequence":
            par_dict = getall_spidriver_2nd_subcontainer("SpiJobAssignment", item, par_dict)
            # print("getall_spidriver_subcontainer()", par_dict)
        param_list.append(par_dict)
    return param_list



def parse_spi_driver(cname, containers):
    spi_driver = {}
    ctnrblk = lib_conf.find_ecuc_container_block(cname, containers)
    if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        spi_driver[par["tag"]] = par["val"]

    # Let us parse the sub-containers
    spichn = getall_spidriver_subcontainer("SpiChannel", ctnrblk)
    spiexd = getall_spidriver_subcontainer("SpiExternalDevice", ctnrblk)
    spijob = getall_spidriver_subcontainer("SpiJob", ctnrblk)
    spiseq = getall_spidriver_subcontainer("SpiSequence", ctnrblk)
    
    spi_config = {}
    spi_config["SpiDriver"] = spi_driver
    spi_config["SpiChannel"] = spichn
    spi_config["SpiExternalDevice"] = spiexd
    spi_config["SpiJob"] = spijob
    spi_config["SpiSequence"] = spiseq

    return spi_config




# This function parses ARXML and extract the Spi information
# Returns: No of spi_configs, Spi pin dictionary
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # empty dictionary
    spi_configs = {}

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_configs("Spi", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    spi_general = parse_spi_general("SpiGeneral", containers)
    spi_pubinfo = parse_spi_general("SpiPublishedInformation", containers)
    spi_driver  = parse_spi_driver("SpiDriver", containers)

    # consolidate all parsed output to one nested-dict
    spi_configs = spi_driver
    spi_configs["SpiDriver"]["SpiMaxHwUnit"] = spi_pubinfo["SpiMaxHwUnit"]
    spi_configs["SpiGeneral"] = spi_general

    # print("parse_arxml->spi_configs", spi_configs)
    
    # return spi_n_pins, spi_configs, spi_groups, spi_general
    return spi_configs

