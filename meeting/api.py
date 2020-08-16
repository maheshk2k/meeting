from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import add_days, nowdate

@frappe.whitelist()
def send_invitation_emails(meeting):
    meeting = frappe.get_doc("Meeting", meeting)
    meeting.check_permission("email")
    print("Meeting status before is ", meeting.status)

    if meeting.status == "Planned":
        frappe.sendmail(
            recipients=[d.attendee for d in meeting.attendees],
            sender=frappe.session.user,
            subject=meeting.title,
            message=meeting.invitation_message,
            reference_doctype=meeting.doctype,
            reference_name=meeting.name
        )
        meeting.status = "Invitation Sent"
        print("Meeting status after is ", meeting.status)
        meeting.save()

        frappe.msgprint(_("Invitation Sent"))
    else:
        frappe.msgprint(_("Meeting status must be 'planned'"))

@frappe.whitelist()
def get_meetings(start, end):
    if not frappe.has_permission("Meeting", "read"):
        raise frappe.PermissionError
    
    # return frappe.db.sql("""select timestamp(`date`, from_time) as start, timestamp(`date`, to_time) as end, name, title, status from `tabMeeting` where `date` between %(start)s and %(end)s""", {"start": start,"end": end}, as_dict=True)
    
    return frappe.db.sql("""select timestamp(`date`, from_time) as start, timestamp(`date`, to_time) as end, name, title, status, 0 as all_day from `tabMeeting` where date between %(start)s and %(end)s""",{"start": start, "end": end}, as_dict=True)

def make_orientation_meeting(doc, method):
    # """Create an orientation meeting when new user is added """
    meeting = frappe.get_doc({
        "doctype": "Meeting",
        "title": "Orientation for {0}".format(doc.first_name),
        "date": add_days(nowdate(), 1),
        "from_time": "09:00",
        "to_time": "09:30",
        "status": "Planned",
        "attendees": [{
            "attendee": doc.name
        }]
    })
    # System manager may not permission to create a meeting 
    meeting.flags.ignore_permissions = True
    meeting.insert()
    frappe.msgprint(_("Orientation meeting created"))