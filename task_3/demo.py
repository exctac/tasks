from task_3.exchange_rate_parser import ExchangeRate, CacheClient


def run():

    exchange_rate_1 = ExchangeRate(cache_client=CacheClient)

    print(exchange_rate_1.all())
    print(exchange_rate_1.get([840, 'EUR']))
    print(exchange_rate_1.convert(100, codes=(840, 'EUR')))

    exchange_rate_2 = ExchangeRate(cache_client=CacheClient, set_ex=60)

    print(exchange_rate_2.all())
    print(exchange_rate_2.get([840, 'EUR']))
    print(exchange_rate_2.convert(100, codes=(840, 'EUR')))

    exchange_rate_3 = ExchangeRate(allow_cache=False)

    print(exchange_rate_3.all())
    print(exchange_rate_3.get([840, 'EUR']))
    print(exchange_rate_3.convert(100, codes=(840, 'EUR')))

    exchange_rate_4 = ExchangeRate(cache_client=CacheClient)

    print(exchange_rate_4.get([840, 'EUR', 'OTHER']))
    print(exchange_rate_4.convert(100, codes=(840, 'EUR', 'OTHER')))


if __name__ == '__main__':
    run()
