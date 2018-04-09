import pickle
import sys
from walmart_crawler import ProductRecord
reload(sys)
sys.setdefaultencoding('utf8')

properties = [
                ('Brand', 'Brand Name','Manufacturer'),
                ('Model','Manufacturer Part Number', 'manufacturer_part_number', 'Item model number','Series'),
                ]
def main(brand):
    filename = 'data/' + brand + '_products.p'
    data = pickle.load(open(filename,'rb'))

    # Properties that all products will have. Each word in each tuple refers to the same real world entity as the rest of the words in the tuple.

    for item in data:
        new = {}
        used = []
        for key in sorted(item.properties.keys()):
            v, prop = key_in_props(key)
            # If the property has not been seen yet and is a property in properties
            if v >= 0 and v not in used:
                new[prop.lower()] = ''.join([c for c in list(item.properties[key].replace(',','').replace('\\','').replace('\n','').replace('"', '')) if ord(c) < 128])
                if new[prop.lower()] == '-' or new[prop.lower()] == 'N/A' or new[prop.lower()] == 'Missing':
                    new[prop.lower()] = ''
                used.append(v)

        # Add empty values for properties not seen.

        # Overwrite properties
        item.properties = new
    
    pickle.dump(data, open(filename,'wb'))
    count = 0
    # Write csv
    with open('data/'+brand+'_products.csv', 'w') as f:
        keys = ','.join(sorted(data[0].properties.keys()))
        print 'id,product title,' + keys + ',combo'
        f.write('id,product title,' + keys + ',combo' + '\n')
        for item in data:
            values = ','.join([item.properties[key] for key in sorted(item.properties.keys())])
            pid = str(brand[0]) + str(count)
            try:
                if item.price == '-' or item.price == 'N/A' or item.price == 'Missing':
                        item.price = ''
                if brand == 'amazon':
                    if item.title[0] == '-' or item.title[0] == 'N/A' or item.title[0] == 'Missing':
                        item.title[0] = ''
                    item_string = str(item.title[0]).replace(',' , '').replace('\\','').replace('\n','').replace('"', '') + ',' + values
                    item_string += ',' + item_string.replace(',',' ')
                    item_string = str(pid) + ','  + item_string
                    item_string = item_string.replace('  ', ' ').lower().replace('  ', ' ')
                    f.write(item_string)
                else:
                    if item.title == '-' or item.title == 'N/A' or item.title == 'Missing':
                        item.title = ''
                    item_string = str(item.title).replace(',' , '').replace('\\','').replace('\n','').replace('"', '') + ',' + values
                    item_string += ',' + item_string.replace(',',' ')
                    item_string = str(pid) + ','  + item_string
                    item_string = item_string.replace('  ', ' ').lower().replace('  ', ' ')
                    f.write(item_string)
                f.write('\n')
                count += 1
            except Exception as e:
                pass


    # for item in data:
    #     for prop in properties:
    #         found = []
    #         if type(prop) is tuple:
    #             for prop_variation in prop:
    #                 prop_variation = prop_variation.lower()
    #                 for key in item.properties.keys():
    #                     key = key.strip()
    #                     if prop_variation in key.lower() and abs(len(prop_variation)-len(key)) <= 2:
    #                         # print(prop_variation, item.properties[key], 'tup')
    #                         found.append((prop_variation,item.properties[key]))
    #         if len(found) > 1:
    #             print(found)
    #             print(item.properties)
    #         elif type(prop) is str:
    #             prop = prop.lower()
    #             for key in item.properties.keys():
    #                 key = key.strip()
    #                 if prop in key.lower() and abs(len(prop)-len(key)) <= 2:
    #                     print(prop, item.properties[key], 'str')
    #     print(item.properties)
    #     print()
    
    # q = 'Computer Memory Type'
    # for item in data:
    #     try:
    #         for key in item.properties.keys():
    #             if q.lower() in key.lower() and abs(len(q) - len(key)) <= 10:
    #                 print(key)
    #                 print(item.properties[key])
    #     except:
    #         pass


    # props = []
    # for item in data:
    #     for key in item.properties.keys():
    #         if key not in props:
    #             props.append(key)

    # for p in sorted(props):
    #     print(p)

# Determines if the key is in properties, and if so, the index.
def key_in_props(key):
    key = key.lower()
    for i, prop_list in enumerate(properties):
        if type(prop_list) is tuple:
            for prop in prop_list:
                prop = prop.lower()
                if (key in prop or prop in key) and abs(len(prop)-len(key)) <= 2:
                    return i, prop_list[0]
        elif type(prop_list) is str:
            prop = prop_list.lower()
            if (key in prop or prop in key) and abs(len(prop)-len(key)) <= 2:
                    return i, prop
    return -1, None

if __name__ == '__main__':
    main('amazon')
    main('walmart')
