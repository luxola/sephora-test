from pptree import *

class Execution:

    def __init__(self, tablename, function, head=None):
        self.tablename = tablename
        self.function = function
        self.team = []
        if head:
            head.team.append(self)

    def __str__(self):
        return self.function

master_string = ''
master_table_list = []
dependency_list = []

inventory_items = 'SELECT sku_id, inventory_count FROM \'raw.inventory_items\''
item_purchase_prices = 'SELECT l.sku_id AS sku_id, i.batch_id, ARRAY_AGG(STRUCT(i.purchase_price, i.currency)) AS purchase_prices FROM \'raw.purchase_line_items\' l INNER JOIN \'raw.purchase_items\' i ON l.batch_purchase_id = i.batch_id GROUP BY 1, 2'
product_categories = 'SELECT p.id As productId, ARRAY_AGG(STRUCT(c.category_name AS categoryName)) AS categories FROM \'raw.products\' p LEFT JOIN \'raw.categories\' c ON  p.category_id = c.id GROUP BY 1'
product_images = 'SELECT pr.id As productId, ARRAY_AGG(p.url) AS urls FROM \'raw.products\' pr LEFT JOIN \'raw.pictures\' p ON (p.id, \'product\') = (p.external_id, p.type) GROUP BY 1'
products = 'SELECT p.id As productId, i.urls AS urls, c.categories AS categories FROM \'raw.products\' p LEFT JOIN \'tmp.product_images\' i ON p.id = i.productId LEFT JOIN \'tmp.product_categories\' c ON p.id = c.productId'
variant_images = 'SELECT v.id AS sku_id, ARRAY_AGG(p.url) AS urls FROM \'raw.variants\' v LEFT JOIN \'raw.pictures\' p ON (v.id, \'variant\') = (p.external_id, p.type) GROUP BY 1'
variants = 'SELECT f.product_id AS productId v.id AS skuId, p.purchase_prices AS purchasePrices, i.urls AS urls, inv.inventory_count AS inventoryCount FROM \'raw.variants\' v LEFT JOIN \'tmp.item_purchase_prices\' p LEFT JOIN \'tmp.variant_images\' i LEFT JOIN \'tmp.inventory_items\' inv'

def find_nth(s, substr, n):
    i = 0
    n = n-1
    while n >= 0:
        n -= 1
        i = s.find(substr, i + 1)
    return i

def find_dependancy(name, query):
    global  master_string 
    table_array = []
    vars()[name] = ''

    master_table_list.append(name)

    table_name = query[query.find('FROM'):len(query)]
    table_name = table_name[table_name.find('\'')+1:find_nth(table_name,'\'',2)]
   
    table_array.append(table_name)
    master_table_list.append(table_name)

    i = len(query)
    j = 1

    while i > 0:
        if find_nth(query, 'JOIN', j) > 0:
            table_name = query[find_nth(query, 'JOIN', j):len(query)]
            table_name = table_name[table_name.find('\'')+1:find_nth(table_name,'\'',2)]
            table_array.append(table_name)
            master_table_list.append(table_name)

        j = j+1
        i = find_nth(query,'JOIN',j)

    i = 1

    for x in table_array:
        if len(table_array) == 1:
            master_string = master_string + name + ' is dependent on ' + x + ' \n'
            vars()[name] = vars()[name] + name + ' is dependent on ' + x + ' \n' 
        elif i == 1:
            master_string = master_string + name + ' is dependent on ' + x 
            vars()[name] = vars()[name] + name + ' is dependent on ' + x 
        elif i != len(table_array):
            master_string = master_string + ' and ' + x
            vars()[name] = vars()[name] + ' and ' + x
        else:
             master_string = master_string + ' and ' + x + ' \n'
             vars()[name] = vars()[name] + ' and ' + x + ' \n'

        i += 1     

    dependency_list.append(vars()[name])


find_dependancy('tmp.inventory_items', inventory_items)    
find_dependancy('tmp.item_purchase_prices', item_purchase_prices)    
find_dependancy('tmp.product_categories', product_categories)
find_dependancy('tmp.product_images', product_images)
find_dependancy('tmp.products', products)
find_dependancy('tmp.variant_images', variant_images)
find_dependancy('tmp.variants', variants)

master_table_list = list(set(master_table_list))

for x in master_table_list:
    vars()[x] = Execution(x, "TOP")

for x in master_table_list:
    for y in dependency_list:
        if y.find(x + ' is dependent on ') >= 0:
            vars()[x] = Execution(x, "CHILD", vars()[y[y.find(' is dependent on ') + 17:y.find(' ', y.find(' is dependent on ') + 17)]])
                        
            i = len(y)
            j = 1
            
            while i > 0:
                if find_nth(y, ' and ', j) >= 0:
                    vars()[x] = Execution(x, "CHILD", vars()[y[y.find(' and ') + 5:y.find(' ', y.find(' and ') + 5)]])
                    
                j = j+1
                i = find_nth(y ,' and ',j)

print('\n')
top = 1
for x in master_table_list:
    for y in dependency_list:
        if y.find(x + ' is dependent on ') >= 0:
            top = 0
    if top == 1:
        print_tree(vars()[x],  "team", "tablename")
        print('\n')
    top = 1 
