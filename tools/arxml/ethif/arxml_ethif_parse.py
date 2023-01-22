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



def get_ethif_2nd_subcontainer(sub_ctnr_name, root, par_dict):
    sub2_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, root)
    if not sub2_list:
        return par_dict

    for cntr2 in sub2_list:
        # parse parameters
        item_params = lib_conf.get_param_list(cntr2)
        for par in item_params:
            par_dict[par["tag"]] = par["val"]

        # parse references
        refs = lib_conf.get_refval_list(cntr2)
        for ref in refs:
            par_dict[ref["tag"]] = ref["val"]

    return par_dict



def get_configset_subcontainer(sub_ctnr_name, ctnr):
    subc_p_list = []

    ctnr_list = lib_conf.findall_subcontainers_with_name(sub_ctnr_name, ctnr)
    if ctnr_list:
        for subc in ctnr_list:
            subc_param = {}
            # parse parameters
            params = lib_conf.get_param_list(subc)
            for par in params:
                subc_param[par["tag"]] = par["val"]

            # parse references
            refs = lib_conf.get_refval_list(subc)
            for ref in refs:
                subc_param[ref["tag"]] = ref["val"]

            # container level 2 parsing
            if sub_ctnr_name == "EthIfPhysController":
                subc_param = get_ethif_2nd_subcontainer("EthIfPhysCtrlRxMainFunctionPriorityProcessing", subc, subc_param)

            subc_p_list.append(subc_param)

    return subc_p_list



def parse_ethif_configset(cname, containers):
    ethif_cfgset_dict = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        ethif_params = {}
        for par in params:
            ethif_params[par["tag"]] = par["val"]

        # Let us parse the sub-containers
        cs_cfgs = get_configset_subcontainer("EthIfFrameOwnerConfig", ctnrblk)
        ethif_cfgset_dict["EthIfFrameOwnerConfig"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfRxIndicationConfig", ctnrblk)
        ethif_cfgset_dict["EthIfRxIndicationConfig"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfTxConfirmationConfig", ctnrblk)
        ethif_cfgset_dict["EthIfTxConfirmationConfig"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfTrcvLinkStateChgConfig", ctnrblk)
        ethif_cfgset_dict["EthIfTrcvLinkStateChgConfig"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfPhysController", ctnrblk)
        ethif_cfgset_dict["EthIfPhysController"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfController", ctnrblk)
        ethif_cfgset_dict["EthIfController"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfTransceiver", ctnrblk)
        ethif_cfgset_dict["EthIfTransceiver"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfSwitch", ctnrblk)
        ethif_cfgset_dict["EthIfSwitch"] = cs_cfgs

        cs_cfgs = get_configset_subcontainer("EthIfSwitchPortGroup", ctnrblk)
        ethif_cfgset_dict["EthIfSwitchPortGroup"] = cs_cfgs

        #EthIfConfigSet has exactly one container, so it is safe to break the loop
        break

    return ethif_cfgset_dict



def print_ethif_configs(ethif_configs):
    print("\n\nRead Operation:")
    print("\nEthIfGeneral:")
    print(ethif_configs["EthIfGeneral"])

    print("\nEthIfConfigSet:")
    print(ethif_configs["EthIfConfigSet"])



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

    # print_ethif_configs(ethif_cfg)
    ethif_configs.append(ethif_cfg)

    return ethif_configs

