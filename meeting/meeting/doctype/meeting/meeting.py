# -*- coding: utf-8 -*-
# Copyright (c) 2020, Pais and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class Meeting(Document):
	def validate(self):
# 		Set missing names and warn if duplicates
		found = []
		for attendee in self.attendees:
			if not attendee.full_name:
				attendee.full_name = get_full_name(attendee.attendee)
			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} entered twice").format(attendee.attendee))

			found.append(attendee.attendee)
# Whitelist method so as to make it accessible from web.
@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	# Concatnates by space if it has value
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))
