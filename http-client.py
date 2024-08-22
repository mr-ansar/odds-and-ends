# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2024 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''Complete an HTTP request-response sequence.

.
'''
import ansar.connect as ar
import api

def http_client(self):
	ar.connect(self, ar.HostPort('127.0.0.1', 5080), api_client='/')
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):			# Good to go.
		pass
	elif isinstance(m, ar.NotConnected):	# Cant setup a transport.
		return m
	else:
		return ar.Aborted()		# Control-c.

	self.send(ar.Enquiry(), self.return_address)
	self.send(api.MixedBag(number=10), self.return_address)
	self.send(api.MixedBag(number=10, ratio=0.125), self.return_address)
	self.send(api.MixedBag(number=10.5, ratio=0.125), self.return_address)
	self.send(ar.HttpRequest(method='GET', request_uri='/Enquiry'), self.return_address)

	value = ar.Ack()
	m = self.select(ar.Ack, ar.HttpResponse, ar.Closed, ar.Abandoned, ar.Faulted, ar.Stop)
	if isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost transport.
		return m
	elif isinstance(m, ar.HttpResponse) and m.status_code == 400:
		value = m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()		# Control-c.
	
	m = self.select(ar.Ack, ar.HttpResponse, ar.Closed, ar.Abandoned, ar.Faulted, ar.Stop)
	if isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost transport.
		return m
	elif isinstance(m, ar.HttpResponse) and m.status_code == 400:
		value = m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()		# Control-c.
	
	m = self.select(ar.Ack, ar.HttpResponse, ar.Closed, ar.Abandoned, ar.Faulted, ar.Stop)
	if isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost transport.
		return m
	elif isinstance(m, ar.HttpResponse) and m.status_code == 400:
		value = m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()		# Control-c.
	
	m = self.select(ar.Ack, ar.HttpResponse, ar.Closed, ar.Abandoned, ar.Faulted, ar.Stop)
	if isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost transport.
		return m
	elif isinstance(m, ar.HttpResponse) and m.status_code == 400:
		value = m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()		# Control-c.
	
	m = self.select(ar.Ack, ar.HttpResponse, ar.Closed, ar.Abandoned, ar.Faulted, ar.Stop)
	if isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost transport.
		return m
	elif isinstance(m, ar.HttpResponse) and m.status_code == 400:
		value = m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()		# Control-c.

	return value

ar.bind(http_client)

if __name__ == '__main__':
	ar.create_object(http_client)
