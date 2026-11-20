import ajustes as aj

def evaluar_estado(variable, valor, umbrales):
    if variable == "temp":
        if valor > aj.CRIT_TEMP:
            return "crit"
        if valor > umbrales["temp_max"]:
            return "aviso"
        return "ok"

    if variable == "hum_suelo":
        if valor < aj.CRIT_SUELO:
            return "crit"
        if valor < umbrales["suelo_min"]:
            return "aviso"
        return "ok"

    if variable == "luz":
        if valor < umbrales["luz_min"]:
            return "aviso"
        return "ok"

    # humedad del aire
    if valor < 25 or valor > 90:
        return "crit"
    if valor < 40 or valor > 80:
        return "aviso"
    return "ok"