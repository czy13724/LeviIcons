import os
import json

def generate_json():
    image_folder = 'leviicons'
    json_data = {
        "name": "Levi图标订阅",
        "description": "收集一些自己常用的图标,欢迎大家引用,如您有新的软件图标可以在issue中说明.",
        "icons": []
    }

    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            raw_url = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/main/{image_path}"
            icon_data = {"name": filename, "url": raw_url}
            json_data["icons"].append(icon_data)

    # Set the output path relative to the repository root
    output_path = os.path.join(os.getcwd(), 'levi.icons.json')

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    # Save output data to the GITHUB_STATE environment file
    with open(os.environ['GITHUB_STATE'], 'a') as state_file:
        state_file.write(f"ICONS_JSON_PATH={output_path}\n")

if __name__ == "__main__":
    generate_json()
