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

#
#
def anywhere_server(self, settings):
	ar.publish(self, settings.listing)

	m = self.select(ar.Published, ar.NotPublished, ar.Stop)
	if isinstance(m, ar.NotPublished):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	while True:
		m = self.select(ar.Enquiry, ar.Delivered, ar.Dropped, ar.Cleared, ar.Stop)
		if isinstance(m, ar.Enquiry):
			pass
		elif isinstance(m, ar.Delivered):
			self.console(f'Delivered to "{m.matched_name}"')	# Acquired a subscriber.
			continue
		elif isinstance(m, (ar.Cleared, ar.Dropped)):			# Lost a subscriber.
			self.console(f'Cleared/Dropped "{m.matched_name}"')
			continue
		else:
			return ar.Aborted()		# Control-c.

		# Respond to enquiry.
		self.reply(ar.Ack())

ar.bind(anywhere_server)

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
	ar.create_node(anywhere_server, factory_settings=factory_settings)
