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
'''.

.
'''
import ansar.connect as ar

# The subscriber object.
def anywhere_client(self, settings):
	ar.subscribe(self, settings.listing)

	m = self.select(ar.Subscribed, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	m = self.select(ar.Available, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()
	server_address = self.return_address

	while True:
		self.send(ar.Enquiry(), server_address)
		t = ar.clock_now()
		r = self.select(ar.Ack, ar.Cleared, ar.Dropped, ar.Stop, seconds=3.0)
		if isinstance(r, ar.Ack):
			pass
		elif isinstance(r, (ar.Cleared, ar.Dropped)):
			return r
		elif isinstance(r, ar.Stop):
			return ar.Aborted()
		elif isinstance(r, ar.SelectTimer):
			return ar.TimedOut(r)
		
		d = ar.clock_now() - t
		s = ar.span_to_text(d)

		self.console(f'Acked after {s}')

ar.bind(anywhere_client)

# Configuration for this executable.
class Settings(object):
	def __init__(self, listing=None):
		self.listing = listing

SETTINGS_SCHEMA = {
	'listing': ar.Unicode(),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(listing='enquiry-from-anywhere')

if __name__ == '__main__':
	ar.create_node(anywhere_client, factory_settings=factory_settings)
