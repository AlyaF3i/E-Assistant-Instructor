from pathlib import Path
from collections import defaultdict

def get_txt_mapping():
    main_path = Path("educational_resources")
    output = defaultdict(list)
    for path in main_path.rglob("*.txt"):
        class_level = path.parent.name
        subject = path.name.replace(".txt", "")
        output[class_level].append(subject)
    return dict(output)