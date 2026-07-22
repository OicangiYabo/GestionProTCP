import subprocess
import os

ks_path = r"C:\Users\Ignacio\flutter\debug.keystore"
if os.path.exists(ks_path):
    print("Keystore ya existe")
    exit(0)

# Buscar keytool en el sistema
possible_paths = [
    r"C:\Program Files\Java\jdk*\bin\keytool.exe",
    r"C:\Program Files (x86)\Java\jdk*\bin\keytool.exe",
    os.path.expandvars(r"%JAVA_HOME%\bin\keytool.exe"),
]

import glob
found = False
for pattern in possible_paths:
    for f in glob.glob(pattern):
        try:
            result = subprocess.run([
                f, "-genkey", "-v", "-keystore", ks_path,
                "-alias", "debug",
                "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000",
                "-storepass", "android",
                "-keypass", "android",
                "-dname", "CN=Debug, OU=Dev, O=GestionPro, L=Habana, ST=Habana, C=CU"
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Keystore creado en {ks_path}")
                found = True
                break
            else:
                print(f"Error con {f}: {result.stderr}")
        except Exception as e:
            print(f"Error ejecutando {f}: {e}")
    if found:
        break

if not found:
    print("No se encontró keytool. Intentando con Python puro...")
    # Generar un keystore usando Python
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        import datetime

        # Generar clave RSA
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Crear certificado autofirmado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CU"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Habana"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Habana"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "GestionPro"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Debug"),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=10000)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        ).sign(key, hashes.SHA256(), default_backend())

        # Guardar como PKCS12 (keystore)
        from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates

        pkcs12 = serialize_key_and_certificates(
            b"debug",
            key,
            cert,
            None,
            b"android"
        )

        with open(ks_path, "wb") as f:
            f.write(pkcs12)

        print(f"Keystore creado con Python en {ks_path}")
    except ImportError:
        print("No se pudo generar keystore. Instala cryptography: pip install cryptography")
