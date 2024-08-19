echo off
cls
echo L2c.bat
echo Run Latin-to-Cham transcription on indicated SFM file.

REM Set Python script version numbers...
set ods2csvVer=1.1.1
set L2Cver=1.0.0

REM Check for existance of required folders...
cd "\My Paratext Projects\"
if NOT exist ChamTemp md ChamTemp

REM Switch to working directory...
cd "\My Paratext Projects\ChamSpConv"

REM Confirm input file spec ...
if "%~s1"=="" goto help
if not exist ..\Cham\%~nx1 goto inFileNotFound

REM Confirm L2cDict.csv is up to date...
if not exist L2cDict.csv goto updateDictionary
for /F %%f in ('dir /b /OD L2cDict.csv L2cDict.ods ^| more +1') do set NEWER=%%f
if /I not %NEWER%==L2cDict.ods goto dictionaryOK
:updateDictionary
python ods2csv-%ods2csvVer%.py L2cDict.ods 
:dictionaryOK

REM verify dictionary date...
REM this is for debugging--it can be commented out of production file.
REM echo Verify that the L2cDict.CSV file is newer than L2cDict.ODS...
REM dir L2cDict.*
REM pause

echo Running pre-usfm...
REM pre-usfm.py fixes the SFM file so it is compatible with usfmtec
python pre-usfm.py ..\Cham\%~nx1 ..\ChamTemp\%~n1-temp1%~x1
rem pause

echo Running usfmtec (dictionary lookup)...
REM python usfmtec -d L2cDict.csv -l --no-warnings -S custom-L2C.sty -o ..\ChamTemp\%~n1-temp2%~x1 ..\ChamTemp\%~n1-temp1%~x1
python C:\ChamSpConv-PythonLibs\palaso-python\scripts\sfm\usfmtec -d L2cDict.csv -l --no-warnings -S custom-L2C.sty -o ..\ChamTemp\%~n1-temp2%~x1 ..\ChamTemp\%~n1-temp1%~x1
if ERRORLEVEL 1 goto usfmtecFail
rem pause

echo Running post-usfm...
REM post-usfm.py removes the tweaks that pre-usfm.py created.
python post-usfm.py ..\ChamTemp\%~n1-temp2%~x1 ..\ChamTemp\%~n1-temp3%~x1

echo Running spelling conversion...
python cjm-Latn2Cham-%L2Cver%.py ..\ChamTemp\%~n1-temp3%~x1 ..\ChamScr\%~n1Scr%~x1
rem pause

goto done

:usfmtecFail
echo. 
echo **********
echo *** ERROR: usfmtec dictionary lookup failed.
echo **********
goto done

:inFileNotFound
echo.
echo ERROR: cannot find input file ..\Cham\%~nx1
:help
echo.
echo Syntax:
echo L2c ^<SFMfile^>
echo.
echo The SFM file MUST be in the folder "\My Paratext Projects\Cham"
echo The output file will be put into the folder "\My Paratext Projects\ChamScript"
echo The working folder will be "\My Paratext Projects\ChamSpConv"
echo.
goto done


REM INFO FOR PROGRAMMERS
REM
REM usfmtect Syntax:
REM python <PythonScriptFolder>\usfmtec [options] <SFMfile>
REM partial list of options:
REM	-d PATH		CSV dictionary
REM	--dict-input=DICTINPUT		Input column number of CSV dictionary [0]
REM	--dict-output=DICTOUTPUT	Output column number of CSV dictionary [0]
REM	--dict-context=DICTTAG		Marker context column number of CSV dictionary [0]
REM					Cells contain a space seperated list of required markers.
REM	-n		No USFM, just plain text
REM	-o PATH		output path or directory
REM	-p PATH		Python path containing converter code
REM	--pythonfunc=PYTHONFUNC 	Function name within python file
REM	-s		"strict" parsing of format markers
REM	-l		"loose" parsing of format markers
REM	-S PATH		User stylesheet to add/override markers in default USFM stylesheet
REM For more info on usfmtec, run:
REM 	python C:\PalasoPy\usfmtec --help
REM QUESTIONS:
REM --dict-context	clarify how this is used.

:done
pause
