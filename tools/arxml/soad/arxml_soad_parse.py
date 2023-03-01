#
# Created on Sun Feb 26 2023 11:03:02 PM
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





def parse_soad_general(cname, containers):
    soad_params = {}

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        params = lib_conf.get_param_list(ctnrblk)
        for par in params:
            soad_params[par["tag"]] = par["val"]

        # SoAdGeneral has exactly one container, so it is safe to break the loop
        break

    return soad_params



def get_soad_2nd_subcontainer(sub_ctnr_name, root, par_dict):
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
            if sub_ctnr_name == "SoAdPhysController":
                subc_param = get_soad_2nd_subcontainer("SoAdPhysCtrlRxMainFunctionPriorityProcessing", subc, subc_param)

            subc_p_list.append(subc_param)

    return subc_p_list



def parse_soad_bswmodules(cname, containers):
    soad_bswmods = []

    ctnrblks = lib_conf.findall_containers_with_name(cname, containers)
    for ctnrblk in ctnrblks:
        if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
            return None
        soad_params = {}

        # parse parameters
        params = lib_conf.get_param_list(ctnrblk)
        for par in params:
            soad_params[par["tag"]] = par["val"]

        # parse references
        refs = lib_conf.get_refval_list(ctnrblk)
        for ref in refs:
            soad_params[ref["tag"]] = ref["val"]

        soad_bswmods.append(soad_params)

    return soad_bswmods


def print_soad_configs(soad_configs):
    print("\n\nRead Operation:")
    print("\nSoAdGeneral:")
    print(soad_configs["SoAdGeneral"])

    print("\nSoAdBswModules:")
    print(soad_configs["SoAdBswModules"])



# This function parses ARXML and extract the SoAd information
# Returns: No of soad_configs
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate container
    soad_modconfs = lib_conf.find_module_configs("SoAd", elems)
    containers = lib_conf.find_containers_in_modconf(soad_modconfs)
    if containers == None:
        print("Error: parse_arxml() couldn't locate SoAd module in ", ar_file)
        return

    soad_cfg = {}

    # copy SoAdGeneral params to soad_configs
    soad_general = parse_soad_general("SoAdGeneral", containers)
    soad_cfg["SoAdGeneral"] = soad_general

    # copy SoAdBswModules to soad_configs
    soad_bswmods = parse_soad_bswmodules("SoAdBswModules", containers)
    soad_cfg["SoAdBswModules"] = soad_bswmods

    # copy SoAdConfig to soad_configs
    soad_cfg["SoAdConfig"] = []

    print_soad_configs(soad_cfg)

    return soad_cfg

