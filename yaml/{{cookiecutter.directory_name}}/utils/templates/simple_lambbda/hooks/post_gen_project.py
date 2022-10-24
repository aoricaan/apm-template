import json
import os
from pathlib import Path

configuration_path = Path(os.getcwd()).joinpath("configuration.json")
configuration = json.loads(configuration_path.read_text())
configuration["cfn"]["Properties"]["MemorySize"] = int(configuration["cfn"]["Properties"]["MemorySize"])
configuration["cfn"]["Properties"]["Timeout"] = int(configuration["cfn"]["Properties"]["MemorySize"])
configuration_path.write_text(json.dumps(configuration, indent=2))

