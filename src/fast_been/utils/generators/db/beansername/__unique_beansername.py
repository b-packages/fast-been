from fast_been.utils.generators.random import number_string


def unique_beanser_name(beanser_name: str) -> str:
    return beanser_name + '_' + number_string(6)
