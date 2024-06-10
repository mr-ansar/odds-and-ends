# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2024 Scott Woods
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
import ansar.connect as ar

#
#
def front_end(self, settings):
	ar.listen(self, settings.listening_ipp)

	m = self.select(ar.Listening, ar.NotListening, ar.Stop)
	if isinstance(m, ar.NotListening):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	ar.connect(self, settings.connecting_ipp)

	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.NotConnected):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	db = self.return_address

	while True:
		m = self.select(ar.Enquiry,		# A request.
			ar.Accepted,				# New connection.
			ar.Abandoned, ar.Closed,	# Lost existing connection.
			ar.Stop)					# Control-c.
		if isinstance(m, ar.Accepted):
			continue
		elif isinstance(m, (ar.Abandoned, ar.Closed)):
			if self.return_address == db:
				return m
			continue
		elif isinstance(m, ar.Stop):
			return ar.Aborted()

		self.forward(m, db, self.return_address)

ar.bind(front_end)

# Configuration for this executable.
class Settings(object):
	def __init__(self, listening_ipp=None, connecting_ipp=None):
		self.listening_ipp = listening_ipp or ar.HostPort()
		self.connecting_ipp = connecting_ipp or ar.HostPort()

SETTINGS_SCHEMA = {
	'listening_ipp': ar.UserDefined(ar.HostPort),
	'connecting_ipp': ar.UserDefined(ar.HostPort),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(listening_ipp=ar.HostPort('127.0.0.1', 30122),
	connecting_ipp=ar.HostPort('127.0.0.1', 30121))

if __name__ == '__main__':
	ar.create_object(front_end, factory_settings=factory_settings)
