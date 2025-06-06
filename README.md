# Key Management Service (KMS)

A secure and centralized system for managing cryptographic keys in cloud-based applications.

## Overview

This KMS provides functionality for generating, storing, distributing, and controlling the use of cryptographic keys according to established policies. It integrates with Hardware Security Modules (HSMs) via the PKCS#11 interface.

## Features

- HSM integration through PKCS#11
- Key lifecycle management
- Policy-based access control
- Audit logging
- Secure API for cryptographic operations
- Support for key rotation and versioning

## Setup

### Requirements

- Python 3.11 or higher
- SoftHSM v2 (for development/testing)
- PKCS#11 library

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize SoftHSM: `python setup.py --init-hsm`
4. Start the server: `python main.py`

## API Documentation

The KMS exposes a RESTful API for key management and cryptographic operations.

DONE:
- `/login`: Authenticate and get access token
- `/encrypt`: Encrypt data using a key
- `/decrypt`: Decrypt data using a key
- `/verify`: Verify a signature

NOT DONE:
- `/keys`: List and create keys
- `/keys/<key_label>`: Delete a key
- `/sign`: Sign data using a key
- `/wrap`: Wrap a key using another key
- `/unwrap`: Unwrap a key

### Routes
/login
- Authenticate and get access token

/logout
- Destroy session in HSM

/dashboard
- Dashboard with all contents

/encrypt
- Encrypt data using a key

/decrypt
- Decrypt data using a key

/download/<filename>
- Download encrypted or decrypted file

/admin
- for administration settings

/admin/register 
- register new user with different permissions ('admin' or default 'user')

## Architecture

The system consists of the following components:

1. **HSM Interface**: Provides low-level access to HSM functions via PKCS#11
2. **Key Operations**: High-level cryptographic operations
3. **Policy Engine**: Enforces security policies for access control
4. **API Server**: RESTful interface for client applications
5. **Key Lifecycle Management**: Manages the complete key lifecycle
6. **Audit Logging**: Secure, tamper-evident logging for compliance

## Security

- All cryptographic operations are performed inside the HSM
- Access control based on roles and policies
- Dual control for sensitive operations
- Encrypted communications using TLS
- Comprehensive audit logging

## Development

### Testing

Run tests with pytest:

```
pytest
```

### Adding New Features

1. Implement the feature in the appropriate module
2. Add tests to ensure functionality
3. Update documentation
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
