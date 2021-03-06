#!/usr/bin/env python3

# The arrow library is used to handle datetimes
from arrow import get
# The request library is used to fetch content through HTTP
from requests import Session
from reescraper import (ElHierro, GranCanaria, Gomera, LanzaroteFuerteventura,
                        LaPalma, Tenerife)
from parsers.lib.exceptions import ParserException


def fetch_island_data(country_code, session):
    if country_code == 'ES-CN-FVLZ':
        lanzarote_fuerteventura_data = LanzaroteFuerteventura(session).get_all()
        if not lanzarote_fuerteventura_data:
            raise ParserException(country_code, "LanzaroteFuerteventura not response")
        else:
            return lanzarote_fuerteventura_data
    elif country_code == 'ES-CN-GC':
        gran_canaria_data = GranCanaria(session).get_all()
        if not gran_canaria_data:
            raise ParserException(country_code, "GranCanaria not response")
        else:
            return gran_canaria_data
    elif country_code == 'ES-CN-IG':
        gomera_data = Gomera(session).get_all()
        if not gomera_data:
            raise ParserException(country_code, "Gomera not response")
        else:
            return gomera_data
    elif country_code == 'ES-CN-LP':
        la_palma_data = LaPalma(session).get_all()
        if not la_palma_data:
            raise ParserException(country_code, "LaPalma not response")
        else:
            return la_palma_data
    elif country_code == 'ES-CN-TE':
        tenerife_data = Tenerife(session).get_all()
        if not tenerife_data:
            raise ParserException(country_code, "Tenerife not response")
        else:
            return tenerife_data
    elif country_code == 'ES-CN-HI':
        el_hierro_data = ElHierro(session).get_all()
        if not el_hierro_data:
            raise ParserException(country_code, "ElHierro not response")
        else:
            return el_hierro_data
    else:
        raise ParserException(country_code, 'Can\'t read this country code {0}'.format(country_code))


def fetch_consumption(country_code='ES-CN', session=None):
    ses = session or Session()
    island_data = fetch_island_data(country_code, ses)
    data = []
    for response in island_data:
        response_data = {
            'countryCode': country_code,
            'datetime': get(response.timestamp).datetime,
            'consumption': response.demand,
            'source': 'demanda.ree.es'
        }

        data.append(response_data)

    return data


def fetch_production(country_code, session=None):
    ses = session or Session()
    island_data = fetch_island_data(country_code, ses)
    data = []

    if country_code == 'ES-CN-HI':
        for response in island_data:
            if response.production() > 0:
                response_data = {
                    'countryCode': country_code,
                    'datetime': get(response.timestamp).datetime,
                    'production': {
                        'coal': 0.0,
                        'gas': round(response.gas + response.combined, 2),
                        'solar': round(response.solar, 2),
                        'oil': round(response.vapor + response.diesel, 2),
                        'wind': round(response.wind, 2),
                        'hydro': 0.0,
                        'biomass': 0.0,
                        'nuclear': 0.0,
                        'geothermal': 0.0
                    },
                    'storage': {
                        'hydro': round(-response.hydraulic, 2),
                        'battery': 0.0
                    },
                    'source': 'demanda.ree.es',
                }
                data.append(response_data)
    else:
        for response in island_data:
            if response.production() > 0:
                response_data = {
                    'countryCode': country_code,
                    'datetime': get(response.timestamp).datetime,
                    'production': {
                        'coal': 0.0,
                        'gas': round(response.gas + response.combined, 2),
                        'solar': round(response.solar, 2),
                        'oil': round(response.vapor + response.diesel, 2),
                        'wind': round(response.wind, 2),
                        'hydro': round(response.hydraulic, 2),
                        'biomass': 0.0,
                        'nuclear': 0.0,
                        'geothermal': 0.0
                    },
                    'storage': {
                        'hydro': 0.0,
                        'battery': 0.0
                    },
                    'source': 'demanda.ree.es',
                }
                data.append(response_data)

    return data


if __name__ == '__main__':
    session = Session
    print("# ES-CN-FVLZ")
    print(fetch_consumption('ES-CN-FVLZ', session))
    print(fetch_production('ES-CN-FVLZ', session))
    print("# ES-CN-GC")
    print(fetch_consumption('ES-CN-GC', session))
    print(fetch_production('ES-CN-GC', session))
    print("# ES-CN-IG")
    print(fetch_consumption('ES-CN-IG', session))
    print(fetch_production('ES-CN-IG', session))
    print("# ES-CN-LP")
    print(fetch_consumption('ES-CN-LP', session))
    print(fetch_production('ES-CN-LP', session))
    print("# ES-CN-TE")
    print(fetch_consumption('ES-CN-TE', session))
    print(fetch_production('ES-CN-TE', session))
    print("# ES-CN-HI")
    print(fetch_consumption('ES-CN-HI', session))
    print(fetch_production('ES-CN-HI', session))
