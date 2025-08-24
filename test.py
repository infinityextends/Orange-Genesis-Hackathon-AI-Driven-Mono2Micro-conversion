import zipfile

with zipfile.ZipFile("microservices_code.zip", 'r') as zip_ref:
    zip_ref.extractall("./microservices_code")