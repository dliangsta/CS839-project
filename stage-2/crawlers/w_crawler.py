import sys
import eventlet
import w_settings as settings
from w_helpers import make_request, log, format_url
from extractors import get_title, get_url, get_price, get_primary_img
from collections import deque
from datetime import datetime
import pickle

crawl_time = datetime.now()
pool = eventlet.GreenPool(settings.max_threads)
pile = eventlet.GreenPile(pool)
queue = deque()
product_list = []

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
        print str(len(product_list)+1) + "\t" + self.pretty_print()
        product_list.append(self)
        if (len(product_list) >= settings.total_crawl):
            pickle.dump(product_list, open("products.p", "wb" ))
            sys.exit(0)

def enqueue_url(url):
    queue.append(url)

def dequeue_url():
    return queue.popleft() 

def begin_crawl():
    # explode out all of our category `start_urls` into subcategories
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blank and commented out lines
            url = line
            page, html = make_request(line)
            count = 0

            i = 1 # starting page
            while page != None:
                print 'page %d of link: %s' %(i, line)
                # look for products listed on this page
                results = page.findAll('div', 'search-result-gridview-item clearfix')  # items in gridview

                for result in results:
                    link = result.find('a')
                    if not link:
                        continue
                    link = link['href']
                    count += 1
                    enqueue_url(link)
                
                i += 1
                # go to list of pages at bottom    
                p_list = page.find('ul', 'paginator-list').findAll('li')
                for p in p_list:
                    # search for 'next' ordinal page
                    if not p.has_attr('class') and str(i) in p.find('a').text:
                        next_page = '?page=%d#searchProductResult' % i # href is wrong because it is dynamically generated
                        url = line + next_page
                        page, html = make_request(url)
                        break
                    else:
                        page = None

            log("Found {} results on {}".format(count, line))

def fetch_listing():
    global crawl_time
    url = dequeue_url()
    if not url:
        log("WARNING: No URLs found in the queue. Retrying...")
        pile.spawn(fetch_listing)
        return

    page, html = make_request(url)
    if not page:
        return

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
        try:
            # visit the page specified by product_url
            page1, html1 = make_request(product_url)
            temp_dict = {}

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
            product.save()
        except Exception as e:
            print e

        # download_image(product_image, product_id)

    # add next page to queue
    next_link = page.find("a", id="pagnNextLink")
    if next_link:
        log(" Found 'Next' link on {}: {}".format(url, next_link["href"]))
        enqueue_url(next_link["href"])
        pile.spawn(fetch_listing)

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "start":
        log("Seeding the URL frontier with subcategory URLs")
        begin_crawl()  # put a bunch of subcategory URLs into the queue

        log("Beginning crawl at {}".format(crawl_time))
        [pile.spawn(fetch_listing) for _ in range(settings.max_threads)]
        pool.waitall()
    else:
        print "Usage: python w_crawler.py start"
