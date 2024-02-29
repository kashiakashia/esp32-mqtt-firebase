import ujson
# ---------------- data methods -----------------------------------

def create_json_data(temp, humidity):
    data = ujson.dumps({
        "temp": temp,
        "humidity": humidity,
    })
    
    return data