MODEL_VERSION='rules-v1'

def predict(payload):
    try:
        pressure=float(payload['pressure_bar'])
        flow=float(payload['flow_lpm'])
        temp=float(payload['temperature_c'])
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError('pressure_bar, flow_lpm and temperature_c must be numeric') from exc
    if not (0<=pressure<=20 and 0<=flow<=1000 and -40<=temp<=120):
        raise ValueError('sensor readings out of range')
    reasons=[]
    if pressure<2.5:
        reasons.append('low_pressure')
    if flow<65:
        reasons.append('low_flow')
    if temp>90:
        reasons.append('high_temperature')
    return {'model_version':MODEL_VERSION,'anomaly':bool(reasons),'reasons':reasons}
