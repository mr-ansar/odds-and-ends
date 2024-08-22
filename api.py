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
'''.'''
import ansar.connect as ar

__all__ = [
	'MixedBag',
	'DoesNotWork',
]

class MixedBag(object):
	def __init__(self, number=0, ratio=None, world=None, span=None, guid=None):
		self.number = number
		self.ratio = ratio
		self.world = world
		self.span = span
		self.guid = guid

MIXED_BAG_SCHEMA = {
	'number': ar.Integer8(),
	'ratio': ar.Float8(),
	'world': ar.WorldTime(),
	'span': ar.TimeSpan(),
	'guid': ar.UUID(),
}

class DoesNotWork(object):
	def __init__(self, can_do_this=None, cant_do_this=None):
		self.can_do_this = can_do_this
		self.cant_do_this = cant_do_this or {}

DOES_NOT_WORK_SCHEMA = {
	'can_do_this': ar.Unicode(),
	'cant_do_this': ar.MapOf(ar.Unicode(), ar.ArrayOf(ar.Float8(), 32)),
}

ar.bind(MixedBag, object_schema=MIXED_BAG_SCHEMA)
ar.bind(DoesNotWork, object_schema=DOES_NOT_WORK_SCHEMA)
