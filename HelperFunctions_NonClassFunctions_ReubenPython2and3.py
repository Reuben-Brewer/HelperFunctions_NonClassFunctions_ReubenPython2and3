# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 09/21/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

#########################################################
import os
import sys
import platform
import math
import time
import datetime
import threading
import collections
from copy import * #for deep_copy of dicts
import inspect #To enable 'TellWhichFileWereIn'
import traceback
import re
import json
import types #Required for 'ListFunctionNamesInClass'
from stdlib_list import stdlib_list #"pip install stdlib_list"
#########################################################

#########################################################
import serial #___IMPORTANT: pip install pyserial (NOT pip install serial).
from serial.tools import list_ports

try:
    import ftd2xx #https://pypi.org/project/ftd2xx/ 'pip install ftd2xx', current version is 1.3.1 as of 05/06/22. For SetAllFTDIdevicesLatencyTimer function
except:
    exceptions = sys.exc_info()[0]
    print("HelperFunctions_NonClassFunctions_ReubenPython2and3, warning: Could not import ftd2xx. Exceptions: %s" % exceptions)
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

##########################################################################################################
##########################################################################################################
def GetMyPlatform():
    my_platform = "other"

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)

    return my_platform
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber):

    try:
        InputNumber_ConvertedToFloat = float(InputNumber)
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber for variable_name '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

    try:
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
            return InputNumber_ConvertedToFloat
        else:
            input("PassThrough0and1values_ExitProgramOtherwise Error. '" + InputNameString + "' must be 0 or 1 (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def PassThroughFloatValuesInRange_ExitProgramOtherwise(InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
    try:
        InputNumber_ConvertedToFloat = float(InputNumber)
    except:
        exceptions = sys.exc_info()[0]
        print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

    try:
        if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
            return InputNumber_ConvertedToFloat
        else:
            input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" + InputNameString + "' must be in the range [" + str(RangeMinValue) + ", " + str(RangeMaxValue) + "] (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(GlobalsDict):

    print("ExitProgram_Callback event fired!")

    GlobalsDict["EXIT_PROGRAM_FLAG"] = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LoadAndParseJSONfile(JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    PassThrough0and1values_ExitProgramOtherwise(key, value)

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################
    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_Advanced Error, Exceptions: %s" % exceptions)
        return dict()
        #################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    GlobalsDict[key] = PassThrough0and1values_ExitProgramOtherwise(key, value)
                else:
                    GlobalsDict[key] = value
            else:
                GlobalsDict[key] = value

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################
    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_Advanced Error, Exceptions: %s" % exceptions)
        return dict()
        #################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ParseColonCommaSeparatedVariableString(line, print_line_flag = 0, numeric_values_only = 0):

    if print_line_flag == 1:
        print("ParseColonCommaSeparatedVariableString input: " + line)

    line_as_dict = dict()

    if len(line) > 0:
        try:
            line = line.replace("\n", "").replace("\r", "")
            line_as_list = filter(None, re.split("[,:]+", line))
            #print(line_as_list)

            toggle_counter = 0
            key = ""
            for element in line_as_list:
                if toggle_counter == 0:  # Every other element is a key, every other element is the value
                    key = element.strip()
                    toggle_counter = 1
                else:
                    if numeric_values_only == 1:
                        try:
                            line_as_dict[key] = float(element)
                            #print(key + " , " + element)
                        except:
                            line_as_dict[key] = "ERROR"
                    else:
                        line_as_dict[key] = element
                    toggle_counter = 0

            return line_as_dict
        except:
            exceptions = sys.exc_info()[0]
            print("ParseColonCommaSeparatedVariableString ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return line_as_dict
    else:
        print("ParseColonCommaSeparatedVariableString WARNING: input string was zero-length")
        return line_as_dict
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def IsTheTimeCurrentlyAM():
    ts = time.time()
    hour = int(datetime.datetime.fromtimestamp(ts).strftime('%H'))
    if hour < 12:
        return 1
    else:
        return 0
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation(LoopCounter, CurrentTime, LastTime, DataStreamingFrequency, DataStreamingDeltaT):

    try:

        DataStreamingDeltaT = CurrentTime - LastTime

        ##########################
        if DataStreamingDeltaT != 0.0:
            DataStreamingFrequency = 1.0/DataStreamingDeltaT
        ##########################

        LastTime = CurrentTime

        LoopCounter = LoopCounter + 1

        return [LoopCounter, LastTime, DataStreamingFrequency, DataStreamingDeltaT]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation, exceptions: %s" % exceptions)
        return [-11111.0]*4
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation_CalculatedFromMainThread(LoopCounter_CalculatedFromMainThread, CurrentTime_CalculatedFromMainThread, LastTime_CalculatedFromMainThread, DataStreamingFrequency_CalculatedFromMainThread, DataStreamingDeltaT_CalculatedFromMainThread):

    try:

        DataStreamingDeltaT_CalculatedFromMainThread = CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread

        ##########################
        if DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
            DataStreamingFrequency_CalculatedFromMainThread = 1.0/DataStreamingDeltaT_CalculatedFromMainThread
        ##########################

        LastTime_CalculatedFromMainThread = CurrentTime_CalculatedFromMainThread

        LoopCounter_CalculatedFromMainThread = LoopCounter_CalculatedFromMainThread + 1

        return [LoopCounter_CalculatedFromMainThread, LastTime_CalculatedFromMainThread, DataStreamingFrequency_CalculatedFromMainThread, DataStreamingDeltaT_CalculatedFromMainThread]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation_CalculatedFromMainThread ERROR, exceptions: %s" % exceptions)
        return [-11111.0]*4
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LimitNumber_IntOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = int(test_val)

    return test_val
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LimitNumber_FloatOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = float(test_val)

    return test_val
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LimitTextEntryInput(min_val, max_val, test_val, TextEntryObject):

    test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

    if test_val > max_val:
        test_val = max_val
    elif test_val < min_val:
        test_val = min_val
    else:
        test_val = test_val

    if TextEntryObject != "":
        if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
            TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
        else:
            TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

    return test_val
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TellWhichFileWereIn():

    #We used to use this method, but it gave us the root calling file, not the class calling file
    #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

    frame = inspect.stack()[1]
    filename = frame[1][frame[1].rfind("\\") + 1:]
    filename = filename.replace(".py","")

    return filename
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def IsInputList(InputToCheck):

    result = isinstance(InputToCheck, list)
    return result
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def IsListAllNumbers(InputList):

    for item in InputList:
        try:
            FloatNumber = float(only_numerics(str(item))) #only_numerics needs the str of the number for it to convert properly
        except:
            return 0

    return 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def AddAnumberToEveryElementInAlist(ListInput, NumberToBeAddedToEveryElement):

    if IsInputList(ListInput) == 1:
        if IsListAllNumbers(ListInput) == 1:
            NewListWithNumberAddedToEveryElement = list([x + NumberToBeAddedToEveryElement for x in ListInput])
            return NewListWithNumberAddedToEveryElement
        else:
            print("AddAnumberToEveryElementInAlist: ERROR, ListInput must be all numbers!")
            return list()
    else:
        print("AddAnumberToEveryElementInAlist: ERROR, ListInput must be type 'List'; currently it is type " + str(type(ListInput)))
        return list()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def MultiplyAnumberWithEveryElementInAlist(ListInput, NumberToBeMultipliedWithEveryElement):

    if IsInputList(ListInput) == 1:
        if IsListAllNumbers(ListInput) == 1:
            NewListWithNumberMultipliedWithEveryElement = list([x * NumberToBeMultipliedWithEveryElement for x in ListInput])
            return NewListWithNumberMultipliedWithEveryElement
        else:
            print("MultiplyAnumberWithEveryElementInAlist: ERROR, ListInput must be all numbers!")
            return list()
    else:
        print("MultiplyAnumberWithEveryElementInAlist: ERROR, ListInput must be type 'List'; currently it is type " + str(type(ListInput)))
        return list()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction):

    TimerObject = threading.Timer(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction) #Must pass arguments to callback-function via list as the third argument to Timer call
    TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
    TimerObject.start()

    print("TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(getPreciseSecondsTimeStampString()))

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TimerCallbackFunctionWithFunctionAsArgument_Repeating_NoParenthesesAfterFunctionName(CycleTimeDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName):

    #print("TimerCallbackFunctionWithFunctionAsArgument_Repeating_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(getPreciseSecondsTimeStampString()))
    FunctionToCall_NoParenthesesAfterFunctionName()

    TimerObject = threading.Timer(CycleTimeDeltaTseconds, TimerCallbackFunctionWithFunctionAsArgument_Repeating_NoParenthesesAfterFunctionName, [CycleTimeDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName]) #Must pass arguments to callback-function via list as the third argument to Timer call
    TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
    TimerObject.start()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertListOfValuesDegToRad(ListOfValuesDegToRadToBeConverted):

    ListOfValuesRadToBeReturned = list()

    try:
        if IsInputList(ListOfValuesDegToRadToBeConverted) == 0:
            ListOfValuesDegToRadToBeConverted = list([ListOfValuesDegToRadToBeConverted])

        for index, value in enumerate(ListOfValuesDegToRadToBeConverted):
            ListOfValuesRadToBeReturned.append(value*math.pi/180.0)

        return ListOfValuesRadToBeReturned

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertListOfValuesDegToRad Exceptions: %s" % exceptions)
        return ListOfValuesRadToBeReturned
        #traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertListOfValuesRadToDeg(ListOfValuesRadToDegToBeConverted):

    ListOfValuesDegToBeReturned = list()

    try:
        if IsInputList(ListOfValuesRadToDegToBeConverted) == 0:
            ListOfValuesDegToRadToBeConverted = list([ListOfValuesRadToDegToBeConverted])

        for index, value in enumerate(ListOfValuesRadToDegToBeConverted):
            ListOfValuesDegToBeReturned.append(value*180.0/math.pi)

        return ListOfValuesDegToBeReturned

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertListOfValuesRadToDeg Exceptions: %s" % exceptions)
        return ListOfValuesDegToBeReturned
        #traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread_CreateRootAndSetRootParameters(GlobalsDict):

    ########################################################### KEY GUI LINE
    ###########################################################
    GlobalsDict["root"] = Tk()
    ###########################################################
    ###########################################################

    ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
    ###################################################
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)
    GlobalsDict["root"].option_add("*Font", default_font)
    ###################################################
    ###################################################

    ###################################################
    ###################################################
    GlobalsDict["TKinter_LightRedColor"] = '#%02x%02x%02x' % (255, 150, 150)  # RGB
    GlobalsDict["TKinter_LightGreenColor"] = '#%02x%02x%02x' % (150, 255, 150)  # RGB
    GlobalsDict["TKinter_LightBlueColor"] = '#%02x%02x%02x' % (150, 150, 255)  # RGB
    GlobalsDict["TKinter_LightYellowColor"] = '#%02x%02x%02x' % (255, 255, 150)  # RGB
    GlobalsDict["TKinter_DefaultGrayColor"] = '#%02x%02x%02x' % (240, 240, 240)  # RGB
    ###################################################
    ###################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread_StartRootLoopAndHandleExitOfGUI(GlobalsDict):

    ###########################################################
    root = GlobalsDict["root"]
    ExitProgram_Callback = GlobalsDict["ExitProgram_Callback"]
    GUI_update_clock = GlobalsDict["GUI_update_clock"]
    ###########################################################

    ###########################################################
    if "GUI_RootAfterCallbackInterval_Milliseconds" in GlobalsDict:
        GUI_RootAfterCallbackInterval_Milliseconds = GlobalsDict["GUI_RootAfterCallbackInterval_Milliseconds"]
    else:
        GUI_RootAfterCallbackInterval_Milliseconds = 30
    ###########################################################

    ###########################################################
    if "GUItitleString" in GlobalsDict:
        GUItitleString = GlobalsDict["GUItitleString"]
    else:
        GUItitleString = ""
    ###########################################################

    ###########################################################
    if "root_width" in GlobalsDict:
        root_width = GlobalsDict["root_width"]
    else:
        root_width = 1820
    ###########################################################

    ###########################################################
    if "root_height" in GlobalsDict:
        root_height = GlobalsDict["root_height"]
    else:
        root_height = 1000
    ###########################################################

    ###########################################################
    if "root_Xpos" in GlobalsDict:
        root_Xpos = GlobalsDict["root_Xpos"]
    else:
        root_Xpos
    ###########################################################

    ###########################################################
    if "root_Ypos" in GlobalsDict:
        root_Ypos = GlobalsDict["root_Ypos"]
    else:
        root_Ypos = 0
    ###########################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title(GUItitleString)
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.mainloop()
    #################################################

    ################################################# THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread_CreateAndStart(GlobalsDict):

    print("Starting GUI thread...")
    GlobalsDict["GUI_Thread_ThreadingObject"] = threading.Thread(target=GlobalsDict["GUI_Thread"])
    GlobalsDict["GUI_Thread_ThreadingObject"].setDaemon(True)  # Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
    GlobalsDict["GUI_Thread_ThreadingObject"].start()
    time.sleep(0.5)  # Allow enough time for 'root' to be created that we can then pass it into other classes.

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ParseARGV_USE_GUI_and_SOFTWARE_LAUNCH_METHOD():

    try:
        USE_GUI_FLAG_ARGV_OVERRIDE = -1
        SOFTWARE_LAUNCH_METHOD = -1

        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1].strip().lower()

            print("ARGV_1: " + str(ARGV_1))
            ARGV_1_ParsedDict = ParseColonCommaSeparatedVariableString(ARGV_1)

            if "use_gui_flag" in ARGV_1_ParsedDict:
                USE_GUI_FLAG_ARGV_OVERRIDE = PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG_ARGV_OVERRIDE", int(ARGV_1_ParsedDict["use_gui_flag"]))

            if "software_launch_method" in ARGV_1_ParsedDict:
                SOFTWARE_LAUNCH_METHOD = ARGV_1_ParsedDict["software_launch_method"]

    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions)
        traceback.print_exc()
        time.sleep(0.25)

    #print("ARGV_1, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE))
    #print("ARGV_1, SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

    return [USE_GUI_FLAG_ARGV_OVERRIDE, SOFTWARE_LAUNCH_METHOD]

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ListFunctionNamesInClass(ClassToBeChecked, FilterFunctionNamesWithLeadingUnderscoresFlag = 1):
    FunctionList_All = list()

    for FunctionName, item in ClassToBeChecked.__dict__.items():
        if isinstance(item, types.FunctionType):
            if FilterFunctionNamesWithLeadingUnderscoresFlag == 0:
                FunctionList_All.append(FunctionName)
            else:
                if FunctionName[0] != "_":
                    FunctionList_All.append(FunctionName)

    return FunctionList_All
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SortListAlphabetically(InputList):
    try:
        OutputList = sorted(InputList, key=lambda v: v.lower())
        return OutputList
    except:
        exceptions = sys.exc_info()[0]
        print("SortListAlphabetically, exceptions: %s" % exceptions)
        return list()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def IsModuleNameStringInPythonStdLibrary(ModuleNameStringToCheck, PythonVersion = -1): #Requires"pip install stdlib_list"

    try:
        PythonVersion = str(PythonVersion)

        if PythonVersion == "-1":
            ListOfAllModuleNameStringInPythonStdLibrary = stdlib_list('.'.join([str(v) for v in sys.version_info[0:2]])) #Uses version of current Python interpreter running this code.
        else:
            ListOfAllModuleNameStringInPythonStdLibrary = stdlib_list(PythonVersion)

        if ModuleNameStringToCheck in ListOfAllModuleNameStringInPythonStdLibrary:
            return 1
        else:
            return 0
    except:
        exceptions = sys.exc_info()[0]
        print("IsModuleNameStringInPythonStdLibrary, exceptions: %s" % exceptions)
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SetAllFTDIdevicesLatencyTimer(FTDI_LatencyTimer_ToBeSet = 1):

    try:
        FTDI_LatencyTimer_ToBeSet = LimitNumber_IntOutputOnly(1, 16, FTDI_LatencyTimer_ToBeSet)

        FTDI_DeviceList = ftd2xx.listDevices()
        print("FTDI_DeviceList: " + str(FTDI_DeviceList))

        if FTDI_DeviceList != None:

            for Index, FTDI_SerialNumber in enumerate(FTDI_DeviceList):

                #################################
                try:
                    if sys.version_info[0] < 3: #Python 2
                        FTDI_SerialNumber = str(FTDI_SerialNumber)
                    else:
                        FTDI_SerialNumber = FTDI_SerialNumber.decode('utf-8')

                    FTDI_Object = ftd2xx.open(Index)
                    FTDI_DeviceInfo = FTDI_Object.getDeviceInfo()

                    '''
                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          ", DeviceInfo: " +
                          str(FTDI_DeviceInfo))
                    '''

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not open FTDI device, Exceptions: %s" % exceptions)
                #################################

                #################################
                try:
                    FTDI_Object.setLatencyTimer(FTDI_LatencyTimer_ToBeSet)
                    time.sleep(0.005)

                    FTDI_LatencyTimer_ReceivedFromDevice = FTDI_Object.getLatencyTimer()
                    FTDI_Object.close()

                    if FTDI_LatencyTimer_ReceivedFromDevice == FTDI_LatencyTimer_ToBeSet:
                        SuccessString = "succeeded!"
                    else:
                        SuccessString = "failed!"

                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          " commanded setLatencyTimer(" +
                          str(FTDI_LatencyTimer_ToBeSet) +
                          "), and getLatencyTimer() returned: " +
                          str(FTDI_LatencyTimer_ReceivedFromDevice) +
                          ", so command " +
                          SuccessString)

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not set/get Latency Timer, Exceptions: %s" % exceptions)
                #################################

        else:
            print("SetAllFTDIdevicesLatencyTimer ERROR: FTDI_DeviceList is empty, cannot proceed.")

    except:
        exceptions = sys.exc_info()[0]
        print("SetAllFTDIdevicesLatencyTimer, Exceptions: %s" % exceptions)

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def FindAssignAndOpenSerialPort():
    print("FindAssignAndOpenSerialPort: Finding all serial ports...")

    ##############
    SerialNumberToCheckAgainst = str(DesiredSerialNumber)
    if my_platform == "linux" or my_platform == "pi":
        SerialNumberToCheckAgainst = SerialNumberToCheckAgainst[:-1] #The serial number gets truncated by one digit in linux
    else:
        SerialNumberToCheckAgainst = SerialNumberToCheckAgainst
    ##############

    ##############
    SerialPortsAvailable_ListPortInfoObjetsList = serial.tools.list_ports.comports()
    ##############

    ###########################################################################
    SerialNumberFoundFlag = 0
    for SerialPort_ListPortInfoObjet in SerialPortsAvailable_ListPortInfoObjetsList:

        SerialPortName = SerialPort_ListPortInfoObjet[0]
        Description = SerialPort_ListPortInfoObjet[1]
        VID_PID_SerialNumber_Info = SerialPort_ListPortInfoObjet[2]
        print(SerialPortName + ", " + Description + ", " + VID_PID_SerialNumber_Info)

        if VID_PID_SerialNumber_Info.find(SerialNumberToCheckAgainst) != -1 and SerialNumberFoundFlag == 0: #Haven't found a match in a prior loop
            SerialPortNameCorrespondingToCorrectSerialNumber = SerialPortName
            SerialNumberFoundFlag = 1 #To ensure that we only get one device
            print("FindAssignAndOpenSerialPort: Found serial number " + SerialNumberToCheckAgainst + " on port " + SerialPortNameCorrespondingToCorrectSerialNumber)
            #WE DON'T BREAK AT THIS POINT BECAUSE WE WANT TO PRINT ALL SERIAL DEVICE NUMBERS WHEN PLUGGING IN A DEVICE WITH UNKNOWN SERIAL NUMBE RFOR THE FIRST TIME.
    ###########################################################################

    ###########################################################################
    if(SerialPortNameCorrespondingToCorrectSerialNumber != "default"): #We found a match

        try: #Will succeed as long as another program hasn't already opened the serial line.

            SerialObject = serial.Serial(SerialPortNameCorrespondingToCorrectSerialNumber, SerialBaudRate, timeout=SerialTimeoutSeconds, parity=SerialParity, stopbits=SerialStopBits, bytesize=SerialByteSize)
            SerialConnectedFlag = 1
            print("FindAssignAndOpenSerialPort: Serial is connected and open on port: " + SerialPortNameCorrespondingToCorrectSerialNumber)

        except:
            SerialConnectedFlag = 0
            print("FindAssignAndOpenSerialPort: ERROR: Serial is physically plugged in but IS IN USE BY ANOTHER PROGRAM.")

    else:
        SerialConnectedFlag = -1
        print("FindAssignAndOpenSerialPort: ERROR: Could not find the serial device. IS IT PHYSICALLY PLUGGED IN?")
    ###########################################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertBytesObjectToString(InputBytesObject):

    if sys.version_info[0] < 3:  # Python 2
        OutputString = str(InputBytesObject)

    else:
        OutputString = InputBytesObject.decode('utf-8')

    return OutputString
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def AverageDataInQueueOfLists(InputQueue):
    try:

        if isinstance(InputQueue, Queue.Queue) == 1:

            InputQueueSize = InputQueue.qsize()

            if InputQueueSize > 0:
                DataElement = InputQueue.get()

                IsListFlag = 1
                ####
                if isinstance(DataElement, list) == 0:  # If not a list, make it one.
                    DataElement = [DataElement]
                    IsListFlag = 0
                ####

                DataElementListLength = len(DataElement)

                SumOfIndex_List = list()
                for Value in DataElement:
                    SumOfIndex_List.append(Value)  # Just to initialize SumOfIndex_List with the first element that we removed.

                ##########################################################################################################
                while InputQueue.qsize() > 0:
                    DataElementValue = InputQueue.get()

                    if IsListFlag == 0:
                        DataElementValue = [DataElementValue]

                    for Index in range(0, DataElementListLength):
                        SumOfIndex_List[Index] = SumOfIndex_List[Index] + DataElementValue[Index]

                ##########################################################################################################

                ##########################################################################################################
                AverageOfIndex_List = [0.0] * DataElementListLength
                for Index in range(0, DataElementListLength):
                    AverageOfIndex_List[Index] = SumOfIndex_List[Index] / InputQueueSize
                ##########################################################################################################

                return AverageOfIndex_List

            else:
                print("AverageDataInQueueOfLists, Error: Queue is empty!")
                return [-11111.0]

        else:
            print("AverageDataInQueueOfLists, Error: Input must be a Queue.Queue!")
            return [-11111.0]

    except:
        ##########################################################################################################
        exceptions = sys.exc_info()[0]
        print("AverageDataInQueueOfLists, Exceptions: %s" % exceptions)
        traceback.print_exc()

        #########################################################
        if InputQueue.qsize() > 0:
            DataElement = InputQueue.get()
            if isinstance(DataElement, list) == 1:
                return [-11111.0] * len(DataElement)
            else:
                return [-11111.0]
        else:
            return [-11111.0]
        #########################################################

        ##########################################################################################################

