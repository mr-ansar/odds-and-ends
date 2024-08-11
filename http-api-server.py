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
'''An HTTP server that supports an Enquiry-Ack exchange with clients.

.
'''
import ansar.connect as ar

THIS_API = [
	ar.Enquiry,
	ar.ApiHttpRequest,
]

def http_server(self):
	ar.listen(self, ar.HostPort('127.0.0.1', 5080), api_server=THIS_API)
	m = self.select(ar.Listening, ar.NotListening, ar.Stop)
	if isinstance(m, ar.Listening):			# Good to go.
		pass
	elif isinstance(m, ar.NotListening):	# Cant setup a server.
		return m
	else:
		return ar.Aborted()		# Control-c.

	while True:
		m = self.select(ar.Accepted, ar.Closed, ar.Abandoned, ar.Stop, ar.Enquiry, ar.ApiHttpRequest)
		if isinstance(m, ar.Accepted):					# Added a client.
			continue
		elif isinstance(m, (ar.Closed, ar.Abandoned)):	# Lost a client.
			continue
		elif isinstance(m, ar.Stop):		# Control-c.
			return ar.Aborted()
		
		# Received an Enquiry as an HTTP request.
		self.reply(ar.Ack())

ar.bind(http_server)

if __name__ == '__main__':
	ar.create_object(http_server)
