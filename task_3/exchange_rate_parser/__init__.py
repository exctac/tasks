"""
Задание 3

Для иностранных клиентов требуется корректировать стоимость продукта (базовая цена в рублях) в зависимости
от курса валют на текущий момент времени. По адресу http://www.cbr.ru/scripts/XML_daily.asp находятся
актуальные данные ЦБ РФ о курсах валют. Необходимо получить данные по соответствующему url и извлечь
курсы доллара и евро по отношению к рублю. Для идентификации валюты использовать символьные коды (USD, EUR) или
цифровые коды (840, 978).

Также необходимо предусмотреть кэширование выходных данных, чтобы при многократном обращении за курсом валют,
реальный запрос по url делался только с определенной частотой.
Кэш должен быть реализован с помощью паттерна делегирования, чтобы сторонний разработчик мог использовать
свою реализацию кэша, ничего не меняя в вашем коде.
Напиши свой базовый вариант кэша для данной задачи, который будет кэшировать данные на заданный интервал времени.

Формат выходных данных:

{
    'USD': Decimal(59.51),
    'EUR': Decimal(63.45)
}
"""

import datetime
import xml.etree.ElementTree as ET
from collections import OrderedDict
from decimal import Decimal
from urllib.request import urlopen


__all__ = (
    'ExchangeRate',
    'CacheClientBase',
    'CacheClient',
)


class CacheClientBase:

    def __init__(self, *args, **kwargs):
        super(CacheClientBase, self).__init__()

        self.args = args
        self.kwargs = kwargs

    def set(self, *args):
        raise NotImplementedError(f'Define method `set` in { self.__class__.__name__ }.')

    def get(self):
        raise NotImplementedError(f'Define method `get` in { self.__class__.__name__ }.')


class CacheClient(CacheClientBase):
    _cache_data = None
    _cache_created_at = None

    cache_expire = 360

    def __init__(self, *args, **kwargs):
        super(CacheClient, self).__init__(*args, **kwargs)

        self.cache_expire = self.kwargs.get('set_ex', self.cache_expire)

    def set(self, data):
        self._cache_data = data
        self._cache_created_at = datetime.datetime.now()

    def get(self):
        if self._cache_data is not None:
            interval_td = datetime.datetime.now() - self._cache_created_at

            if interval_td.seconds > self.cache_expire:
                self.clear_cache()

        return self._cache_data

    def clear_cache(self):
        self._cache_data = None
        self._cache_created_at = None


class ExchangeRate:
    _target_url = "http://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, allow_cache=True, cache_client=None, *args, **kwargs):
        assert isinstance(allow_cache, bool), "`allow_cache` an bool value is expected."
        assert not allow_cache or cache_client, "`cache_client` is not defined."

        if allow_cache:
            self.cache_client = cache_client(*args, *kwargs)

        self.allow_cache = allow_cache

    def _build_initial_data(self):
        response = urlopen(self._target_url)

        xml_tree = ET.parse(response)
        root = xml_tree.getroot()

        data = OrderedDict()
        for child in root.findall("Valute"):
            nominal = int(child.find("Nominal").text)

            value = child.find("Value").text.replace(',', '.')
            value = Decimal(value) / nominal

            data[child.find("NumCode").text, child.find("CharCode").text] = round(value, 2)

        return data

    @property
    def _initial_data(self):
        if self.allow_cache:
            initial_data = self.cache_client.get()

            if not initial_data:
                initial_data = self._build_initial_data()
                self.cache_client.set(initial_data)

            return initial_data

        return self._build_initial_data()

    def _extract(self, codes=None):
        codes_ = [] if codes is None else codes

        if not isinstance(codes_, (list, tuple, set)):
            raise ValueError('`codes` must be `list`, `tuple` or `set`.')

        codes_ = {str(code) for code in codes_}

        def exp(*args):
            if not codes_:
                return True

            args = set(args)
            match = bool(codes_ & args)

            if match:
                codes_.difference(args)

            return match

        return OrderedDict([
            (code_char, value)
            for (_, code_char), value in self._initial_data.items()
            if exp(_, code_char)
        ])

    def get(self, codes):
        return self._extract(codes)

    def all(self):
        return self._extract()

    def convert(self, value, codes):
        value = Decimal(value)

        exchange_rates = self._extract(codes)
        for code, rate_value in exchange_rates.items():
            exchange_rates[code] = round(value * rate_value, 2)

        return exchange_rates
