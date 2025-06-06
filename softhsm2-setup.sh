#!/bin/bash
# Script to install and configure SoftHSM2

# Check if running with sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as root or with sudo"
  exit
fi

# Install SoftHSM2 and required dependencies
echo "Installing SoftHSM2 and dependencies..."
apt-get update
apt-get install -y softhsm2 libsofthsm2 opensc libp11-3 openssl libengine-pkcs11-openssl

# Create directories for SoftHSM2 tokens
echo "Creating SoftHSM2 directories..."
mkdir -p /var/lib/softhsm/tokens
chmod 755 /var/lib/softhsm/tokens

# Configure SoftHSM2
echo "Configuring SoftHSM2..."
cat > /etc/softhsm/softhsm2.conf << EOF
directories.tokendir = /var/lib/softhsm/tokens
objectstore.backend = file
log.level = INFO
slots.removable = false
EOF

export SOFTHSM2_CONF=/etc/softhsm/softhsm2.conf

# Initialize HSM slots
echo "Initializing HSM slots..."

# Initialize Master HSM with PIN and label
softhsm2-util --init-token --slot 0 --label "MasterHSM" --pin 1234 --so-pin 5678
echo "Master HSM initialized at slot 0"

# Initialize User HSM with PIN and label
softhsm2-util --init-token --slot 1 --label "UserHSM" --pin 1234 --so-pin 5678
echo "User HSM initialized at slot 1"

# Initialize Admin HSM with PIN and label
softhsm2-util --init-token --slot 2 --label "AdminHSM" --pin 1234 --so-pin 5678
echo "Admin HSM initialized at slot 2"

echo "SoftHSM2 setup completed successfully!"
echo "Please remember to change the default PINs in a production environment."
