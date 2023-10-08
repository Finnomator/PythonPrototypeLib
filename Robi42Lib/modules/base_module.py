from ..hardware_manager import manager as hw_manager
from ..hardware_manager import platform_description as pltfm_desc

# redefine for easy access the Hardware
DigitalBoardPin = pltfm_desc.DigitalBoardPin
DigitalBoardPins = pltfm_desc.DigitalBoardPins
AnalogBoardPin = pltfm_desc.AnalogBoardPin
AnalogBoardPins = pltfm_desc.AnalogBoardPins


def needs_i2c_hardware(driver_name):
    def function_wrapper(func):
        manager_instance = hw_manager.HardwareManager.get_instance()

        def inner_wrap(*args, **kwargs):
            driver = manager_instance.get_i2c_driver_by_name(driver_name)
            func(*args, **kwargs, **{driver_name: driver})

        return inner_wrap

    return function_wrapper


def get_first_i2c_hardware(driver_name, ignore_if_not_present=True):
    def function_wrapper(func):
        manager_instance = hw_manager.HardwareManager.get_instance()

        def inner_wrap(*args, **kwargs):
            drivers = manager_instance.get_i2c_driver_by_name(driver_name)
            if len(drivers) > 0:
                return func(*args, **kwargs, **{driver_name: drivers[0]})

            if not ignore_if_not_present:
                raise RuntimeError('Hardware for driver \'{}\' not registered!'.format(driver_name))

        return inner_wrap

    return function_wrapper


class BaseModule:
    ...
