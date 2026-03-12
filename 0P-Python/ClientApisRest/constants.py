
url_base:str = 'https://jsonplaceholder.typicode.com/posts/{}'
URLS:list = [url_base.format(post) for post in range(1, 100)]
URLS.append('https://not-found-url/1')
URLS.append('http://not-found-url/2')
#URLS.append(float(1))
