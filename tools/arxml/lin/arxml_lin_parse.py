#
# Created on Mon Dec 19 2022 12:07:25 PM
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





def parse_lin_general(cname, containers):
    lin_params = {}
    ofld_dict = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        for par in params:
            lin_params[par["tag"]] = par["val"]

        # LinGeneral has exactly one container, so it is safe to break the loop
        break

    return lin_params



# def get_lin_3rd_subcontainer(subc2_name, subc3_name, root, par_dict):
#     sub2_list = lib_conf.findall_subcontainers_with_name(subc2_name, root)
#     if not sub2_list:
#         return par_dict

#     # Only one "LinCtrlConfigEgress" or "LinCtrlConfigIngress" container exist within its super container, but loop one and exit
#     for ctnr2 in sub2_list:
#         if lib_conf.get_tag(ctnr2) == "ECUC-CONTAINER-VALUE":
#             sub3_list = lib_conf.findall_subcontainers_with_name(subc3_name, ctnr2)
#             for ctnr3 in sub3_list:
#                 item_params = lib_conf.get_param_list(ctnr3)
#                 for par in item_params:
#                     par_dict[par["tag"]] = par["val"]
#         # break after one loop, refer above note for more details
#         break

#     return par_dict



# def get_lin_2nd_subcontainer(sub_ctnr_name, root, par_dict):
#     sub2_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, root)
#     if not sub2_list:
#         return par_dict

#     # Only one "LinCtrlConfigSpiConfiguration" container exist within its super container, but loop one and exit
#     for cntr2 in sub2_list:
#         item_params = lib_conf.get_param_list(cntr2)
#         for par in item_params:
#             par_dict[par["tag"]] = par["val"]
#         # break after one loop, refer above note for more details
#         break

#     return par_dict



# def get_lincfg_scheduler_dict(root, par_dict):
#     sub2_list = lib_conf.findall_subcontainers_with_name("LinCtrlConfigEgress", root)
#     if not sub2_list:
#         return par_dict

#     # Only one "LinCtrlConfigScheduler" container exist within its super container, but loop one and exit
#     for ctnr2 in sub2_list:
#         par_dict = get_lin_3rd_subcontainer("LinCtrlConfigScheduler", "LinCtrlConfigSchedulerPredecessor", ctnr2, par_dict)

#     return par_dict



def get_linconfig_subcontainer(sub_ctnr_name, ctnr):
    chncfg_dict = {}

    ctnr_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, ctnr)
    # Only one "LinCtrlConfig" container exist within its super container, but loop one iteration and exit
    for item in ctnr_list:
        params = lib_conf.get_param_list(item)
        for par in params:
            chncfg_dict[par["tag"]] = par["val"]

        # break after getting the first, see above note for more details
        break

    return chncfg_dict



def parse_lin_chan_config(cname, containers):
    lin_chncfg_dict = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        lin_params = {}
        for par in params:
            lin_params[par["tag"]] = par["val"]

        # Let us parse the sub-containers
        chn_cfg  = get_linconfig_subcontainer("LinChannel", ctnrblk)
        lin_chncfg_dict[cname] = chn_cfg

        #LinConfigSet has exactly one container, so it is safe to break the loop
        break

    return lin_chncfg_dict



# This function parses ARXML and extract the Lin information
# Returns: No of lin_configs
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # empty list
    lin_configs = []

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    lin_modconfs = lib_conf.findall_module_configs("Lin", elems)
    for i, modconf in enumerate(lin_modconfs):
        # locate container
        containers = lib_conf.find_containers_in_modconf(modconf)
        if containers == None:
            continue

        # copy LinGlobalConfig to lin_configs
        lin_cfg = parse_lin_chan_config("LinGlobalConfig", containers)

        # copy LinGeneral params to lin_configs
        lin_general = parse_lin_general("LinGeneral", containers)
        lin_cfg["LinGeneral"] = lin_general
        lin_cfg["LinIndex"] = str(i)

        lin_configs.append(lin_cfg)

    return lin_configs