##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
def CreateNewDirectoryIfItDoesntExist(directory):
    try:
        #print("CreateNewDirectoryIfItDoesntExist, directory: " + directory)
        if os.path.isdir(directory) == 0: #No directory with this name exists
            os.makedirs(directory)
    except:
        exceptions = sys.exc_info()[0]
        print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def CreateNewCSVfileIfItDoesntExist(FileFullPathToCheck):
    try:
        if os.path.isfile(FileFullPathToCheck) == 0:
            with open(FileFullPathToCheck, "w") as my_empty_csv:
                pass
    except:
        exceptions = sys.exc_info()[0]
        print("CreateNewCSVfileIfItDoesntExist ERROR, Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def TimeFunctionCallOverManyIterations(FunctionToCall, ArgumentList, NumberOfIterations = 1000):

    StartingTime = time.time()

    for Counter in range(1, NumberOfIterations):
        FunctionToCall(*ArgumentList) #* says to unwrap the list of arguments into individual arguments.

    EndingTime = time.time()

    TimePerFunctionCallInseconds = (EndingTime - StartingTime) / float(NumberOfIterations)
    print("TimeFunctionCallOverManyIterations: After running " + str(NumberOfIterations) + " iterations, found that TimePerFunctionCallInseconds for function '" + FunctionToCall.__name__ + "': " + str(TimePerFunctionCallInseconds))

    return TimePerFunctionCallInseconds
#######################################################################################################################
#######################################################################################################################

###########################################################################################################
##########################################################################################################
def ComputeListNorm(InputList):
    #print("ComputeListNorm: InputList = " + str(InputList))

    norm = -1

    try:
        ElementsSquaredSum = 0.0
        for InputElement in InputList:
            InputElement = float(InputElement)
            ElementsSquaredSum = ElementsSquaredSum + InputElement * InputElement

        norm = math.sqrt(ElementsSquaredSum)

    except:
        exceptions = sys.exc_info()[0]
        print("ComputeListNorm Error, Exceptions: %s" % exceptions)

    return norm
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def NormalizeListToUnitLength(InputList):
    OutputList = list(InputList)

    try:
        ElementsSquaredSum = 0.0
        for InputElement in InputList:
            InputElement = float(InputElement)
            ElementsSquaredSum = ElementsSquaredSum + InputElement * InputElement

        norm = math.sqrt(ElementsSquaredSum)

        for i, InputElement in enumerate(InputList):
            InputElement = float(InputElement)
            OutputList[i] = InputElement / norm

    except:
        exceptions = sys.exc_info()[0]
        print("NormalizeListToUnitLength Error, Exceptions: %s" % exceptions)

    return OutputList
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def MultiplyListOfNumbersByScalar(InputList, ScalarToMultiplyBy):
    OutputList = list(InputList)

    try:
        for i, OutputElement in enumerate(OutputList):
            OutputElementFloat = float(OutputElement)
            OutputList[i] = ScalarToMultiplyBy*OutputElementFloat

    except:
        exceptions = sys.exc_info()[0]
        print("MultiplyListOfNumbersByScalar Error, Exceptions: %s" % exceptions)
        return list()

    return OutputList
##########################################################################################################
##########################################################################################################
