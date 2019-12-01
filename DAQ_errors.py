#!/usr/bin/env python3

# SCPI Errors
# -100 to -200 Command Errors
# -200 to -299 Execution Errors
# -300 to -399 SCPI Specified Device-Specific Errors
# -400 to -800 Query and System Errors
# 100 to 200  PNA-specific Errors
# http://na.support.keysight.com/pna/help/latest/Support/SCPI_Errors.htm

# -100 to -200 Command Errors
# A command error indicates that the test set's GPIB parser has detected an IEEE 488.2 syntax error.
# When one of these errors is generated, the command error bit in the event status register is set.

SCPI_error = {-100, ["std_command", "Command - This event bit (Bit 5) indicates a syntax error, or a semantic error, or a GET command was entered, see IEEE 488.2, 11.5.1.1.4.

-101

std_invalidChar

Invalid character - Indicates a syntactic elements contains a character which is invalid for that type.

-102

std_syntax

Syntax - Indicates that an unrecognized command or data type was encountered. For example, a string was received when the device does not accept strings.

-103

std_invalidSeparator

Invalid separator - The parser was expecting a separator and encountered an illegal character. For example, the semicolon was omitted after a program message unit.

-104

std_wrongParamType

Data type -The parser recognized a data element different than one allowed. For example, numeric or string data was expected but block data was encountered.

-105

std_GETNotAllowed

GET not allowed - Indicates a Group Execute Trigger was received within a program message. Correct the program so that the GET does not occur within the program code.

-108

std_tooManyParameters

Parameter not allowed - Indicates that more parameters were received than expected for the header. For example, *ESE common command only accepts one parameter, so *ESE 0,1 is not allowed.

-109

std_tooFewParameters

Missing parameter - Indicates that less parameters were received than required for the header. For example, *ESE requires one parameter, *ESE is not allowed.

-110

std_cmdHeader

Command header - Indicates an error was detected in the header. This error is used when the device cannot detect the more specific errors -111 through -119.

-111

std_headerSeparator

Header separator - Indicates that a character that is not a legal header separator was encountered while parsing the header.

-112

std_IDTooLong

Program mnemonic too long - Indicates that the header contains more that twelve characters, see IEEE 488.2, 7.6.1.4.1.

-113

std_undefinedHeader

Undefined header - Indicates the header is syntactically correct, but it is undefined for this specific device. For example, *XYZ is not defined for any device.

-114

std_suffixOutOfRange

Header suffix out of range - Indicates the value of a header suffix attached to a program mnemonic makes the header invalid.

-120

std_numericData

Numeric data - This error, as well as errors

-121

std_invalidCharInNumber

Invalid character in number - Indicates an invalid character for the data type being parsed was encountered. For example, an alpha in a decimal numeric or a "9" in octal data.

-123

std_exponentTooLarge

Exponent too large - Indicates the magnitude of an exponent was greater than 32000, see IEEE 488.2, 7.7.2.4.1.

-124

std_decimalTooLong

Too many digits - Indicates the mantissa of a decimal numeric data element contained more than 255 digits excluding leading zeros, see IEEE 488.2, 7.7.2.4.1.

-128

std_numericNotAllowed

Numeric data not allowed - Indicates that a legal numeric data element was received, but the device does not accept one in this position for the header.

-130

std_suffix

Suffix - This error, as well as errors -131 through -139, are generated when parsing a suffix. This particular error message is used if the device cannot detect  a more specific error.

-131

std_badSuffix

Invalid suffix - Indicates the suffix does not follow the syntax described in IEEE 488.2, 7.7.3.2, or the suffix is inappropriate for this device.

-134

std_suffixTooLong

Suffix too long - Indicates the suffix contain more than 12 characters, see IEEE 488.2, 7.7.3.4.

-138

std_suffixNotAllowed

Suffix not allowed - Indicates that a suffix was encountered after a numeric element that does not allow suffixes.

-140

std_charData

Character data - This error, as well as errors

-141

std_invalidCharData

Invalid character data - Indicates that the character data element contains an invalid character or the particular element received is not valid for the header.

-144

std_charDataTooLong

Character data too long - Indicates the character data element contains more than twelve characters, see IEEE 488.2, 7.7.1.4.

-148

std_charNotAllowed

Character data not allowed - Indicates a legal character data element was encountered where prohibited by the device.

-150

std_stringData

String data - This error, as well as errors

-151

std_stringInvalid

Invalid string data - Indicates that a string data element was expected, but was invalid, see IEEE 488.2, 7.7.5.2. For example, an END message was received before the terminal quote character.

-158

std_stringNotAllowed

String data not allowed - Indicates that a string data element was encountered but was not allowed by the device at this point in parsing.

-160

std_blockData

Block data - This error, as well as errors -161 through -169, are generated when parsing a block data element. This particular error message is used if the device cannot detect a more specific error.

-161

std_badBlock

Invalid block data - Indicates a block data element was expected, but was invalid, see IEEE 488.2, 7.7.6.2. For example, and END message was received before the end length was satisfied.

-168

std_blockNotAllowed

Block data not allowed - Indicates a legal block data element was encountered, but not allowed by the device at this point in parsing.

-170

std_expr

Expression - This error, as well as errors -171 through -179, are generated when parsing an expression data element. This particular error message is used if the device cannot detect a more specific error.

-171

std_invalidExpression

Invalid expression - Indicates the expression data element was invalid, see IEEE 488.2, 7.7.7.2. For example, unmatched parentheses or an illegal character.

-178

std_exprNotAllowed

Expression data not allowed - Indicates a legal expression data was encountered, but was not allowed by the device at this point in parsing.

-180

std_macro

Macro - This error, as well as error -181 through -189, are generated when defining a macro or execution a macro. This particular error message is used if the device cannot detect a more specific error.

-181

std_validOnlyInsideMacro

Invalid outside macro definition - Indicates that a macro parameter place holder was encountered outside of a macro definition.

-183

std_invalidWithinMacro

Invalid inside macro definition - Indicates that the program message unit sequence, sent with a *DDT or a *DMC command, is syntactically invalid, see IEEE 488.2, 10.7.6.3.

-184

std_macroParm

Macro parameter - Indicates that a command inside the macro definition had the wrong number or type of parameters.

-200 to -299 Execution Errors
These errors are generated when something occurs that is incorrect in the current state of the instrument. These errors may be generated by a user action from either the remote or the manual user interface

-200

std_execGen

Execution - This event bit (Bit 4) indicates a PROGRAM DATA element following a header was outside the legal input range or otherwise inconsistent with the device's capabilities, see IEEE 488.2, 11.5.1.1.5.

-201

std_invalidWhileInLocal

Invalid while in local

-202

std_settingsLost

Settings lost due to rtl

-203

std_commandProtected

Command protected - Indicates that a legal password-protected program command or query could not be executed because the command was disabled.

-210

std_trigger

Trigger

-211

std_triggerIgnored

Trigger ignored

-212

std_armIgnored

Arm ignored

-213

std_initIgnored

Init ignored

-214

std_triggerDeadlock

Trigger deadlock

-215

std_armDeadlock

Arm deadlock

-220

std_parm

Parameter - Indicates that a program data element related error occurred.

-221

std_settingsConflict

Settings conflict - Indicates that a legal program data element was parsed but could not be executed due to the current device state.

-222

std_dataOutOfRange

Data out of range - Indicates that a legal program data element was parsed but could not be executed because the interpreted value was outside the legal range defined by the devices

-223

std_tooMuchData

Too much data - Indicates that a legal program data element of block, expression, or string type was received that contained more data than the device could handle due to memory or related device-specific requirements.

-224

std_illegalParmValue

Illegal parameter value - Indicates that the value selected was not part of the list of values given.

-225

std_noMemoryForOp

Out of memory - The device has insufficient memory to perform the requested operation.

-226

std_listLength

Lists not same length - Attempted to use LIST structure having individual LIST's of unequal lengths.

-230

std_dataCorruptOrStale

Data corrupt or stale - Indicates invalid data, a new reading started but not completed since the last access.

-231

std_dataQuestionable

Data questionable - Indicates that measurement accuracy is suspect.

-232

std_invalidFormat

Invalid format

-233

std_invalidVersion

Invalid version - Indicates that a legal program data element was parsed but could not be executed because the version of the data is incorrect to the device. For example, a not supported file version, a not supported instrument version.

-240

std_hardware

Hardware - Indicates that a legal program command or query could not be executed because of a hardware problem in the device.

-241

std_hardwareMissing

Hardware missing - Indicates that a legal program command or query could not be executed because of missing device hardware. For example, an option was not installed.

-250

std_massStorage

Mass storage - Indicates that a mass storage error occurred. The device cannot detect the more specific errors described for errors -251 through -259.

-251

std_missingMassStorage

Missing mass storage - Indicates that a legal program command or query could not be executed because of missing mass storage.

-252

std_missingMedia

Missing media - Indicates that a legal program command or query could not be executed because of missing media. For example, no disk.

-253

std_corruptMedia

Corrupt media - Indicates that a legal program command or query could not be executed because of corrupt media. For example, bad disk or wrong format.

-254

std_mediaFull

Media full- Indicates that a legal program command or query could not be executed because the media is full. For example, there is no room left on the disk.

-255

std_directoryFull

Directory full - Indicates that a legal program command or query could not be executed because the media directory was full.

-256

std_fileNotFound

File name not found - Indicates that a legal program command or query could not be executed because the file name was not found on the media.

-257

std_fileName

File name - Indicates that a legal program command or query could not be executed because the file name on the device media was in error. For example, an attempt was made to read or copy a nonexistent file.

-258

std_mediaProtected

Media protected - Indicates that a legal program command or query could not be executed becuse the media was protected. For example, the write-protect switch on a memory card was set.

-260

std_expression

Expression

-261

std_math

Math  in expression

-270

std_macroExecution

Macro - Indicates that a macro related execution error occurred.

-271

std_macroSyntax

Macro syntax - Indicates that a syntactically legal macro program data sequence, according to IEEE 488.2, 10.7.2, could not be executed due to a syntax error within the macro definition.

-272

std_macroExec

Macro execution - Indicates that a syntactically legal macro program data sequence could not be executed due to some error in the macro definition, see IEEE 488.2, 10.7.6.3.

-273

std_badMacroName

Illegal macro label - Indicates that the macro label was not accepted, it did not agree with the definition in IEEE 488.2, 10.7.3

-274

std_macroPlaceholderMa

cro parameter - Indicates that the macro definition improperly used a macro parameter placeholder, see IEEE 4882, 10.7.3.

-275

std_macroTooLong

Macro definition too long - Indicates that a syntactically legal macro program data sequence could not be executed because the string of block contents were too long for the device to handle, IEEE 488.2, 10.7.6.1.

-276

std_macroRecursion

Macro recursion - Indicates that a syntactically legal macro program data sequence count not be executed because it would be recursive, see IEEE 488.2, 10.7.6.6.

-277

std_cantRedefineMacro

Macro redefinition not allowed - Indicates that redefining an existing macro label, see IEEE 488.2, 10.7.6.4.

-278

std_macroNotFound

Macro header not found - Indicates that a legal macro label in the *GMS?, see IEEE 488.2, 10.13, could not be executed because the header was not previously defined.

-280

std_program

Program

-281

std_cantCreateProgram

Cannot create program

-282

std_illegalProgramName

Illegal program name

-283

std_illegalVarName

Illegal variable name

-284

std_programRunning

Program currently running

-285

std_programSyntax

Program syntax

-286

std_programRuntime

Program runtime

-290

std_memoryUse

Memory use

-291

std_execOutOfMemory

Out of memory

-292

std_nameNotFound

Referenced name does not exist

-293

std_nameAlreadyExists

Referenced name already exists

-294

std_incompatibleType

Incompatible type

-300 to -399 SCPI Specified Device-Specific Errors
A device-specific error indicates that the instrument has detected an error that occurred because some operations did not properly complete, possibly due to an abnormal hardware or firmware condition. For example, an attempt by the user to set an out of range value will generate a device specific error. When one of these errors is generated, the device specific error bit in the event status register is set.

-300

std_deviceSpecific

Device specific - This event bit (Bit 3) indicates that a device operation did not properly complete due to some condition, such as overrange see IEEE 488.2, 11.5.1.1.6.

-310

std_system

System

-311

std_memory

Memory - Indicates some physical fault in the devices memory, such as a parity error.

-312

std_PUDmemoryLost

PUD memory lost - Indicates protected user data saved by the *PUD command has been lost, see IEEE 488.2, 10.27.

-313

std_calMemoryLost

Calibration memory lost - Indicates that nonvolatile calibration data used by the *CAL? command has been lost, see IEEE 488.2, 10.2.

-314

std_savRclMemoryLost

Save/recall memory lost - Indicates that the nonvolatile data saved by the *SAV command has been lost, see IEEE 488.2, 10.33.

-315

std_configMemoryLost

Configuration memory lost - Indicates that nonvolatile configuration data saved by the device has been lost.

-320

std_storageFault

Storage fault - Indicates that the firmware detected a fault when using data storage. This is not an indication of physical damage or failure of any mass storage element.

-321

std_outOfMemory

Out of memory - An internal operation needed more memory than was available

-330

std_selfTestFailed

Self-test failed - Indicates a problem with the device that is not covered by a specific error message. The device may require service.

-340

std_calFailed

Calibration failed - Indicates a problem during calibration of the device that is not covered by a specific error.

-350

std_queueOverflow

Queue overflow - Indicates that there is no room in the queue and an error occurred but was not recorded. This code is entered into the queue in lieu of the code that caused the error.

-360

std_comm

Communication - This is the generic communication error for devices that cannot detect the more specific errors described for error -361 through -363.

-361

std_parity

Parity  in program message - Parity bit not correct when data received for example, on a serial port.

-362

std_framing

Framing  in program message - A stop bit was not detected when data was received for example, on a serial port (for example, a baud rate mismatch).

-363

std_inputBufferOverrun

Input buffer overrun - Software or hardware input buffer on serial port overflows with data caused by improper or nonexistent pacing.

-400 to -800 Query and System Errors
A Query error is generated either when data in the instrument's GPIB output queue has been lost, or when an attempt is being made to read data from the output queue when no output is present or pending.

-400

std_queryGen

Query - This event bit (Bit 2) indicates that an attempt to read data from the Output Queues when no output is present or pending, to data in the Output Queue has been lost see IEEE488.2, 11.5.1.1.7.

-410

std_interrupted

Query INTERRUPTED - Indicates the test set has been interrupted by a new program message before it finishes sending a RESPONSE MESSAGE see IEEE 488.2, 6.3.2.3.

-420

std_unterminated

Query UNTERMINATED - Indicates an incomplete Query in the program see IEEE 488.2, 6.3.2.2.

-430

std_deadlocked

Query DEADLOCKED - Indicates that the Input Buffer and Output Queue are full see IEEE 488.2, 6.3.1.7.

-440

std_responseNotAllowed

Query UNTERMINATED after indefinite response - Indicates that a query was received in the same program message after a query requesting an indefinite response was executed see IEEE 488.2, 6.5.7.5.

-500

std_powerOn

Power on

-600

std_userRequest

User request

-700

std_requestControl

Request control

-800

std_operationComplete

Operation complete

.
Analyzer-Specific (Positive) SCPI Errors
100

dupWindNum

"Duplicate window number"

101

windNumNotFound

"Window number not found"

102

failedWindCreate

"Window creation failed"

103

noCalcParamSelection

"CALC measurement selection set to none"

See CALC:PAR:SEL

104

dupMeasName

"Duplicate measurement name"

105

dataNotFound

"Requested data not available"

106

measNotFound

"Requested measurement not found"

107

traceNotFound

"Requested trace not found"

108

notImplemented

"Mnemonic not yet implemented"

109

noDocument

"No measurement container found"

110

dupTraceNum

"Duplicate trace number"

111

titleStrTooLong

"Title string exceeds 50 characters"

112

memoryNotFound

"Requested memory not found"

113

exceedMaxTraces

"Exceeded the maximum number of traces per window"

114

SerNumNotFound

"The serial number was not found. Please store the serial number."

115

LoadFailed

"The state was not loaded. Please check the file name."

116

StoreFailed

"The state was not stored. Please check the file and path names."

117

File

"An  in the File operation occurred. Please check file and path names."

118

measChanConflict

"Measurement does not belong to specified channel."

119

exceedMaxWindows

"Exceeded the maximum number of data windows"

120

markerNotFound

"The specified marker was not found."

121

diagnostic

"Diagnostic ."

122

channelNotFound

"The specified channel was not found."

123

exceedMaxMeasurements

"Exceeded the maximum number of allowed mesurements."

124

parameterOutOfRange

"The specified value was out of range."

125

userRangeNotValid

"The currently selected user range is not valid."

126

referenceMarkerNotFound

"The reference marker is not active."

127

sweepSegmentNotFound

"The sweep segment was not found."

128

markerNotDelta

"The specified marker is not a delta marker."

129

printoutFailed

"Attempt to output to a printer failed."

130

memory_trace_not_compatible

"Memory not compatible. Trace Math not applied."

131

trace_math_reset

"Memory not compatible. Trace Math turned off."

132

hw_read_failed

"Hardware read failed."

133

hw_write_failed

"Hardware write failed."

134

dsp_active

"Failed because DSP was not halted."

135

secure_memory

"Attempt to access secure memory region."

136

snum_protected

"The serial number is protected."

137

snum_format_bad

"The serial number format is bad."

138

snum_already_set

"The serial number is already set."

139

hw_setting_failed

"Hardware setting failed."

140

cal_access_failed

"Calibration data access failed."

141

db_access_failed

"Database access failed."

142

memory_range_exceeded

"Command exceeds usable memory range."

143

lost_phase_lock

"Phase lock has been lost."

144

over_power

"Detected too much power at input."

145

ee_wrt_failed

"EEPROM write failed."

146

yig_cal_failed

"YTO calibration failed."

147

ramp_cal_failed

"Analog ramp calibration failed."

148

dspcom_bad

"DSP communication failed."

149

no_license_found

"Request failed. The required license was not found."

150

argLimited

"The argument was out of range

151

markerBWNotFound

"The Marker Bandwidth was not found."

153

peakNotFound

"The Peak was not found."

154

targetNotFound

"The Target search value was not found."

155

calNotImpl

"The Calibration feature requested is not implemented."

156

calClassNotValidForCalType

"SENS:CORR:CCH measurement selection set to none"

158

calNotValidForConfidenceChe

"Selected measurement does not have a calibration valid for Confidence Check"

159

invalidPort

"Specified port is out of range"

160

invalidPortPath

"ROUT:PATH:DEF:PORT  x, y does not match measurement; setting to defaults"

161

ioInvalidWrite

"Attempted I/O write while port set to read only."

162

ioInvalidRead

"Attempted I/O read from write only port."

163

calsetNotFound

"Requested Cal Set was not found in Cal Set Storage."

164

noCalSetSelected

"There is no Cal Set currently selected for the specified channel."

165

cantDeleteCalSetInUse

"Cannot delete a Cal Set while it is being used."

166

calsetStimChange

"Channel stimulus settings changed to match selected Cal Set."

167

exceedMaxCalSets

"Exceeded the maximum number of cal sets."

168

calCouldNotTurnOn

"A valid calibration is required before correction can be turned on."

169

standardMeasurementRequired

"The attempted operation can only be performed on a standard measurement type."

170

noDivisorBuffer

"A valid divisor buffer is required before normalization can be turned on."

171

InvalidReceiverPowerCalParagraph

"Receiver power cal requires the measurement to be of unratioed power."

172

ecalCouldNotConfigure

"Could not configure the Electronic Calibration system. Check to see if the module is plugged into the proper connector."

173

measHasNoMemoryAlg

"This measurement does not support memory operations"

174

measHasNoNormalizeAlg

"This measurement does not support normalize operations."

175

userCharacterizationNotFound

"User characterization was not found in the Electronic Calibration module."

176

measInvalidBufferSize

"The data provided has an invalid number of points. It could not be stored."