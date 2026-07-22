import zipfile, os, re

apk = r"D:\AAA OPERATIVO\APLICACION MOVIL PARA TCP\GestionProTCP-app\GestionProTCP.apk"
z = zipfile.ZipFile(apk)

# Check signature
if "META-INF/CERT.RSA" in z.namelist():
    cert = z.read("META-INF/CERT.RSA")
    if b"CN=Android Debug" in cert:
        print("FIRMA: DEBUG (Android Debug)")
    else:
        cns = re.findall(rb"CN=([^\x00-\x08\x0a-\x1f]+)", cert)
        if cns:
            print(f"FIRMA: {cns[0].decode(errors='ignore')}")
        else:
            print("FIRMA: Desconocida")
else:
    print("FIRMA: No se encontró CERT.RSA")

# Check if android:debuggable is in manifest
if "AndroidManifest.xml" in z.namelist():
    data = z.read("AndroidManifest.xml")
    if b"debuggable" in data:
        print("AndroidManifest: contiene 'debuggable'")
    else:
        print("AndroidManifest: sin 'debuggable'")

z.close()
print(f"Tamaño: {os.path.getsize(apk)/1024/1024:.1f} MB")
