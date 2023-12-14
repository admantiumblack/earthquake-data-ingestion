from process.steps import pipeline_step


@pipeline_step
def reformat_earthquake(data):
    res = []
    for i in data.copy():
        earthquake_properties = i["properties"]
        earthquake_location = i["geometry"]
        earthquake_properties["longitude"] = earthquake_location[0]
        earthquake_properties["latitude"] = earthquake_location[1]
        earthquake_properties["depth"] = earthquake_location[2]
        res.append(earthquake_properties)
    return res
