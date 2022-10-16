#
# Created on Mon Aug 15 2022 1:48:39 PM
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
import sys
import xml.etree.ElementTree as ET

import os_builder.scripts.System_Generator as sg
import arxml.core.lib as lib
import arxml.core.lib_conf as lib_conf
import arxml.core.lib_defs as lib_defs


###############################################################################
# Import ECUC

def get_ecuc_tree(root):
   ecuc_conf = None
   container = None
   if lib.get_tag(root) == "AUTOSAR":
      for item in list(root):
         if lib.get_tag(item) == "AR-PACKAGES":
            for pkg in list(item):
               if lib.get_tag(pkg) == "AR-PACKAGE":
                  for elem in list(pkg):
                     if lib.get_tag(elem) == "ELEMENTS":
                        for conf in list(elem):
                           if lib.get_tag(conf) == "ECUC-MODULE-CONFIGURATION-VALUES":
                              ecuc_conf = conf
                              break

   for item in list(ecuc_conf):
      if lib.get_tag(item) == "CONTAINERS":
         container = item
         break

   return ecuc_conf, container



def parse_OsHooks(ctnr):
   plist = lib.get_param_list(ctnr)
   for lst in plist:
      if lst["tag"] == "OsErrorHook":
         sg.OS_Cfgs["ERRORHOOK"] = lst["val"]
      if lst["tag"] == "OsPostTaskHook":
         sg.OS_Cfgs["POSTTASKHOOK"] = lst["val"]
      if lst["tag"] == "OsPreTaskHook":
         sg.OS_Cfgs["PRETASKHOOK"] = lst["val"]
      if lst["tag"] == "OsShutdownHook":
         sg.OS_Cfgs["SHUTDOWNHOOK"] = lst["val"]
      if lst["tag"] == "OsStartupHook":
         sg.OS_Cfgs["STARTUPHOOK"] = lst["val"]
      if lst["tag"] == "OsProtectionHook":
         sg.OS_Cfgs["OsProtectionHook"] = lst["val"]



def parse_OsHookStack(ctnr):
   plist = lib.get_param_list(ctnr)
   for lst in plist:
      if lst["tag"] == "OsHookStackSize":
         sg.OS_Cfgs["OS_STACK_SIZE"] = lst["val"]



def parse_NammaOsekParams(ctnr):
   plist = lib.get_param_list(ctnr)
   for lst in plist:
      if lst["tag"] == "OsName":
         sg.OS_Cfgs["OS"] = lst["val"]
      if lst["tag"] == "CpuName":
         sg.OS_Cfgs["CPU"] = lst["val"]
      if lst["tag"] == "IrqStackSize":
         sg.OS_Cfgs["IRQ_STACK_SIZE"] = lst["val"]
      if lst["tag"] == "ContextSaveSize":
         sg.OS_Cfgs["OS_CTX_SAVE_SZ"] = lst["val"]
      if lst["tag"] == "AppTasksSize":
         sg.OS_Cfgs["TASK_STACK_SIZE"] = lst["val"]



def parse_oscfg(ctnr):
   for elem in list(ctnr):
      if lib.get_tag(elem) == "PARAMETER-VALUES":
         plist = lib.get_param_list(ctnr)
         for lst in plist:
            if lst["tag"] == "OsStatus":
               sg.OS_Cfgs["STATUS"] = lst["val"]
      if lib.get_tag(elem) == "SUB-CONTAINERS":
         for ctnr in list(elem):
            dref = lib.get_dref_from_container(ctnr)
            if dref == "/AUTOSAR/EcucDefs/Os/OsOS/OsHooks":
               parse_OsHooks(ctnr)
            if dref == "/AUTOSAR/EcucDefs/Os/OsOS/OsHookStack":
               parse_OsHookStack(ctnr)
            if dref == "/AUTOSAR/EcucDefs/Os/OsOS/VendorSpecific":
               parse_NammaOsekParams(ctnr)



def parse_appmode(ctnr):
   for elem in list(ctnr):
      if lib.get_tag(elem) == "SHORT-NAME":
         sg.AppModes.append(elem.text)



