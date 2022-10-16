#
# Created on Mon Aug 15 2022 1:48:56 PM
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
import os
import xml.etree.ElementTree as ET

import os_builder.scripts.System_Generator as sg
import arxml.core.lib as lib
import arxml.core.lib_conf as lib_conf
import arxml.core.lib_defs as lib_defs





###############################################################################
# Functions
def export_appmodes_to_container(root):
   ci = len(list(root))
   for appmode in sg.AppModes:
      root.insert(ci, ET.Comment("OsAppMode"))
      am_ctnr = lib_conf.insert_conf_container(root, appmode, "conf", "/AUTOSAR/EcucDefs/Os/OsAppMode")
      ci += 2 # because we inserted 2 elements under root



def insert_osos_to_subcontainer(root):
   # OsOs Sub-Containers
   osos_subctnr = ET.SubElement(root, "SUB-CONTAINERS")

   # OS Hooks
   oshooks_ctnr = lib_conf.insert_conf_container(osos_subctnr, "OsHooks", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks")
   # Parameters
   params = ET.SubElement(oshooks_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsErrorHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", sg.OS_Cfgs["ERRORHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPostTaskHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", sg.OS_Cfgs["POSTTASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPreTaskHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", sg.OS_Cfgs["PRETASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsShutdownHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", sg.OS_Cfgs["SHUTDOWNHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsStartupHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", sg.OS_Cfgs["STARTUPHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsProtectionHook"
   lib_conf.insert_conf_param(params, refname, "numerical", "bool", "NOT YET SUPPORTED") # Todo: Please fix this.

   # OsHookStack
   oshooksstack_ctnr = lib_conf.insert_conf_container(osos_subctnr, "OsHookStack", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack")
   # Parameters
   params = ET.SubElement(oshooksstack_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack/OsHookStackSize"
   lib_conf.insert_conf_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_STACK_SIZE"])

   # NammaOsekParams
   freeosek_ctnr = lib_conf.insert_conf_container(osos_subctnr, "NammaOsekParams", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific")
   # Parameters
   params = ET.SubElement(freeosek_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific/OsName"
   lib_conf.insert_conf_param(params, refname, "text", "enum", sg.OS_Cfgs["OS"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific/CpuName"
   lib_conf.insert_conf_param(params, refname, "text", "enum", sg.OS_Cfgs["CPU"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific/IrqStackSize"
   lib_conf.insert_conf_param(params, refname, "numerical", "int", sg.OS_Cfgs["IRQ_STACK_SIZE"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific/ContextSaveSize"
   lib_conf.insert_conf_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_CTX_SAVE_SZ"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific/AppTasksSize"
   lib_conf.insert_conf_param(params, refname, "numerical", "int", sg.OS_Cfgs["TASK_STACK_SIZE"])



def export_osos_to_container(root):
   ci = len(list(root))
   root.insert(ci, ET.Comment("OsOs"))
   osos_ctnr = lib_conf.insert_conf_container(root, "OsOs", "conf", "/AUTOSAR/EcucDefs/Os/OsOS")
   # Parameters
   params = ET.SubElement(osos_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsStatus"
   lib_conf.insert_conf_param(params, refname, "text", "enum", sg.OS_Cfgs["STATUS"])
   insert_osos_to_subcontainer(osos_ctnr)



def export_events_to_container(root):
   Events = []
   for task in sg.Tasks:
      if "EVENT" in task:
         for evt in task["EVENT"]:
            if evt not in Events:
               Events.append(evt)
   ci = len(list(root))
   for evt in Events:
      root.insert(ci, ET.Comment("OsEvent"))
      lib_conf.insert_conf_container(root, evt, "conf", "/AUTOSAR/EcucDefs/Os/OsEvent")
      ci += 2



def export_counters_to_container(root):
   ci = len(list(root))
   for cntr in sg.Counters:
      root.insert(ci, ET.Comment("OsCounter"))
      ctnr = lib_conf.insert_conf_container(root, cntr["Counter Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsCounter")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMaxAllowedValue"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", cntr['MAXALLOWEDVALUE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMinCycle"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", cntr['MINCYCLE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterTicksPerBase"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", cntr['TICKSPERBASE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterType"
      lib_conf.insert_conf_param(params, refname, "text", "enum", cntr['OsCounterType'])



def insert_task_reference(root, task, os_obj, dref):
   ecuname = lib.get_ecuc_arpkg_name()
   if os_obj in task:
      for obj in task[os_obj]:
         lib_conf.insert_conf_reference(root, dref, "/EcucDefs/Os/"+str(obj))



def export_resources_to_container(root):
   resources = []

   for task in sg.Tasks:
      if "RESOURCE" in task:
         for res in task["RESOURCE"]:
            if res not in resources:
               resources.append(res)
   
   if len(resources) > 0:
      ci = len(list(root)) # ci stands for comment index
      for res in resources:
         root.insert(ci, ET.Comment("OsResource"))
         ctnr = lib_conf.insert_conf_container(root, res, "conf", "/AUTOSAR/EcucDefs/Os/OsResource")
         ci += 2
         # Parameters
         params = ET.SubElement(ctnr, "PARAMETER-VALUES")
         # OsResource Parameters
         refname = "/AUTOSAR/EcucDefs/Os/OsResource/OsResourceProperty"
         lib_conf.insert_conf_param(params, refname, "text", "enum", "STANDARD") #Todo: Fixme: INTERNAL & LINKED to be supported!!



def export_tasks_to_container(root):
   ci = len(list(root))
   for task in sg.Tasks:
      root.insert(ci, ET.Comment("OsTask"))
      ctnr = lib_conf.insert_conf_container(root, task["Task Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsTask")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskActivation"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", task['ACTIVATION'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskPriority"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", task['PRIORITY'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskStackSize"
      lib_conf.insert_conf_param(params, refname, "numerical", "int", task['STACK_SIZE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskSchedule"
      lib_conf.insert_conf_param(params, refname, "text", "enum", task['SCHEDULE'])

      # References
      references = ET.SubElement(ctnr, "REFERENCE-VALUES")
      # Event References
      dref = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskEventRef"
      insert_task_reference(references, task, "EVENT", dref)
      # Resource References
      dref = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskResourceRef"
      insert_task_reference(references, task, "RESOURCE", dref)

      # Sub-Containers
      if "AUTOSTART_APPMODE" in task:
         sub_ctnr = ET.SubElement(ctnr, "SUB-CONTAINERS")
         l2_ctnr = lib_conf.insert_conf_container(sub_ctnr, "OsTaskAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart")
         # References
         l2_refs = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart/OsTaskAppModeRef"
         for am in task["AUTOSTART_APPMODE"]:
            lib_conf.insert_conf_reference(l2_refs, dref, "/EcucDefs/Os/"+str(am))



def export_alarms_to_container(root):
   ci = len(list(root)) # ci stands for comment index
   for alm in sg.Alarms:
      root.insert(ci, ET.Comment("OsAlarm"))
      ctnr = lib_conf.insert_conf_container(root, alm["Alarm Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm")
      ci += 2
      # References
      references = ET.SubElement(ctnr, "REFERENCE-VALUES")
      # Counters references
      dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmCounterRef"
      lib_conf.insert_conf_reference(references, dref, "/EcucDefs/Os/"+alm["COUNTER"])
      
      # Sub-Containers
      sub_ctnr = ET.SubElement(ctnr, "SUB-CONTAINERS")

      # Container Level-3 for OsAlarmAction
      l2_ctnr = lib_conf.insert_conf_container(sub_ctnr, "OsAlarmAction", "choice", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction")
      l3_ctnr = ET.SubElement(l2_ctnr, "SUB-CONTAINERS")
      if alm["Action-Type"] == "ACTIVATETASK" or alm["Action-Type"] == "OsAlarmActivateTask":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask"
         l4_ctnr = lib_conf.insert_conf_container(l3_ctnr, "ACTIVATETASK", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask/OsAlarmActivateTaskRef"
         lib_conf.insert_conf_reference(references, dref, "/EcucDefs/Os/"+alm["arg1"])
      elif alm["Action-Type"] == "SETEVENT" or alm["Action-Type"] == "OsAlarmSetEvent":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent"
         l4_ctnr = lib_conf.insert_conf_container(l3_ctnr, "SETEVENT", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task & Event references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventTaskRef"
         lib_conf.insert_conf_reference(references, dref, "/EcucDefs/Os/"+alm["arg1"])
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventRef"
         lib_conf.insert_conf_reference(references, dref, "/EcucDefs/Os/"+alm["arg2"])
      elif alm["Action-Type"] == "ALARMCALLBACK" or alm["Action-Type"] == "OsAlarmCallback":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback"
         l4_ctnr = lib_conf.insert_conf_container(l3_ctnr, "ALARMCALLBACK", "conf", dref)
         # Parameters
         params = ET.SubElement(l4_ctnr, "PARAMETER-VALUES")
         # Callback references
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback/OsAlarmCallbackName"
         lib_conf.insert_conf_param(params, refname, "text", "func", alm["arg1"])

      # Container Level-3 for OsAlarmAutoStart
      if alm["IsAutostart"] == "TRUE":
         l2_ctnr = lib_conf.insert_conf_container(sub_ctnr, "OsAlarmAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart")
         # Parameters
         params = ET.SubElement(l2_ctnr, "PARAMETER-VALUES")
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAlarmTime"
         lib_conf.insert_conf_param(params, refname, "numerical", "int", alm["ALARMTIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmCycleTime"
         lib_conf.insert_conf_param(params, refname, "numerical", "int", alm["CYCLETIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAutostartType"
         lib_conf.insert_conf_param(params, refname, "numerical", "int", "NOT YET SUPPORTED") # Todo: add support for this in UI
      if "APPMODE" in alm:
         # References
         references = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAppModeRef"
         for am in alm["APPMODE"]:
            lib_conf.insert_conf_reference(references, dref, "/EcucDefs/Os/"+am)



def export_isrs_to_container(root):
   ci = len(list(root))
   for isr in sg.ISRs:
      root.insert(ci, ET.Comment("OsIsr"))
      ctnr = lib_conf.insert_conf_container(root, isr["ISR Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsIsr")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptNumber"
      if 'IRQn' in isr:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", isr['IRQn'])
      else:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", "99")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptPriority"
      if 'OsIsrInterruptPriority' in isr:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", isr['OsIsrInterruptPriority'])
      else:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", '0')

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrCategory"
      if 'CATEGORY' in isr:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", isr['CATEGORY'])
      else:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", "2")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrStackSize"
      if 'OsIsrStackSize' in isr:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", isr['OsIsrStackSize'])
      else:
         lib_conf.insert_conf_param(params, refname, "numerical", "int", "128")



# This function is called from core.main.py with AR-PACKAGES as root and name as Ecuc
# arg1: AR-PACKAGES element
def build_ecuc_os_package(root):
   # Create the Os Module Configuration Element
   modconf = lib_conf.insert_ecuc_module_conf(root, "Os")
   containers = lib_conf.find_containers_in_modconf(modconf)

   # Add OS configurations to the module configuration container
   export_appmodes_to_container(containers)
   export_osos_to_container(containers) # sg.OS_Cfgs go in here
   export_events_to_container(containers) # All events extracted from tasks go in here
   export_counters_to_container(containers)
   export_resources_to_container(containers)
   export_tasks_to_container(containers)
   export_alarms_to_container(containers)
   export_isrs_to_container(containers)


