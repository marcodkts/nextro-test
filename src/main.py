import json
import re


def getJson(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as json_file:
        content = json_file.read()

    return json.loads(content)


def saveJson(dict: dict, file_name: str):
    with open(f"./output/{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(dict, json_file, ensure_ascii=False, indent=2)


def getInfo(value: tuple, fk_file) -> dict:
    data_list = getJson(f"./assets/{fk_file}.json")
    data = [data for data in data_list if data[value[0]] == value[1]]
    return data


consumer_units = getJson("./assets/consumer_units.json")
contacts = getJson("./assets/contacts.json")

for unit in consumer_units:
    project_fk = unit["project_id"]
    contacts_fk = unit["contact_id"]
    adress_info = unit["address"].split(", ")

    if len(adress_info) == 4:
        zipcode = "-".join(re.findall("\d+", adress_info[3].split(" / ")[0]))
        unit["address_info"] = {
            "street": adress_info[0],
            "number": adress_info[1],
            "neighborhood": adress_info[2],
            "zipcode": zipcode,
            "city": adress_info[3].split(" / ")[0].replace(zipcode+" ", ""),
            "state": adress_info[3].split(" / ")[1]
        }
    else: 
        print(adress_info[2])
        zipcode = "-".join(re.findall("\d+", adress_info[2].split(" / ")[0]))
        unit["address_info"] = {
            "street": adress_info[0],
            "neighborhood": adress_info[1],
            "zipcode": zipcode,
            "city": adress_info[2].split(" / ")[0].replace(zipcode+" ", ""),
            "state": adress_info[2].split(" / ")[1]
        }

    unit["contact"] = [contact for contact in contacts if contact["id"] == contacts_fk][0]
    unit["consumption"] = getInfo(
        ("consumer_unit_id", unit["id"]), "consumption_history"
    )

    projects = getInfo(("id", project_fk), "projects")
    if projects:
        project = projects[0]
        project_contact = [
            contact for contact in contacts if contact["id"] == project["contact_id"]
        ]
        if project_contact:
            project["contact"] = project_contact[0]
        unit["project"] = project

saveJson(consumer_units, "consumer_units")
