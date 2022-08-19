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


###############################################################################
# Export ECUC

# Globals
EcuName = None


def export_appmodes_to_container(root):
   ci = len(list(root))
   for appmode in sg.AppModes:
      root.insert(ci, ET.Comment("OsAppMode"))
      am_ctnr = lib.deprecated_insert_container(root, appmode, "conf", "/AUTOSAR/EcucDefs/Os/OsAppMode")
      ci += 2 # because we inserted 2 elements under root



def insert_osos_to_subcontainer(root):
   # OsOs Sub-Containers
   osos_subctnr = ET.SubElement(root, "SUB-CONTAINERS")

   # OS Hooks
   oshooks_ctnr = lib.deprecated_insert_container(osos_subctnr, "OsHooks", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks")
   # Parameters
   params = ET.SubElement(oshooks_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsErrorHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["ERRORHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPostTaskHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["POSTTASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPreTaskHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["PRETASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsShutdownHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["SHUTDOWNHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsStartupHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["STARTUPHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsProtectionHook"
   lib.deprecated_insert_param(params, refname, "numerical", "bool", "NOT YET SUPPORTED") # Todo: Please fix this.

   # OsHookStack
   oshooksstack_ctnr = lib.deprecated_insert_container(osos_subctnr, "OsHookStack", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack")
   # Parameters
   params = ET.SubElement(oshooksstack_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack/OsHookStackSize"
   lib.deprecated_insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_STACK_SIZE"])

   # FreeOsekParams
   freeosek_ctnr = lib.deprecated_insert_container(osos_subctnr, "FreeOsekParams", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams")
   # Parameters
   params = ET.SubElement(freeosek_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/OsName"
   lib.deprecated_insert_param(params, refname, "text", "enum", sg.OS_Cfgs["OS"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/CpuName"
   lib.deprecated_insert_param(params, refname, "text", "enum", sg.OS_Cfgs["CPU"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/IrqStackSize"
   lib.deprecated_insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["IRQ_STACK_SIZE"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/ContextSaveSize"
   lib.deprecated_insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_CTX_SAVE_SZ"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/AppTasksSize"
   lib.deprecated_insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["TASK_STACK_SIZE"])



def export_osos_to_container(root):
   ci = len(list(root))
   root.insert(ci, ET.Comment("OsOs"))
   osos_ctnr = lib.deprecated_insert_container(root, "OsOs", "conf", "/AUTOSAR/EcucDefs/Os/OsOS")
   # Parameters
   params = ET.SubElement(osos_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsStatus"
   lib.deprecated_insert_param(params, refname, "text", "enum", sg.OS_Cfgs["STATUS"])
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
      lib.deprecated_insert_container(root, evt, "conf", "/AUTOSAR/EcucDefs/Os/OsEvent")
      ci += 2



def export_counters_to_container(root):
   ci = len(list(root))
   for cntr in sg.Counters:
      root.insert(ci, ET.Comment("OsCounter"))
      ctnr = lib.deprecated_insert_container(root, cntr["Counter Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsCounter")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMaxAllowedValue"
      lib.deprecated_insert_param(params, refname, "numerical", "int", cntr['MAXALLOWEDVALUE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMinCycle"
      lib.deprecated_insert_param(params, refname, "numerical", "int", cntr['MINCYCLE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterTicksPerBase"
      lib.deprecated_insert_param(params, refname, "numerical", "int", cntr['TICKSPERBASE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterType"
      lib.deprecated_insert_param(params, refname, "text", "enum", cntr['OsCounterType'])



def insert_task_reference(root, task, os_obj, dref):
   if os_obj in task:
      for obj in task[os_obj]:
         lib.deprecated_insert_reference(root, dref, "/"+str(EcuName)+"/Os/"+str(obj))



def export_resources_to_container(root):
   global EcuName
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
         ctnr = lib.deprecated_insert_container(root, res, "conf", "/AUTOSAR/EcucDefs/Os/OsResource")
         ci += 2
         # Parameters
         params = ET.SubElement(ctnr, "PARAMETER-VALUES")
         # OsResource Parameters
         refname = "/AUTOSAR/EcucDefs/Os/OsResource/OsResourceProperty"
         lib.deprecated_insert_param(params, refname, "text", "enum", "STANDARD") #Todo: Fixme: INTERNAL & LINKED to be supported!!



def export_tasks_to_container(root):
   global EcuName

   ci = len(list(root))
   for task in sg.Tasks:
      root.insert(ci, ET.Comment("OsTask"))
      ctnr = lib.deprecated_insert_container(root, task["Task Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsTask")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskActivation"
      lib.deprecated_insert_param(params, refname, "numerical", "int", task['ACTIVATION'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskPriority"
      lib.deprecated_insert_param(params, refname, "numerical", "int", task['PRIORITY'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskStackSize"
      lib.deprecated_insert_param(params, refname, "numerical", "int", task['STACK_SIZE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskSchedule"
      lib.deprecated_insert_param(params, refname, "text", "enum", task['SCHEDULE'])

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
         l2_ctnr = lib.deprecated_insert_container(sub_ctnr, "OsTaskAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart")
         # References
         l2_refs = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart/OsTaskAppModeRef"
         for am in task["AUTOSTART_APPMODE"]:
            lib.deprecated_insert_reference(l2_refs, dref, "/"+str(EcuName)+"/Os/"+str(am))



def export_alarms_to_container(root):
   global EcuName

   ci = len(list(root)) # ci stands for comment index
   for alm in sg.Alarms:
      root.insert(ci, ET.Comment("OsAlarm"))
      ctnr = lib.deprecated_insert_container(root, alm["Alarm Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm")
      ci += 2
      # References
      references = ET.SubElement(ctnr, "REFERENCE-VALUES")
      # Counters references
      dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmCounterRef"
      lib.deprecated_insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["COUNTER"])
      
      # Sub-Containers
      sub_ctnr = ET.SubElement(ctnr, "SUB-CONTAINERS")

      # Container Level-3 for OsAlarmAction
      l2_ctnr = lib.deprecated_insert_container(sub_ctnr, "OsAlarmAction", "choice", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction")
      l3_ctnr = ET.SubElement(l2_ctnr, "SUB-CONTAINERS")
      if alm["Action-Type"] == "ACTIVATETASK" or alm["Action-Type"] == "OsAlarmActivateTask":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask"
         l4_ctnr = lib.deprecated_insert_container(l3_ctnr, "OsAlarmActivateTask", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask/OsAlarmActivateTaskRef"
         lib.deprecated_insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg1"])
      elif alm["Action-Type"] == "SETEVENT" or alm["Action-Type"] == "OsAlarmSetEvent":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent"
         l4_ctnr = lib.deprecated_insert_container(l3_ctnr, "OsAlarmSetEvent", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task & Event references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventTaskRef"
         lib.deprecated_insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg1"])
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventRef"
         lib.deprecated_insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg2"])
      elif alm["Action-Type"] == "ALARMCALLBACK" or alm["Action-Type"] == "OsAlarmCallback":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback"
         l4_ctnr = lib.deprecated_insert_container(l3_ctnr, "OsAlarmCallback", "conf", dref)
         # Parameters
         params = ET.SubElement(l4_ctnr, "PARAMETER-VALUES")
         # Callback references
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback/OsAlarmCallbackName"
         lib.deprecated_insert_param(params, refname, "text", "func", alm["arg1"])

      # Container Level-3 for OsAlarmAutoStart
      if alm["IsAutostart"] == "TRUE":
         l2_ctnr = lib.deprecated_insert_container(sub_ctnr, "OsAlarmAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart")
         # Parameters
         params = ET.SubElement(l2_ctnr, "PARAMETER-VALUES")
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAlarmTime"
         lib.deprecated_insert_param(params, refname, "numerical", "int", alm["ALARMTIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmCycleTime"
         lib.deprecated_insert_param(params, refname, "numerical", "int", alm["CYCLETIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAutostartType"
         lib.deprecated_insert_param(params, refname, "numerical", "int", "NOT YET SUPPORTED") # Todo: add support for this in UI
      if "APPMODE[]" in alm:
         # References
         references = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAppModeRef"
         for am in alm["APPMODE[]"]:
            lib.deprecated_insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+am)



def export_isrs_to_container(root):
   ci = len(list(root))
   for isr in sg.ISRs:
      root.insert(ci, ET.Comment("OsIsr"))
      ctnr = lib.deprecated_insert_container(root, isr["ISR Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsIsr")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptNumber"
      if 'IRQn' in isr:
         lib.deprecated_insert_param(params, refname, "numerical", "int", isr['IRQn'])
      else:
         lib.deprecated_insert_param(params, refname, "numerical", "int", "99")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptPriority"
      if 'OsIsrInterruptPriority' in isr:
         lib.deprecated_insert_param(params, refname, "numerical", "int", isr['OsIsrInterruptPriority'])
      else:
         lib.deprecated_insert_param(params, refname, "numerical", "int", '0')

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrCategory"
      if 'CATEGORY' in isr:
         lib.deprecated_insert_param(params, refname, "numerical", "int", isr['CATEGORY'])
      else:
         lib.deprecated_insert_param(params, refname, "numerical", "int", "2")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrStackSize"
      if 'OsIsrStackSize' in isr:
         lib.deprecated_insert_param(params, refname, "numerical", "int", isr['OsIsrStackSize'])
      else:
         lib.deprecated_insert_param(params, refname, "numerical", "int", "128")



# This function is called from core.main.py with AR-PACKAGES as root and name as Ecuc
# arg1: AR-PACKAGES element
# arg2: "Ecuc"
def build_ecuc_os_package(root, name):
   global EcuName

   # ci = len(list(root))
   # root.insert(ci, ET.Comment("AR-Package: AUTOSAR"))
   # arpkg = ET.SubElement(root, "AR-PACKAGE")
   # arpkg.set("UUID", "ECUC:ECUCDEFS")
   # shortname = ET.SubElement(arpkg, "SHORT-NAME")
   # shortname.text = name
   EcuName = name
   # elements = ET.SubElement(arpkg, "ELEMENTS")

   # Create the Os Module Configuration Element
   containers = lib.deprecated_insert_modconf(root, "Os")

   # Add OS configurations to the module configuration container
   export_appmodes_to_container(containers)
   export_osos_to_container(containers) # sg.OS_Cfgs go in here
   export_events_to_container(containers) # All events extracted from tasks go in here
   export_counters_to_container(containers)
   export_resources_to_container(containers)
   export_tasks_to_container(containers)
   export_alarms_to_container(containers)
   export_isrs_to_container(containers)


