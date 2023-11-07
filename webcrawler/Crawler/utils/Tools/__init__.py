def getFirstOne(value, default):
    return next(iter(value), default)

def getJsonValueFromPath(jObj, path, defaultValue):
    try:
        for k in path.split('/'):
            jObj = jObj.get(k, {})
    except Exception as e:
        return defaultValue
    return defaultValue if (jObj == {} or jObj is None) else jObj