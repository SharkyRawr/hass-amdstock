import logging, sys, json

from bs4 import BeautifulSoup
import httpx

#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

HEADERS = {
    'authority': 'www.amd.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'referer': 'https://www.amd.com/de/direct-buy',
    'accept-language': 'de',
    'dnt': '1'
}

async def check_stock():
    result = {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get('https://www.amd.com/de/direct-buy/products/de', headers=HEADERS)
        if r.status_code >= 400:
            print('error:', str(r.error))

        response_body = r.content
        #print(response_body, file=sys.stderr)
        soup = BeautifulSoup(response_body, 'html.parser')

        container = soup.select('.direct-buy')
        
        for c in container:
            title = str(c.select('.shop-title')[0].contents[0])
            title = title.strip()

            #if '6800' not in title: continue

            price = str(c.select('.shop-price')[0].contents[0])
            price = price.strip()

            shop_link = c.select('.shop-links')[0] 
            
            stock = ""
            if link := shop_link.find('button'):
                stock = 'https://amd.com' + link.get('href')
            else:
                stock = str(shop_link.contents[0])
            stock = stock.strip()

            result[title] = {
                #'title': title,
                'price': price,
                'stock': stock,
            }

    return result




if __name__ == '__main__':
    import asyncio
    task = check_stock()
    res = asyncio.get_event_loop().run_until_complete( task )
    print(json.dumps(res))