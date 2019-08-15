import xml.etree.ElementTree as ElementTree
import copy
import json
import os
from collections import OrderedDict

class xmlConverter:

    def __init__(self, xmlfile, jsonfile):
        self.xmlfile = xmlfile
        self.jsonfile = jsonfile
        self.items = []

    def parseXML(self):
        xmlfilename = self.xmlfile[self.xmlfile.rfind('/')+1:self.xmlfile.find('.xml')]
        tree = ElementTree.parse(self.xmlfile)
        root = tree.getroot()
        for elem in root.findall('item'):
            bitmap = elem.find('bitmap')
            data = copy.deepcopy(bitmap.attrib)
            keys = data.keys()
            for key in keys:
                value = data.get(key)
                value_mod = value[value.find('/')+1:]
                data[key[key.find('}')+1:]] = value_mod if value_mod != 'true' and value_mod != 'false' else json.loads(value_mod)
                del data[key]
            sort_order = ['src', 'gravity','antialias','tint']
            sorted_data = OrderedDict(sorted(data.iteritems(), key=lambda (k,v): sort_order.index(k)))
            id = xmlfilename+'_'+data['src']
            item = {'id': id, 'item': sorted_data}
            self.items.append(item)

            # data = [data]
            # sort_order = ['src', 'gravity', 'antialias', 'tint']
            # ordered_data = [OrderedDict(sorted(item.iteritems(), key=lambda (k,v): sort_order.index(k))) for item in data]
            # id = xmlfilename+'_'+data[0]['src']
            # item = {'id' : id, 'item' : ordered_data[0]}
            # self.items.append(item)

        sort_order = ['id', 'item']
        ordered_item = [OrderedDict(sorted(item.iteritems(), key=lambda (k,v): sort_order.index(k))) for item in self.items]
        print json.dumps(ordered_item, indent=4)
        self.items = ordered_item

    def writeToJSON(self):
        with open(self.jsonfile, 'w') as f:
            json.dump(self.items, f, indent=4)


def main():
    # path = '/Users/wejian/devel/homework/src/ClockFaceSelectorLibrary/src/main/res/drawable/'
    # # path = 'venv/'
    # filenames = os.listdir(path)
    # for xmlfile in filenames:
    #     if xmlfile.startswith('hand_') and xmlfile.endswith('.xml'):
    #         jsonfile = xmlfile[0:xmlfile.find('.xml')]+'.json'
    #         converter = xmlConverter(path+xmlfile, jsonfile)
    #         converter.parseXML()
    #         converter.writeToJSON()

    path = '/Users/wejian/devel/homework/src/ClockFaceSelectorLibrary/src/rook/res/drawable/'
    xmlfile = 'hand_kaleidoscope_wheel.xml'
    jsonfile = xmlfile[0:xmlfile.find('.xml')] + '.json'
    converter = xmlConverter(path+xmlfile, jsonfile)
    converter.parseXML()
    converter.writeToJSON()


if __name__ == '__main__':
    main()
