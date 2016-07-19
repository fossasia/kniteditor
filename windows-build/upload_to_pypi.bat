@echo off
cd %~dp0

REM in https://ci.appveyor.com/project/niccokunzmann/knittingpattern/settings/environment
REM set the variables for the python package index http://pypi.python.org/
REM   PYPI_USERNAME
REM   PYPI_PASSWORD
set HOME=.
%PYTHON%\\python.exe setup_pypirc.py || exit 1

REM upload to pypi
REM check for the tags
REM see http://www.appveyor.com/docs/branches#build-on-tags-github-and-gitlab-only
cd ..
echo APPVEYOR_REPO_TAG: %APPVEYOR_REPO_TAG%
echo APPVEYOR_REPO_TAG_NAME: %APPVEYOR_REPO_TAG_NAME%
IF %APPVEYOR_REPO_TAG% == true (
  FOR /F %%V IN ('%PYTHON%\\python.exe setup.py --version') DO (
    IF "v%%V" == "%APPVEYOR_REPO_TAG_NAME%" (
      %PYTHON%\\python.exe setup.py register
      %PYTHON%\\python.exe setup.py bdist_wininst upload
      IF ERRORLEVEL 1 ( 
        echo Error because the build is already uploaded.
      ) ELSE (
        echo Successfully uploaded build.
      )
    ) ELSE (
      echo Invalid tag %APPVEYOR_REPO_TAG_NAME% should be v%%V.
    )
  )
) ELSE (
  echo Normal build without PyPi deployment.
)
