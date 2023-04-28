from json import loads, dumps, load
from urllib import urlencode
from geventhttpclient import HTTPClient, URL, httplib
httplib.patch()
from ADL.Utilities import *

def _jsonlist(list):
	return loads(list) if not isList(list) else list[:]


def _request(url, method='GET', query={}, body={}, headers={}, asjson=False):
	print 'Logic.library.Internet._request:', url, method, query, body, headers
	
	if not query: query = {};
	if not body: body = {};
	if not headers: headers = {};

	def _remove_empty_params(params):
		if not isDict(params): params = loads(params);
		return dict([(k,v) for k,v in params.items() if v is not None])

	query = _remove_empty_params(query)
	print 'Logic.library.Internet._request.query:', query

	headers = _remove_empty_params(headers)
	print 'Logic.library.Internet._request.headers:', headers

	body_str = urlencode(_remove_empty_params(body))
	print 'Logic.library.Internet._request.body_str:', body_str

	http_url = URL(url)
	for k,v in query.items(): http_url[k] = v;
	print 'Logic.library.Internet._request.http_url:', http_url

	http = HTTPClient.from_url(http_url, connection_timeout=1000, network_timeout=1000)
	print 'Logic.library.Internet._request -> calling'
	print 'Logic.library.Internet._request.http:', http
	response = http.request(method, http_url.request_uri, body=body_str, headers=headers)
	print 'Logic.library.Internet._request.response.dir:', dir(response)
	print 'Logic.library.Internet._request.response.headers:', response.headers
	
	headers = dict(response.headers)
	if 'content-type' in headers and headers['content-type'] == 'application/json' and not asjson:
		try:
			body = load(response)
		except:
			body = response.read()
	else:
		body = response.read()
	
	return {
		'headers' : headers,
		'body' : body,
		'status' : response.status_code
	}

functions = {
	"http" : {
		"get" : lambda url, query={}, headers={}: _request(url, 'GET', query, headers=headers),
		"post" : lambda url, query={}, body={}, headers={}: _request(url, 'POST', query, body, headers),
		"put" : lambda url, query={}, body={}, headers={}: _request(url, 'PUT', query, body, headers),
		"delete" : lambda url, query={}, body={}, headers={}: _request(url, 'DELETE', query, body, headers)
	},
	'headers' : lambda headers={}: headers
}

# resp = functions['http']['get']('http://httpbin.org/get')
# print 'GET:', dumps(resp)
# 
# resp = functions['http']['put'](**{
# 	"url": "http://httpbin.org/put",
# 	"query": {"qsvar":"qsval"},
# 	"body": {"hello":"world"},
# 	"headers": {"graphheader":"hi"}
# })
# print 'PUT:', dumps(resp)
# 
# resp = functions['http']['post'](**{
# 	"url": "http://httpbin.org/post",
# 	"query": {"qsvar":"qsval"},
# 	"body": {"hello":"world"},
# 	"headers": {"graphheader":"hi"}
# })
# print 'POST:', dumps(resp)
# 
# resp = functions['http']['delete'](**{
# 	"url": "http://httpbin.org/delete",
# 	"query": {"qsvar":"qsval"},
# 	"body": {"hello":"world"},
# 	"headers": {"graphheader":"hi"}
# })
# print 'DEL:', dumps(resp)
