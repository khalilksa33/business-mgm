#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"

cd ~/business-mgm

echo "=== Pre-creating database using sudo ==="
echo '*/*iicc2*/*' | sudo -S mysql -e "
CREATE DATABASE IF NOT EXISTS _26i_uk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '_26i_uk'@'localhost' IDENTIFIED BY 'admin_password_123';
GRANT ALL PRIVILEGES ON _26i_uk.* TO '_26i_uk'@'localhost';
FLUSH PRIVILEGES;
"

echo "=== Creating site 26i.uk with --skip-db-creation ==="
bench new-site 26i.uk --force --db-name _26i_uk --db-password admin_password_123 --skip-db-creation --admin-password admin
