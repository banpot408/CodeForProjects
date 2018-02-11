auto_operations.hotwork_warning_2.criterion = "permit_type = 'ID1515991393312977874132' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND valid_plus_1_email_status = 'Not Sent' AND (valid_end_plus_1 <= ${current_time})"
auto_operations.hotwork_warning_2.operations = "record.send_hotwork_warning(sa_session,2)"
auto_operations.hotwork_warning_2.time_cached = True
auto_operations.hotwork_warning_2.schedule.hour = "*"
auto_operations.hotwork_warning_2.schedule.minute = "*"
auto_operations.coldwork_warning_2.criterion = "permit_type = 'ID1515991347662001866770' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND valid_plus_1_email_status = 'Not Sent' AND (valid_end_plus_1 <= ${current_time})"
auto_operations.coldwork_warning_2.operations = "record.send_coldwork_warning(sa_session,2)"
auto_operations.coldwork_warning_2.time_cached = True
auto_operations.coldwork_warning_2.schedule.hour = "*"
auto_operations.coldwork_warning_2.schedule.minute = "*"