def parse_counter(ctnr):
   iter_per_cntr = 2
   cntr = {}
   for elem in list(ctnr):
      if lib.get_tag(elem) == "SHORT-NAME":
         iter_per_cntr -= 1
         cntr["Counter Name"] = elem.text
      if lib.get_tag(elem) == "PARAMETER-VALUES":
         iter_per_cntr -= 1
         plist = lib.get_param_list(ctnr)
         for lst in plist:
            if lst["tag"] == "OsCounterMaxAllowedValue":
               cntr["MAXALLOWEDVALUE"] = lst["val"]
            if lst["tag"] == "OsCounterMinCycle":
               cntr["MINCYCLE"] = lst["val"]
            if lst["tag"] == "OsCounterTicksPerBase":
               cntr["TICKSPERBASE"] = lst["val"]
            if lst["tag"] == "OsCounterType":
               cntr["OsCounterType"] = lst["val"]
      if iter_per_cntr == 0:
         sg.Counters.append(cntr)
         iter_per_cntr = 2
         cntr = {}




def insert_in_task(task, key, val):
   try:
         task[key].append(val)
   except KeyError:
         task[key] = []
         task[key].append(val)


def parse_task(ctnr):
   iter_per_task = len(list(ctnr)) - 1
   task = {}
   autostart = False
   for elem in list(ctnr):
      if lib.get_tag(elem) == "SHORT-NAME":
         iter_per_task -= 1
         task["Task Name"] = elem.text
      elif lib.get_tag(elem) == "PARAMETER-VALUES":
         iter_per_task -= 1
         plist = lib.get_param_list(ctnr)
         for lst in plist:
            if lst["tag"] == "OsTaskActivation":
               task["ACTIVATION"] = lst["val"]
            if lst["tag"] == "OsTaskPriority":
               task["PRIORITY"] = lst["val"]
            if lst["tag"] == "OsTaskStackSize":
               task["STACK_SIZE"] = lst["val"]
            if lst["tag"] == "OsTaskSchedule":
               task["SCHEDULE"] = lst["val"]
      elif lib.get_tag(elem) == "REFERENCE-VALUES":
         iter_per_task -= 1
         plist = lib.get_dref_list(elem)
         for lst in plist:
            if lst["tag"] == "OsTaskResourceRef":
               insert_in_task(task, "RESOURCE", lst["val"])
            if lst["tag"] == "OsTaskEventRef":
               insert_in_task(task, "EVENT", lst["val"])
      elif lib.get_tag(elem) == "SUB-CONTAINERS":
         iter_per_task -= 1
         for l2c in list(elem):
            if lib.get_tag(l2c) == "ECUC-CONTAINER-VALUE":
               for item in list(l2c):
                  if lib.get_tag(item) == "REFERENCE-VALUES":
                     plist = lib.get_dref_list(item)
                     for lst in plist:
                        if lst["tag"] == "OsTaskAppModeRef":
                           insert_in_task(task, "AUTOSTART_APPMODE", lst["val"])
                           task["AUTOSTART"] = "TRUE"
                           autostart = True
      if iter_per_task == 0:
         if autostart == False:
            task["AUTOSTART"] = "FALSE"
         sg.Tasks.append(task)
         iter_per_task = len(list(ctnr)) - 1
         task = {}



def parse_alarm_action(ctnr, alarm):
   for item in list(ctnr):
      if lib.get_tag(item) == "SUB-CONTAINERS":
         for l3c in list(item):
            if lib.get_tag(l3c) == "ECUC-CONTAINER-VALUE":
               for elem in list(l3c):
                  if lib.get_tag(elem) == "SHORT-NAME":
                     alarm["Action-Type"] = elem.text
                  if lib.get_tag(elem) == "REFERENCE-VALUES":
                     plist = lib.get_dref_list(elem)
                     for lst in plist:
                        if lst["tag"] == "OsAlarmActivateTaskRef":
                           alarm["arg1"] = lst["val"]
                        if lst["tag"] == "OsAlarmSetEventTaskRef":
                           alarm["arg1"] = lst["val"]
                        if lst["tag"] == "OsAlarmIncrementCounterRef":
                           alarm["arg1"] = lst["val"]
                        if lst["tag"] == "OsAlarmSetEventRef":
                           alarm["arg2"] = lst["val"]
                  if lib.get_tag(elem) == "PARAMETER-VALUES":
                     plist = lib.get_param_list(l3c)
                     for lst in plist:
                        if lst["tag"] == "OsAlarmCallbackName":
                           alarm["arg1"] = lst["val"]



