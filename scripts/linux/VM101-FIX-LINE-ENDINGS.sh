#!/bin/bash
# Fix line endings for all shell scripts in deployment package
# Run this on VM101 after transferring files

cd ~/VM101-DEPLOYMENT-PACKAGE-v1.0.0/

echo "Converting line endings from Windows (CRLF) to Unix (LF)..."

# Check if dos2unix is available
if command -v dos2unix &> /dev/null; then
    echo "Using dos2unix..."
    dos2unix *.sh
else
    echo "dos2unix not found, using sed..."
    # Use sed to remove carriage returns
    for file in *.sh; do
        sed -i 's/\r$//' "$file"
    done
fi

# Make sure all scripts are executable
chmod +x *.sh

echo "✅ Line endings fixed!"
echo "✅ Scripts are now executable"
echo ""
echo "Try running again:"
echo "  ./MASTER-DEPLOYMENT-EXECUTOR.sh"



