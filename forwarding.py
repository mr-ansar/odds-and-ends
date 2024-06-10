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

def job_processor(self, **kw):
	while True:
		m = self.select(ar.Enquiry, ar.Stop)
		if isinstance(m, ar.Enquiry):		# Request
			self.reply(ar.Ack())
		else:
			return ar.Aborted()

ar.bind(job_processor)

def job_done(self):
	while True:
		m = self.select(ar.Ack, ar.Stop)
		if isinstance(m, ar.Stop):
			return ar.Aborted()
		self.console(f'Done')

ar.bind(job_done)

#
#
def main(self):
	j = self.create(job_processor)
	d = self.create(job_done)

	self.send(ar.Enquiry(), j)
	m = self.select(ar.Ack, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	self.forward(ar.Enquiry(), j, d)

	self.send(ar.Enquiry(), j)
	m = self.select(ar.Ack, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()

	return None

ar.bind(main)

if __name__ == '__main__':
	ar.create_object(main)
