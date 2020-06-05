from dataclasses import InitVar, dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

import iso6346


@dataclass
class ShippingContainer:
    owner_code: str
    length_ft: float
    contents: Optional[Union[List[Any], str]]
    HEIGHT_FT: ClassVar[float] = 8.5
    WIDTH_FT: ClassVar[float] = 8.0
    next_serial: ClassVar[int] = 1337
    args: Optional[Tuple[Any]] = field(init=False, repr=False)
    kwargs: Optional[Dict[str, Any]] = field(init=False, repr=False)

    def __post_init__(self):
        self.bic = self._make_bic_code(
            owner_code=self.owner_code, serial=ShippingContainer._get_next_serial(),
        )

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(owner_code=owner_code, serial=str(serial).zfill(6))

    @classmethod
    def _get_next_serial(cls):
        result = cls.next_serial
        cls.next_serial += 1
        return result

    @classmethod
    def create_empty(cls, owner_code, length_ft, *args, **kwargs):
        return cls(owner_code, length_ft, contents=None, *args, **kwargs)

    @classmethod
    def create_with_items(cls, owner_code, length_ft, items, *args, **kwargs):
        return cls(owner_code, length_ft, contents=list(items), *args, **kwargs)

    def _calc_volume(self):
        return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT * self.length_ft

    @property
    def volume_ft3(self):
        return self._calc_volume()


@dataclass
class RefrigeratedShippingContainer(ShippingContainer):
    celsius: float
    _celsius: float = field(init=False, repr=False)
    MAX_CELSIUS: ClassVar[float] = 4.0
    FRIDGE_VOLUME_FT3: ClassVar[float] = 100

    @staticmethod
    def _make_bic_code(owner_code: str, serial: int) -> str:
        return iso6346.create(
            owner_code=owner_code, serial=str(serial).zfill(6), category="R",
        )

    @staticmethod
    def _c_to_f(celsius) -> float:
        return celsius * 9 / 5 + 32

    @staticmethod
    def _f_to_c(fahrenheit) -> float:
        return (fahrenheit - 32) * 5 / 9

    @property
    def celsius(self) -> float:
        return self._celsius

    def _set_celsius(self, value: float) -> None:
        try:
            if value > RefrigeratedShippingContainer.MAX_CELSIUS:
                raise ValueError("Temperature too hot!")
        except TypeError:
            raise TypeError(
                "__init__() missing 1 required positional argumentL 'celsius'"
            )
        self._celsius = float(value)

    @celsius.setter
    def celsius(self, value: float) -> None:
        self._set_celsius(value)

    @property
    def fahrenheit(self) -> float:
        return RefrigeratedShippingContainer._c_to_f(self.celsius)

    @fahrenheit.setter
    def fahrenheit(self, value) -> None:
        self.celsius = RefrigeratedShippingContainer._f_to_c(value)

    def _calc_volume(self):
        return super()._calc_volume() - RefrigeratedShippingContainer.FRIDGE_VOLUME_FT3


@dataclass
class HeatedRefrigeratedShippingContainer(RefrigeratedShippingContainer):
    MIN_CELSIUS: ClassVar[float] = -20.0

    def _set_celsius(self, value: float) -> None:
        try:
            if value < HeatedRefrigeratedShippingContainer.MIN_CELSIUS:
                raise ValueError("Temperature too cold!")
            super()._set_celsius(value)
        except TypeError:
            raise TypeError(
                f"TypeError: __init__() missing 1 required keyword argument: {'celsius'}"
            )
