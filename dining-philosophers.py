# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
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

class INITIAL: pass
class READY: pass
class WAITING: pass
class EATING: pass
class THINKING: pass

# The shared resource.
class Fork(object):
	def __init__(self):
		pass

ar.bind(Fork)

# Resource at rest.
class Holder(ar.Point, ar.StateMachine):
	def __init__(self):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.fork = None
		self.enquired = ar.deque()

def Holder_INITIAL_Start(self, message):
	# Start with the fork down.
	self.fork = Fork()
	return READY

def Holder_READY_Enquiry(self, message):
	# Someone is hungry. Add them to the tail of the queue.
	self.enquired.append(self.return_address)
	if self.fork:
		a = self.enquired.popleft()		# Waiting the longest.
		self.send(self.fork, a)
		self.fork = None
	return READY

def Holder_READY_Fork(self, message):
	# Fork is being returned. Is someone waiting?
	if self.enquired:
		a = self.enquired.popleft()
		self.send(message, a)
		return READY
	self.fork = message
	return READY

HOLDER_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	READY: (
		(Fork, ar.Enquiry), ()
	),
}

ar.bind(Holder, HOLDER_DISPATCH)

#
#
class Philosopher(ar.Threaded, ar.StateMachine):
	def __init__(self, name, left_holder, right_holder):
		ar.Threaded.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.name = name
		self.left_holder = left_holder
		self.right_holder = right_holder
		# Start with no forks.
		self.holding = ar.deque()
		self.retry = None
		self.mark = None

	def next(self):
		# Introduce variation in eating/thinking times.
		if self.retry is None:
			intervals = ar.RetryIntervals(regular_steps=2.0, randomized=0.25, truncated=0.5)
			self.retry = ar.smart_intervals(intervals)
		p = next(self.retry)
		return p

def Philosopher_INITIAL_Start(self, message):
	# Hungry. Wait for both forks.
	self.send(ar.Enquiry(), self.left_holder)
	self.send(ar.Enquiry(), self.right_holder)
	self.mark = ar.clock_now()
	self.console(f'"{self.name}" is WAITING')
	return WAITING

def Philosopher_WAITING_Fork(self, message):
	# A fork has been relinquished. Got a pair?
	self.holding.append(message)
	if len(self.holding) == 2:
		span = ar.clock_now() - self.mark
		d = ar.span_to_text(span)
		self.console(f'"{self.name}" is EATING (waited {d})')
		self.start(ar.T1, self.next())
		return EATING
	return WAITING

def Philosopher_EATING_T1(self, message):
	# Enough for a while. Put forks down.
	self.send(self.holding.pop(), self.left_holder)
	self.send(self.holding.pop(), self.right_holder)
	self.start(ar.T2, self.next())
	self.console(f'"{self.name}" is THINKING')
	return THINKING

def Philosopher_THINKING_T2(self, message):
	# Hungry again.
	self.send(ar.Enquiry(), self.left_holder)
	self.send(ar.Enquiry(), self.right_holder)
	self.mark = ar.clock_now()
	self.console(f'"{self.name}" is WAITING')
	return WAITING

PHILOSOPHER_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	WAITING: (
		(Fork,), ()
	),
	EATING: (
		(ar.T1,), ()
	),
	THINKING: (
		(ar.T2,), ()
	),
}

ar.bind(Philosopher, PHILOSOPHER_DISPATCH)

#
#
philosopher = [
	"Socrates",
	"Descartes",
	"Aristotle",
	"Nietzsche",
	"Sartre",
	"Amdahl",
	"Seneca",
	"Epicurus",
	"Aurelius",
	"Confucius",
	"Dante",
	"Pascale",
	"Voltaire",
	"Schopenhauer",
]

def main(self):
	# Set the table. One holder/fork between each
	# seated philosopher.
	holder = [self.create(Holder) for p in philosopher]

	# Seat the 1st, 3rd, ... etc.
	i = 0
	left_holder = holder[-1]				# Wrap back to the last holder/fork.
	for h, p in zip(holder, philosopher):
		if i % 2 == 0:
			a = self.create(Philosopher, p, left_holder, h)
		left_holder = h
		i += 1

	# Seat the 2nd, 4th, ... etc.
	i = 0
	left_holder = holder[-1]
	for h, p in zip(holder, philosopher):
		if i % 2 == 1:
			a = self.create(Philosopher, p, left_holder, h)
		left_holder = h
		i += 1

	# Wait for control-c.
	self.select(ar.Stop)

ar.bind(main)

#
#
if __name__ == '__main__':
	ar.create_object(main)
