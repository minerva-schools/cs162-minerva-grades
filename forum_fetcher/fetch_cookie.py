import browser_cookie3

def cookie_fetcher():
    cookies = browser_cookie3.chrome(domain_name='.forum.minerva.kgi.edu')
    return cookies

if __name__ == '__main__':
    cookie_fetcher()