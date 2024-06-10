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
def client(self, settings):
	ar.connect(self, settings.connecting_ipp)

	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.NotConnected):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	front_end = self.return_address

	self.send(ar.Enquiry(), front_end)
	m = self.select(ar.Ack,			# A response.
		ar.Abandoned, ar.Closed,	# Lost connection.
		ar.Stop)					# Control-c.
	if isinstance(m, (ar.Abandoned, ar.Closed)):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	
	return m

ar.bind(client)

# Configuration for this executable.
class Settings(object):
	def __init__(self, connecting_ipp=None):
		self.connecting_ipp = connecting_ipp or ar.HostPort()

SETTINGS_SCHEMA = {
	'connecting_ipp': ar.UserDefined(ar.HostPort),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(connecting_ipp=ar.HostPort('127.0.0.1', 30122))

if __name__ == '__main__':
	ar.create_object(client, factory_settings=factory_settings)
