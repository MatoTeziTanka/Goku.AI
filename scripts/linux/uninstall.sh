#!/bin/bash
echo "========================================"
echo "  Goku.AI Uninstallation (Linux)"
echo "========================================"
echo
read -p "Are you sure? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Uninstallation cancelled."
    exit 1
fi
echo "Uninstalling..."
pip uninstall -r ../../requirements.txt -y
echo
echo "✅ Uninstallation complete!"
