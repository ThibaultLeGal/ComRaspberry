import simplejson as json
import xml.etree.ElementTree as xml_tree
from MonPaquet import Cgpio


def readconfig(my_gpios, xml_file):
    tree = xml_tree.parse(xml_file)
    root = tree.getroot()
    for gpio in root:
        l_range = gpio[1].text.split(";")

        new_gpio = Cgpio.Cgpio()
        new_gpio.nom = gpio[0].text
        new_gpio.range = l_range
        new_gpio.setValue(gpio[2].text)
        my_gpios.append(new_gpio)


def write_json(Cgpio_list):
    dp = ": "
    vg = ", "
    q = '"'
    json_string = "{"
    for gpio in Cgpio_list:
        json_string += q + gpio.nom + q + dp + q + gpio.value + q + vg
    json_string = json_string[0:-2]
    json_string += "}"
    return json_string


def read_json(json_string, Cgpio_list):
    parsed_json = json.loads(json_string)
    for gpio in Cgpio_list:
        gpio.setValue(parsed_json[gpio.nom])


if __name__ == '__main__':
    my_gpios = []

    ch = "nom : %s    valeur : %s"

    readconfig(my_gpios, "gpio_def.xml")
    print("------- 1 --------")

    for i in my_gpios:
        ch2 = ch % (i.nom, i.value)
        print(ch2)

    print("------- 2 --------")

    json_final = write_json(my_gpios)
    print(json_final)

    print("------- 3 --------")

    my_gpios2 = []
    readconfig(my_gpios2, "gpio_def_test.xml")
    json_str_2 = write_json(my_gpios2)
    print(json_str_2)

    print("------- 4 --------")

    read_json(json_str_2, my_gpios)

    for i in my_gpios:
        ch2 = ch % (i.nom, i.value)
        print(ch2)
