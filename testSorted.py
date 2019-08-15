from collections import OrderedDict
import json

# allsites = [
#     {
#         'A5': 'G1',
#         'A10': 'G1',
#         'site': 'example1.com',
#         'A1': 'G1'
#     }
#     # },
#     # {
#     #     'A5': 'R',
#     #     'A10': 'Y',
#     #     'site': 'example2.com',
#     #     'A1': 'G'
#     # }
# ]
#
# sort_order = ['site', 'A1', 'A5', 'A10']
# # print sort_order.index('site')
# # print sort_order.index('A5')
# # for item in allsites:
# #     for (k, v) in item.iteritems():
# #         print k, v
# allsites_ordered = [OrderedDict(sorted(item.iteritems(), key=lambda (k, v): sort_order.index(k))) for item in allsites]
# print json.dumps(allsites_ordered, indent=4)

# unsortedarr = ['1', '2', '3']
# sort_order = ['2', '1', '3']
# sortedarr = sorted(unsortedarr, key=lambda k : sort_order.index(k))
# print sorted

unsorted = [{
    'A5': 'G1',
    'A10': 'G1',
    'site': 'example1.com',
    'A1': 'G1'
}]
sort_order = ['site', 'A1', 'A5', 'A10']
# sortedarr = [OrderedDict(sorted(item.iteritems(), key=lambda (k,v): sort_order.index(k))) for item in unsorted]
aftersorted = []
for item in unsorted:
    print item
    aftersorted.append(OrderedDict(sorted(item.iteritems(), key=lambda (k,v): sort_order.index(k))))
    print json.dumps(aftersorted, indent=4)
# print json.dumps(sortedarr, indent=2)

before = unsorted[0]
print json.dumps(before, indent=4)
after = OrderedDict(sorted(before.iteritems(), key=lambda (k,v): sort_order.index(k)))
print json.dumps(after,  indent=4)

