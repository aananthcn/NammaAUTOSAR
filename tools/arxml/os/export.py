import os
import xml.etree.ElementTree as ET

import scripts.System_Generator as sg
import arxml.lib as lib


###############################################################################
# Export ECUC

# Globals
EcuName = None


def export_appmodes_to_container(root):
   ci = len(list(root))
   for appmode in sg.AppModes:
      root.insert(ci, ET.Comment("OsAppMode"))
      am_ctnr = lib.insert_container(root, appmode, "conf", "/AUTOSAR/EcucDefs/Os/OsAppMode")
      ci += 2 # because we inserted 2 elements under root



def insert_osos_to_subcontainer(root):
   # OsOs Sub-Containers
   osos_subctnr = ET.SubElement(root, "SUB-CONTAINERS")

   # OS Hooks
   oshooks_ctnr = lib.insert_container(osos_subctnr, "OsHooks", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks")
   # Parameters
   params = ET.SubElement(oshooks_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsErrorHook"
   lib.insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["ERRORHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPostTaskHook"
   lib.insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["POSTTASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsPreTaskHook"
   lib.insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["PRETASKHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsShutdownHook"
   lib.insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["SHUTDOWNHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsStartupHook"
   lib.insert_param(params, refname, "numerical", "bool", sg.OS_Cfgs["STARTUPHOOK"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks/OsProtectionHook"
   lib.insert_param(params, refname, "numerical", "bool", "NOT YET SUPPORTED") # Todo: Please fix this.

   # OsHookStack
   oshooksstack_ctnr = lib.insert_container(osos_subctnr, "OsHookStack", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack")
   # Parameters
   params = ET.SubElement(oshooksstack_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack/OsHookStackSize"
   lib.insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_STACK_SIZE"])

   # FreeOsekParams
   freeosek_ctnr = lib.insert_container(osos_subctnr, "FreeOsekParams", "conf", "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams")
   # Parameters
   params = ET.SubElement(freeosek_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/OsName"
   lib.insert_param(params, refname, "text", "enum", sg.OS_Cfgs["OS"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/CpuName"
   lib.insert_param(params, refname, "text", "enum", sg.OS_Cfgs["CPU"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/IrqStackSize"
   lib.insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["IRQ_STACK_SIZE"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/ContextSaveSize"
   lib.insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["OS_CTX_SAVE_SZ"])
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/FreeOsekParams/AppTasksSize"
   lib.insert_param(params, refname, "numerical", "int", sg.OS_Cfgs["TASK_STACK_SIZE"])



def export_osos_to_container(root):
   ci = len(list(root))
   root.insert(ci, ET.Comment("OsOs"))
   osos_ctnr = lib.insert_container(root, "OsOs", "conf", "/AUTOSAR/EcucDefs/Os/OsOS")
   # Parameters
   params = ET.SubElement(osos_ctnr, "PARAMETER-VALUES")
   refname = "/AUTOSAR/EcucDefs/Os/OsOS/OsStatus"
   lib.insert_param(params, refname, "text", "enum", sg.OS_Cfgs["STATUS"])
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
      lib.insert_container(root, evt, "conf", "/AUTOSAR/EcucDefs/Os/OsEvent")
      ci += 2



def export_counters_to_container(root):
   ci = len(list(root))
   for cntr in sg.Counters:
      root.insert(ci, ET.Comment("OsCounter"))
      ctnr = lib.insert_container(root, cntr["Counter Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsCounter")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMaxAllowedValue"
      lib.insert_param(params, refname, "numerical", "int", cntr['MAXALLOWEDVALUE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterMinCycle"
      lib.insert_param(params, refname, "numerical", "int", cntr['MINCYCLE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterTicksPerBase"
      lib.insert_param(params, refname, "numerical", "int", cntr['TICKSPERBASE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsCounter/OsCounterType"
      lib.insert_param(params, refname, "text", "enum", cntr['OsCounterType'])



def insert_task_reference(root, task, os_obj, dref):
   if os_obj in task:
      for obj in task[os_obj]:
         lib.insert_reference(root, dref, "/"+str(EcuName)+"/Os/"+str(obj))



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
         ctnr = lib.insert_container(root, res, "conf", "/AUTOSAR/EcucDefs/Os/OsResource")
         ci += 2
         # Parameters
         params = ET.SubElement(ctnr, "PARAMETER-VALUES")
         # OsResource Parameters
         refname = "/AUTOSAR/EcucDefs/Os/OsResource/OsResourceProperty"
         lib.insert_param(params, refname, "text", "enum", "STANDARD") #Todo: Fixme: INTERNAL & LINKED to be supported!!



def export_tasks_to_container(root):
   global EcuName

   ci = len(list(root))
   for task in sg.Tasks:
      root.insert(ci, ET.Comment("OsTask"))
      ctnr = lib.insert_container(root, task["Task Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsTask")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskActivation"
      lib.insert_param(params, refname, "numerical", "int", task['ACTIVATION'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskPriority"
      lib.insert_param(params, refname, "numerical", "int", task['PRIORITY'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskStackSize"
      lib.insert_param(params, refname, "numerical", "int", task['STACK_SIZE'])
      refname = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskSchedule"
      lib.insert_param(params, refname, "text", "enum", task['SCHEDULE'])

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
         l2_ctnr = lib.insert_container(sub_ctnr, "OsTaskAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart")
         # References
         l2_refs = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsTask/OsTaskAutostart/OsTaskAppModeRef"
         for am in task["AUTOSTART_APPMODE"]:
            lib.insert_reference(l2_refs, dref, "/"+str(EcuName)+"/Os/"+str(am))



def export_alarms_to_container(root):
   global EcuName

   ci = len(list(root)) # ci stands for comment index
   for alm in sg.Alarms:
      root.insert(ci, ET.Comment("OsAlarm"))
      ctnr = lib.insert_container(root, alm["Alarm Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm")
      ci += 2
      # References
      references = ET.SubElement(ctnr, "REFERENCE-VALUES")
      # Counters references
      dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmCounterRef"
      lib.insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["COUNTER"])
      
      # Sub-Containers
      sub_ctnr = ET.SubElement(ctnr, "SUB-CONTAINERS")

      # Container Level-3 for OsAlarmAction
      l2_ctnr = lib.insert_container(sub_ctnr, "OsAlarmAction", "choice", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction")
      l3_ctnr = ET.SubElement(l2_ctnr, "SUB-CONTAINERS")
      if alm["Action-Type"] == "ACTIVATETASK" or alm["Action-Type"] == "OsAlarmActivateTask":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask"
         l4_ctnr = lib.insert_container(l3_ctnr, "OsAlarmActivateTask", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmActivateTask/OsAlarmActivateTaskRef"
         lib.insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg1"])
      elif alm["Action-Type"] == "SETEVENT" or alm["Action-Type"] == "OsAlarmSetEvent":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent"
         l4_ctnr = lib.insert_container(l3_ctnr, "OsAlarmSetEvent", "conf", dref)
         # References
         references = ET.SubElement(l4_ctnr, "REFERENCE-VALUES")
         # Task & Event references
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventTaskRef"
         lib.insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg1"])
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmSetEvent/OsAlarmSetEventRef"
         lib.insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+alm["arg2"])
      elif alm["Action-Type"] == "ALARMCALLBACK" or alm["Action-Type"] == "OsAlarmCallback":
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback"
         l4_ctnr = lib.insert_container(l3_ctnr, "OsAlarmCallback", "conf", dref)
         # Parameters
         params = ET.SubElement(l4_ctnr, "PARAMETER-VALUES")
         # Callback references
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAction/OsAlarmCallback/OsAlarmCallbackName"
         lib.insert_param(params, refname, "text", "func", alm["arg1"])

      # Container Level-3 for OsAlarmAutoStart
      if alm["IsAutostart"] == "TRUE":
         l2_ctnr = lib.insert_container(sub_ctnr, "OsAlarmAutostart", "conf", "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart")
         # Parameters
         params = ET.SubElement(l2_ctnr, "PARAMETER-VALUES")
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAlarmTime"
         lib.insert_param(params, refname, "numerical", "int", alm["ALARMTIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmCycleTime"
         lib.insert_param(params, refname, "numerical", "int", alm["CYCLETIME"])
         refname = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAutostartType"
         lib.insert_param(params, refname, "numerical", "int", "NOT YET SUPPORTED") # Todo: add support for this in UI
      if "APPMODE[]" in alm:
         # References
         references = ET.SubElement(l2_ctnr, "REFERENCE-VALUES")
         dref = "/AUTOSAR/EcucDefs/Os/OsAlarm/OsAlarmAutostart/OsAlarmAppModeRef"
         for am in alm["APPMODE[]"]:
            lib.insert_reference(references, dref, "/"+str(EcuName)+"/Os/"+am)



def export_isrs_to_container(root):
   ci = len(list(root))
   for isr in sg.ISRs:
      root.insert(ci, ET.Comment("OsIsr"))
      ctnr = lib.insert_container(root, isr["ISR Name"], "conf", "/AUTOSAR/EcucDefs/Os/OsIsr")
      ci += 2
      # Parameters
      params = ET.SubElement(ctnr, "PARAMETER-VALUES")
      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptNumber"
      if 'IRQn' in isr:
         lib.insert_param(params, refname, "numerical", "int", isr['IRQn'])
      else:
         lib.insert_param(params, refname, "numerical", "int", "99")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrInterruptPriority"
      if 'OsIsrInterruptPriority' in isr:
         lib.insert_param(params, refname, "numerical", "int", isr['OsIsrInterruptPriority'])
      else:
         lib.insert_param(params, refname, "numerical", "int", '0')

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrCategory"
      if 'CATEGORY' in isr:
         lib.insert_param(params, refname, "numerical", "int", isr['CATEGORY'])
      else:
         lib.insert_param(params, refname, "numerical", "int", "2")

      refname = "/AUTOSAR/EcucDefs/Os/OsIsr/OsIsrStackSize"
      if 'OsIsrStackSize' in isr:
         lib.insert_param(params, refname, "numerical", "int", isr['OsIsrStackSize'])
      else:
         lib.insert_param(params, refname, "numerical", "int", "128")



def build_ecuc_os_package(root, name):
   global EcuName

   arpkg = ET.SubElement(root, "AR-PACKAGE")
   shortname = ET.SubElement(arpkg, "SHORT-NAME")
   shortname.text = name
   EcuName = name
   elements = ET.SubElement(arpkg, "ELEMENTS")

   # Create the Os Module Configuration Element
   mod_conf = ET.SubElement(elements, "ECUC-MODULE-CONFIGURATION-VALUES")
   shortname = ET.SubElement(mod_conf, "SHORT-NAME")
   shortname.text = "Os"
   def_ref = ET.SubElement(mod_conf, "DEFINITION-REF", DEST="ECUC-MODULE-DEF")
   def_ref.text = "/AUTOSAR/EcucDefs/Os"
   ecu_def_edition = ET.SubElement(mod_conf, "ECUC-DEF-EDITION")
   ecu_def_edition.text = "4.2.0"
   impl_cfg_var = ET.SubElement(mod_conf, "IMPLEMENTATION-CONFIG-VARIANT")
   impl_cfg_var.text = "VARIANT-PRE-COMPILE"

   # Create CONTAINER element and export Os objects.
   containers = ET.SubElement(mod_conf, "CONTAINERS")
   export_appmodes_to_container(containers)
   export_osos_to_container(containers) # sg.OS_Cfgs go in here
   export_events_to_container(containers) # All events extracted from tasks go in here
   export_counters_to_container(containers)
   export_resources_to_container(containers)
   export_tasks_to_container(containers)
   export_alarms_to_container(containers)
   export_isrs_to_container(containers)


