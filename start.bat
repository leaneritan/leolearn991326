@echo off
echo Kick-off! Starting Grammar 1: Coach Leo Edition...
cd docs
start http://localhost:8000
python -m http.server 8000
