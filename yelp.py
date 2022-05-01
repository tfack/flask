import requests
def find_coffee():
	api_key = 'pMWcYDMpXkTeeyWIb7AtpzRbcJ2PKRvHIzT7p0QAukPFge4IGKectozkpQBkZnTBKE9g3FwC7Os68MmQKgAwwucLgeMo0oMgagYENkYs-9TZKKJ8HXXMmwM1ZAaBYHYx'
	headers = {'Authorization': 'Bearer {}'.format(api_key)}
	search_api_url = 'https://api.yelp.com/v3/businesses/search'
	params = {'term': 'coffee shop', 
	          'location': 'Seattle, Washington',
	          'limit': 50}
	response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
	data=response.json()
	sortedbyRating=sorted(data["businesses"], key=lambda i: i['rating'], reverse=True)
	return sortedbyRating
