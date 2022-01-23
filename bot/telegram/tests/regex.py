import re as regex

tests = [
    '/subscription  "Proceso de Titulación primavera 2021":"Fechas o Hitos"',
    '/subscription "Proceso de Titulación primavera 2021":"Novedades"',
    '/subscription "Practicas Prueba 2022":"Fechas o Hitos"']

re_c = regex.compile(r'\/subscription\s')
re_create = regex.compile(r'\/subscription\s\".*\":\".*\"')
re_create_divider = regex.compile(r':')


if __name__ == '__main__':
    for t in tests:
        match = re_create.match(t)
        print(match)
        _, value = re_c.split(t)
        value = value.replace('"', "")
        instance, target = re_create_divider.split(value)
        print(instance, target)