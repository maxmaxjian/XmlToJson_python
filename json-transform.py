import json
import os
import collections


directory = "/Users/wejian/devel/homework/src/ClockFaceSelectorLibrary/src/main/res/raw/"


def main():
    raw_files = os.listdir(directory)
    for raw_file in raw_files:
        if raw_file.startswith("clock_face") and "stellar" in raw_file:
            file_path = directory + raw_file
            process_file(file_path)


def process_file(file_name):
    # Load file into dict
    with open(file_name, "r") as file_handle:
        blob = get_json_as_dict(file_handle)

    if blob["type"] != "ClockFace":
        raise Exception("Not a clock face file")

    if "complication_bar" not in blob:
        print "skipping " + file_name + " because we already did that one"
        return

    old_layers = get_layers(blob)
    date_window_layers = get_date_window_layers(blob)
    complications_layers = get_complications_layers(blob)
    tick_marks, face_layers = split_tick_marks(old_layers)

    final_layers = []
    final_layers += tick_marks
    final_layers += [tag_layer(l, "DATE_WINDOW") for l in date_window_layers]
    final_layers += complications_layers
    final_layers += face_layers

    new_blob = {"type": "ClockFace",
                "id": blob["id"],
                "layers": final_layers}

    sorted_blob = sort_dict(new_blob)

    print json.dumps(sorted_blob, indent=4)
    with open(file_name, "w") as file_handle:
        json.dump(new_blob, file_handle, indent=4)


def get_json_as_dict(file_handle):
    blob = json.load(file_handle)
    return blob


def get_layers(face_blob):
    return face_blob["layers"]


def get_date_window_layers(face_blob):
    if "date_window" in face_blob:
        return face_blob["date_window"]
    else:
        return []


def get_complications_layers(face_blob):
    return [face_blob["complication_alert"], face_blob["complication_bar"]]


def split_tick_marks(layer_list):
    pivot = 0
    for i, entry in enumerate(layer_list):
        if layer_list[i]["type"] != "ImageLayer":
            pivot = i
            break
    return layer_list[:pivot], layer_list[pivot:]


def tag_layer(layer, tag):
    layer["layer_properties"] = [tag]
    return layer


def sort_dict(node):
    if isinstance(node, list):
        return [sort_dict(x) for x in node]

    if not isinstance(node, dict):
        return node

    if "type" not in node:
        raise Exception("Missing type")

    key_ordering = get_key_ordering(node["type"])
    ordered_dict = collections.OrderedDict()
    sorted_keys = sorted(node, key=lambda k: key_ordering.index(k) if k in key_ordering else len(key_ordering) + 1)
    for key in sorted_keys:
        ordered_dict[key] = sort_dict(node[key])
    return ordered_dict


def get_key_ordering(type_name):
    if "Layer" in type_name:
        return ["type",
                "layout_id",
                "src",
                "mask",
                "day_src",
                "night_src",
                "day_tint",
                "night_tint",
                "day_opacity",
                "night_opacity",
                "center_x",
                "center_y",
                "bottom_y",
                "position",
                "hand_rotation",
                "tick_ms",
                "layer_properties"]

    if type_name == "ClockFace":
        return ["type",
                "id",
                "layers"]
    else:
        return []


if __name__ == "__main__":
    main()
