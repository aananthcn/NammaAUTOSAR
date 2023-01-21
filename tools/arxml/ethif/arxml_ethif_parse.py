#
# Created on Thu Jan 19 2023 10:49:51 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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





def parse_ethif_general(cname, containers):
    ethif_params = {}
    hfile_idx = 0
    hfiles = []

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        for par in params:
            if "EthIfPublicCddHeaderFile" == par["tag"]:
                hfile = {}
                hfile["FileNo"] = hfile_idx
                hfile_idx += 1
                hfile["Headerfile"] = par["val"]
                hfiles.append(hfile)
            else:
                ethif_params[par["tag"]] = par["val"]

        # ofld_dict = get_ethif_2nd_subcontainer("EthIfCtrlOffloading", ctnrblk, ofld_dict)

        # EthIfGeneral has exactly one container, so it is safe to break the loop
        break

    ethif_params["EthIfPublicCddHeaderFile"] = hfiles

    return ethif_params



def get_ethif_3rd_subcontainer(subc2_name, subc3_name, root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name(subc2_name, root)
    if not sub2_list:
        return par_dict

    # Only one "EthIfCtrlConfigEgress" or "EthIfCtrlConfigIngress" container exist within its super container, but loop one and exit
    for ctnr2 in sub2_list:
        if lib_conf.get_tag(ctnr2) == "ECUC-CONTAINER-VALUE":
            sub3_list = lib_conf.findall_subcontainers_with_name(subc3_name, ctnr2)
            for ctnr3 in sub3_list:
                item_params = lib_conf.get_param_list(ctnr3)
                for par in item_params:
                    par_dict[par["tag"]] = par["val"]
        # break after one loop, refer above note for more details
        break

    return par_dict



def get_ethif_2nd_subcontainer(sub_ctnr_name, root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, root)
    if not sub2_list:
        return par_dict

    # Only one "EthIfCtrlConfigSpiConfiguration" container exist within its super container, but loop one and exit
    for cntr2 in sub2_list:
        item_params = lib_conf.get_param_list(cntr2)
        for par in item_params:
            par_dict[par["tag"]] = par["val"]
        # break after one loop, refer above note for more details
        break

    return par_dict



def get_ethifcfg_scheduler_dict(root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name("EthIfCtrlConfigEgress", root)
    if not sub2_list:
        return par_dict

    # Only one "EthIfCtrlConfigScheduler" container exist within its super container, but loop one and exit
    for ctnr2 in sub2_list:
        par_dict = get_ethif_3rd_subcontainer("EthIfCtrlConfigScheduler", "EthIfCtrlConfigSchedulerPredecessor", ctnr2, par_dict)

    return par_dict



def get_configset_subcontainer(sub_ctnr_name, ctnr):
    eccpar_dict = {}
    egress_dict = {}
    schdlr_dict = {}
    shaper_dict = {}
    xgress_dict = {}
    spicfg_dict = {}

    ctnr_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, ctnr)
    # Only one "EthIfCtrlConfig" container exist within its super container, but loop one iteration and exit
    for item in ctnr_list:
        params = lib_conf.get_param_list(item)
        for par in params:
            eccpar_dict[par["tag"]] = par["val"]

        egress_dict = get_ethif_3rd_subcontainer("EthIfCtrlConfigEgress", "EthIfCtrlConfigEgressFifo", item, egress_dict)
        schdlr_dict = get_ethifcfg_scheduler_dict(item, schdlr_dict)
        shaper_dict = get_ethif_3rd_subcontainer("EthIfCtrlConfigEgress", "EthIfCtrlConfigShaper", item, shaper_dict)
        xgress_dict = get_ethif_3rd_subcontainer("EthIfCtrlConfigIngress", "EthIfCtrlConfigIngressFifo", item, xgress_dict)
        spicfg_dict = get_ethif_2nd_subcontainer("EthIfCtrlConfigSpiConfiguration", item, spicfg_dict)

        # merge Egress and Ingress dicts
        xgress_dict.update(egress_dict)

        # break after getting the first, see above note for more details
        break

    return eccpar_dict, xgress_dict, schdlr_dict, shaper_dict, spicfg_dict



def parse_ethif_configset(cname, containers):
    ethif_cfgset_dict = {}

    return ethif_cfgset_dict

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        ethif_params = {}
        for par in params:
            ethif_params[par["tag"]] = par["val"]

        # Let us parse the sub-containers
        ecc_cfg, xgr_cfg, sch_cfg, shp_cfg, spi_cfg = get_configset_subcontainer("EthIfCtrlConfig", ctnrblk)
        ethif_cfgset_dict["EthIfCtrlConfig"] = ecc_cfg
        ethif_cfgset_dict["EthIfCtrlConfigXgressFifo"] = xgr_cfg
        ethif_cfgset_dict["EthIfCtrlConfigScheduler"] = sch_cfg
        ethif_cfgset_dict["EthIfCtrlConfigShaper"] = shp_cfg
        ethif_cfgset_dict["EthIfCtrlConfigSpiConfiguration"] = spi_cfg

        #EthIfConfigSet has exactly one container, so it is safe to break the loop
        break

    return ethif_cfgset_dict



# This function parses ARXML and extract the EthIf information
# Returns: No of ethif_configs
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # empty list
    ethif_configs = []

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate container
    ethif_modconfs = lib_conf.find_module_configs("EthIf", elems)
    containers = lib_conf.find_containers_in_modconf(ethif_modconfs)
    if containers == None:
        print("Error: parse_arxml() couldn't locate EthIf module in ", ar_file)
        return

    # copy EthIfConfigSet to ethif_configs
    ethif_cfg = {}
    ethif_cfgset = parse_ethif_configset("EthIfConfigSet", containers)
    ethif_cfg["EthIfConfigSet"] = ethif_cfgset

    # copy EthIfGeneral params to ethif_configs
    ethif_general = parse_ethif_general("EthIfGeneral", containers)
    ethif_cfg["EthIfGeneral"] = ethif_general

    ethif_configs.append(ethif_cfg)

    return ethif_configs

