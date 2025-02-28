@echo off
echo Starting Cosmic Snake...
REM Try using python command directly
python cosmic_snake.py 2>nul
if %errorlevel% == 0 goto end

REM If direct command fails, try with full path to Python
echo Python command not found, trying alternative methods...
where python 2>nul
if %errorlevel% == 0 (
    FOR /F "tokens=*" %%i IN ('where python') DO (
        echo Using Python at: %%i
        "%%i" cosmic_snake.py
        goto end
    )
)

REM If all else fails, try using py command
echo Trying 'py' launcher...
py -3 cosmic_snake.py 2>nul
if %errorlevel% == 0 goto end

echo.
echo ERROR: Could not find Python. Please make sure Python is installed and in your PATH.
echo.

:end
pause 