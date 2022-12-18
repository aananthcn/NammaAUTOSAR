#
# Created on Sun Dec 11 2022 11:47:14 PM
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





def parse_eth_general(cname, containers):
    eth_params = {}
    ofld_dict = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        for par in params:
            eth_params[par["tag"]] = par["val"]

        ofld_dict = get_eth_2nd_subcontainer("EthCtrlOffloading", ctnrblk, ofld_dict)

        # EthGeneral has exactly one container, so it is safe to break the loop
        break

    return eth_params, ofld_dict



def get_eth_3rd_subcontainer(subc2_name, subc3_name, root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name(subc2_name, root)
    if not sub2_list:
        return par_dict

    # Only one "EthCtrlConfigEgress" or "EthCtrlConfigIngress" container exist within its super container, but loop one and exit
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



def get_eth_2nd_subcontainer(sub_ctnr_name, root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, root)
    if not sub2_list:
        return par_dict

    # Only one "EthCtrlConfigSpiConfiguration" container exist within its super container, but loop one and exit
    for cntr2 in sub2_list:
        item_params = lib_conf.get_param_list(cntr2)
        for par in item_params:
            par_dict[par["tag"]] = par["val"]
        # break after one loop, refer above note for more details
        break

    return par_dict



def get_ethcfg_scheduler_dict(root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name("EthCtrlConfigEgress", root)
    if not sub2_list:
        return par_dict

    # Only one "EthCtrlConfigScheduler" container exist within its super container, but loop one and exit
    for ctnr2 in sub2_list:
        par_dict = get_eth_3rd_subcontainer("EthCtrlConfigScheduler", "EthCtrlConfigSchedulerPredecessor", ctnr2, par_dict)

    return par_dict



def get_configset_subcontainer(sub_ctnr_name, ctnr):
    eccpar_dict = {}
    egress_dict = {}
    schdlr_dict = {}
    shaper_dict = {}
    xgress_dict = {}
    spicfg_dict = {}

    ctnr_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, ctnr)
    # Only one "EthCtrlConfig" container exist within its super container, but loop one iteration and exit
    for item in ctnr_list:
        params = lib_conf.get_param_list(item)
        for par in params:
            eccpar_dict[par["tag"]] = par["val"]

        egress_dict = get_eth_3rd_subcontainer("EthCtrlConfigEgress", "EthCtrlConfigEgressFifo", item, egress_dict)
        schdlr_dict = get_ethcfg_scheduler_dict(item, schdlr_dict)
        shaper_dict = get_eth_3rd_subcontainer("EthCtrlConfigEgress", "EthCtrlConfigShaper", item, shaper_dict)
        xgress_dict = get_eth_3rd_subcontainer("EthCtrlConfigIngress", "EthCtrlConfigIngressFifo", item, xgress_dict)
        spicfg_dict = get_eth_2nd_subcontainer("EthCtrlConfigSpiConfiguration", item, spicfg_dict)

        # merge Egress and Ingress dicts
        xgress_dict.update(egress_dict)

        # break after getting the first, see above note for more details
        break

    return eccpar_dict, xgress_dict, schdlr_dict, shaper_dict, spicfg_dict



def parse_eth_configset(cname, containers):
    eth_cfgset_dict = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        eth_params = {}
        for par in params:
            eth_params[par["tag"]] = par["val"]

        # Let us parse the sub-containers
        ecc_cfg, xgr_cfg, sch_cfg, shp_cfg, spi_cfg = get_configset_subcontainer("EthCtrlConfig", ctnrblk)
        eth_cfgset_dict["EthCtrlConfig"] = ecc_cfg
        eth_cfgset_dict["EthCtrlConfigXgressFifo"] = xgr_cfg
        eth_cfgset_dict["EthCtrlConfigScheduler"] = sch_cfg
        eth_cfgset_dict["EthCtrlConfigShaper"] = shp_cfg
        eth_cfgset_dict["EthCtrlConfigSpiConfiguration"] = spi_cfg

        #EthConfigSet has exactly one container, so it is safe to break the loop
        break

    return eth_cfgset_dict



# This function parses ARXML and extract the Eth information
# Returns: No of eth_configs
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # empty list
    eth_configs = []

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    eth_modconfs = lib_conf.findall_module_configs("Eth", elems)
    for i, modconf in enumerate(eth_modconfs):
        # locate container
        containers = lib_conf.find_containers_in_modconf(modconf)
        if containers == None:
            continue

        # copy EthConfigSet to eth_configs
        eth_cfg = parse_eth_configset("EthConfigSet", containers)

        # copy EthGeneral params to eth_configs
        eth_general, eth_offload = parse_eth_general("EthGeneral", containers)
        eth_cfg["EthGeneral"] = eth_general
        eth_cfg["EthCtrlOffloading"] = eth_offload
        eth_cfg["EthIndex"] = str(i)

        eth_configs.append(eth_cfg)

    return eth_configs

