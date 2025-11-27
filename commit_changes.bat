@echo off
REM Quick script to stage and commit the v2.9.0 restructure

echo ======================================================================
echo STAGING ALL CHANGES FOR COMMIT
echo ======================================================================
echo.

git add -A

echo.
echo ======================================================================
echo COMMITTING WITH STANDARDIZED MESSAGE
echo ======================================================================
echo.

git commit -m "refactor(repo): align Goku.AI to Master Prompt v2.9.0 standards" -m "- Implemented Strangler Fig remediation pattern" -m "- Created v2.9.0 compliant directory structure" -m "- Migrated 441 files from legacy structure" -m "- Organized scripts by OS (Windows/Linux)" -m "- Added mandatory configuration files (.vscode, .editorconfig)" -m "- Created installation/uninstallation scripts per OS" -m "- Standardized repository organization (src/, docs/, config/, scripts/, tests/)" -m "" -m "BREAKING CHANGE: Repository structure completely reorganized" -m "Ref: Master Prompt v2.9.0 Section 18.10"

echo.
echo ======================================================================
echo COMMIT COMPLETE
echo ======================================================================
echo.
echo Next: git push origin main
echo.

pause

