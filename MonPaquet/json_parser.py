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
        new_gpio.pin = int(gpio[3].text)
        my_gpios[new_gpio.nom] = new_gpio


def write_json(Cgpio_list, encode = False):
    dp = ": "
    vg = ", "
    q = '"'
    json_string = "{"
    for (clef,valeur) in Cgpio_list.items():
        json_string += q + clef + q + dp + q + valeur.value + q + vg
    json_string = json_string[0:-2]
    json_string += "}"

    if encode :
        return json_string.encode('utf8')
    else :
        return json_string


def read_json(json_string, Cgpio_list):
    parsed_json = json.loads(json_string)
    #for gpio in Cgpio_list:
        #gpio.setValue(parsed_json[gpio.nom])
    for key in Cgpio_list:
        Cgpio_list[key].setValue(parsed_json[key])


if __name__ == '__main__':
    my_gpios = dict()

    ch = "nom : %s    valeur : %s"

    readconfig(my_gpios, "../gpio_def.xml")
    print("------- 1 --------")



    for clef in my_gpios.keys():
        print(clef + " vaut " + my_gpios[clef].value)

    my_gpios["LED4"].setValue("On")

    print("------- 1.5 --------")

    for clef in my_gpios.keys():
        print(clef + " vaut " + my_gpios[clef].value)

    print("------- 2 --------")

    json_final = write_json(my_gpios)
    print(json_final)

    print("------- 3 --------")

    my_gpios2 = dict()
    readconfig(my_gpios2, "../gpio_def_test.xml")
    json_str_2 = write_json(my_gpios2)
    print(json_str_2)

    print("------- 4 --------")

    read_json(json_str_2, my_gpios)

    """for i in my_gpios:
        ch2 = ch % (i.nom, i.value)
        print(ch2)"""

    for clef in my_gpios.keys():
        print(clef + " vaut " + my_gpios[clef].value)
