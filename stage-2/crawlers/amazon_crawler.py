import sys
import eventlet
import settings
from helpers import make_request, log, format_url
from extractors import get_title, get_url, get_price, get_primary_img
from collections import deque
from datetime import datetime
import pickle

crawl_time = datetime.now()
queue = deque()
product_list = []
product_dict = {}
product_urls = []
class ProductRecord(object):
    def __init__(self, title, product_url, price, properties):
        super(ProductRecord, self).__init__()
        self.title = title
        self.product_url = product_url
        self.price = price
        self.properties = properties

    def pretty_print(self):
        return self.title  + ":" +  str(self.price) + ":" +str(self.properties.keys())

    def save(self):
        product_list.append(self)

def enqueue_url(url):
    queue.append(url)

def dequeue_url():
    return queue.popleft() 

def begin_crawl():
    visited = {}
    w = open(settings.a_URL_file, 'w')
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blank and commented out lines
            page, html = make_request(line)
            url = line
            count = 0
            while page != None and count <= 3500:
                items = page.findAll("li", "s-result-item")
                log("Found {} items on {}".format(len(items), url))
                for item in items[:settings.max_details_per_listing]:
                    product_image = get_primary_img(item)
                    if not product_image:
                        log("No product image detected, skipping")
                        continue
                    product_title = get_title(item)
                    product_url = get_url(item)
                    product_price = get_price(item)
                    if product_url not in visited:
                        count += 1
                        print product_url, product_price, product_title
                        visited[product_url] = True # mark that we've seen it
                        # need to add host to url
                        product_url = format_url(product_url)
                        w.write('%s\n' % product_url)
                        product_dict[product_url] = (product_title, product_price)
                        print count, product_url, product_dict[product_url]

                next_link = page.find("a", id="pagnNextLink")
                if next_link:
                    log(" Found 'Next' link on {}: {}".format(url, next_link["href"]))
                    page, html = make_request(next_link["href"])
                    url = next_link["href"]
    w.close()
    pickle.dump(product_dict, open("products.p", "wb" ))

def gather_urls(start, end):
    with open(settings.a_URL_file, 'r') as w:
        urls = (w.readlines()[start:end])
    i = start
    for url in urls:
        url = url.strip()
        product_urls.append(url)
        i += 1
    log('Total number of product URLs enqueued: %d' % len(urls))

def print_product(index):
	file = '%s%d.p' % (settings.a_products_path, index)
	with open(file, 'rb') as f:
		product = pickle.load(f)

	print product.title
	print product.price
	print product.properties

def fetch_listing(start, end):
	global crawl_time
	with open('amazon-products.p', 'rb') as pf:
		product_dict = pickle.load(pf)
	index = start-1
	count = 0
	for product_url in product_urls:
		#print product_url
		index += 1
		page1, html1 = make_request(product_url)
		try:
		# visit the page specified by product_url
			temp_dict = {}
			product_title = product_dict[product_url]
			product_price = page1.find("span", "a-size-medium a-color-price").get_text().strip()

			#extract product info from comparison_table
			table = page1.find("table", "a-bordered a-horizontal-stripes a-spacing-mini a-size-base comparison_table")
			for i in table.findAll("tr"):
				if "a-span3 comparison_attribute_name_column comparison_table_first_col" in str(i):
					k = i.find("td").find("span").get_text()
					v = i.find("th").find("span").get_text()
					temp_dict[v] = k

			#extract product info from product details Table
			tables = page1.findAll("table", "a-keyvalue prodDetTable")
			for table2 in tables:
				for i in table2.findAll("tr"):
					k = i.find("td").get_text().strip()
					v = i.find("th").get_text().strip()
					temp_dict[v] = k

			product = ProductRecord(
			title=product_title,
			product_url=format_url(product_url),
			price=product_price,
			properties=temp_dict
			)
			product_name = settings.a_products_path +  str(index) + ".p"
			pickle.dump(product, open(product_name, 'wb'))
			#print_product(index)
			count += 1
			print (count, index, product_price)
		except Exception as e:
			print "Exception##:" +str(index) + '\t' + str(e)
        
        
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "crawl":
    	log("Seeding the URL frontier with subcategory URLs")
        begin_crawl()  # put a bunch of subcategory URLs into the queue

        #log("Seeding the URL frontier with subcategory URLs")
        #session = dryscrape.Session()
        #begin_crawl(session)  # put a bunch of subcategory URLs into the queue

        #log('Dumping all URLs to file: %s' % settings.w_URL_file)
        #dump_urls()
    elif len(sys.argv) > 1 and sys.argv[1] == "start":
        gather_urls(int(sys.argv[2]), int(sys.argv[3]))
        log("Beginning crawl at {}".format(crawl_time))
        fetch_listing(int(sys.argv[2]), int(sys.argv[3]))
        #[pile.spawn(fetch_listing) for _ in range(settings.max_threads)]
        #pool.waitall()
        #print_product(int(sys.argv[2])) # test print of first product
    else:
        print "Usage: python walmart_crawler.py start"
