def singleItem(r1, r2):
    r1['value'] = r2['value']
    r1['minValue'] = 0
    r1['maxValue'] = 0
    lis = r2['value'].split('/')
    for i in range(len(lis)):
        r1['area'+str(i+1)] = lis[i]
    return r1


def multipleItems(r1, r2):
    r1['minValue'] = 0
    r1['maxValue'] = 0
    for item in r2['fieldItems']:
        if item['isSelected'] == 1:
            content = item['content']
    for item in r1['fieldItems']:
        if item['content'] == content:
            value = item['itemWid']
            item['isSelected'] = 1
            r1['fieldItems'] = []
            r1['fieldItems'].append(item)
        else:
            value = item['itemWid']
            item['isSelected'] = 1
            r1['fieldItems'] = []
            r1['fieldItems'].append(item)
    r1['value'] = value
    return r1


def fillForm(r1, r2):
    form = []
    for index in range(len(r1)):
        if r1[index]['fieldItems']:
            item = multipleItems(r1[index], r2[index])
            form.append(item)
        else:
            item = singleItem(r1[index], r2[index])
            form.append(item)
    return form
