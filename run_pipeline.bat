
@echo off
cd /d C:\chinni\CityFlow

echo Starting CityFlow ETL pipeline...

.venv\Scripts\python.exe src\pipeline.py
if errorlevel 1 exit /b 1

echo Running data quality tests...

.venv\Scripts\python.exe -m pytest tests -v
if errorlevel 1 exit /b 1

echo CityFlow pipeline and tests completed successfully.
exit /b 0
