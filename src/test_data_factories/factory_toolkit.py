import functools
from copy import deepcopy


class FactoryToolkit:

    @staticmethod
    def deep_merge(target: dict, override: dict) -> dict:
        copy_override = deepcopy(override)

        for key, value in target.items():
            if isinstance(value, dict) and isinstance(copy_override.get(key), dict):
                FactoryToolkit.deep_merge(value, copy_override.setdefault(key, {}))
            else:
                target[key] = copy_override.get(key) if copy_override.get(key) is not None else target[key]

        additional_override_keys = list(set(copy_override.keys()) - set(target.keys()))

        for add_key in additional_override_keys:
            target[add_key] = copy_override[add_key]

        return target

    @staticmethod
    def obj_none_to_empty_dict(factory_build_function):
        @functools.wraps(factory_build_function)
        def wrap(factory, obj=None):
            if obj is None:
                obj = {}

            result = factory_build_function(factory, obj)

            return result

        return wrap