def parse_alarm_autostart(ctnr, alarm):
   for item in list(ctnr):
      if lib.get_tag(item) == "PARAMETER-VALUES":
         plist = lib.get_param_list(ctnr)
         for lst in plist:
            if lst["tag"] == "OsAlarmAlarmTime":
               alarm["ALARMTIME"] = lst["val"]
            if lst["tag"] == "OsAlarmCycleTime":
               alarm["CYCLETIME"] = lst["val"]
            if lst["tag"] == "OsAlarmAutostartType":
               alarm["OsAlarmAutostartType"] = lst["val"]
      if lib.get_tag(item) == "REFERENCE-VALUES":
         plist = lib.get_dref_list(item)
         for lst in plist:
            if lst["tag"] == "OsAlarmAppModeRef":
               alarm["APPMODE"].append(lst["val"])



def parse_alarm(ctnr):
   alarm = {}
   alarm["IsAutostart"] = "FALSE"
   for elem in list(ctnr):
      if lib.get_tag(elem) == "SHORT-NAME":
         alarm["Alarm Name"] = elem.text
      elif lib.get_tag(elem) == "REFERENCE-VALUES":
         plist = lib.get_dref_list(elem)
         for lst in plist:
            if lst["tag"] == "OsAlarmCounterRef":
               alarm["COUNTER"] = lst["val"]
      elif lib.get_tag(elem) == "SUB-CONTAINERS":
         for l2c in list(elem):
            if lib.get_tag(l2c) == "ECUC-CONTAINER-VALUE":
               for item in list(l2c):
                  if lib.get_tag(item) == "SHORT-NAME" and item.text == "OsAlarmAction":
                     parse_alarm_action(l2c, alarm)
                  elif lib.get_tag(item) == "SHORT-NAME" and item.text == "OsAlarmAutostart":
                     alarm["IsAutostart"] = "TRUE"
                     alarm["APPMODE"] = []
                     parse_alarm_autostart(l2c, alarm)

   sg.Alarms.append(alarm)



def parse_isr(ctnr):
   isr = {}
   for elem in list(ctnr):
      if lib.get_tag(elem) == "SHORT-NAME":
         isr["ISR Name"] = elem.text
      elif lib.get_tag(elem) == "PARAMETER-VALUES":
         plist = lib.get_param_list(ctnr)
         for lst in plist:
            if lst["tag"] == "OsIsrInterruptNumber":
               isr["IRQn"] = lst["val"]
            if lst["tag"] == "OsIsrInterruptPriority":
               isr["OsIsrInterruptPriority"] = lst["val"]
            if lst["tag"] == "OsIsrCategory":
               isr["CATEGORY"] = lst["val"]
            if lst["tag"] == "OsIsrStackSize":
               isr["OsIsrStackSize"] = lst["val"]
   sg.ISRs.append(isr)



def parse_arxml(filepath):
   tree = ET.parse(filepath)
   root = tree.getroot()
   modconf, cntainr = get_ecuc_tree(root)
   for cv in cntainr:
      dref = lib.get_dref_from_container(cv)
      if dref == "/AUTOSAR/EcucDefs/Os/OsOS":
         parse_oscfg(cv)
      elif dref == "/AUTOSAR/EcucDefs/Os/OsAppMode":
         parse_appmode(cv)
      elif dref == "/AUTOSAR/EcucDefs/Os/OsCounter":
         parse_counter(cv)
      elif dref == "/AUTOSAR/EcucDefs/Os/OsTask":
         parse_task(cv)
      elif dref == "/AUTOSAR/EcucDefs/Os/OsAlarm":
         parse_alarm(cv)
      elif dref == "/AUTOSAR/EcucDefs/Os/OsIsr":
         parse_isr(cv)
      # else:
      #    print(dref)



if __name__ == '__main__':
   print("import.py::__main__")