import os

BASE_DIR = "./microservices_code"

for service in os.listdir(BASE_DIR):
    service_dir = os.path.join(BASE_DIR, service)
    for root, _, files in os.walk(service_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    lines = f.readlines()
                # Remove Markdown lines
                clean_lines = [l for l in lines if not ("**" in l or l.lstrip().startswith("1."))]
                text = "".join(clean_lines)
                # Add missing imports
                if "Optional" in text and "from typing import Optional" not in text:
                    text = "from typing import Optional\n" + text
                if "BaseModel" in text and "from pydantic import BaseModel" not in text:
                    text = "from pydantic import BaseModel\n" + text
                with open(path, "w") as f:
                    f.write(text)