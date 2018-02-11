auto_operations.scaffolding_warning_1.criterion = "certificate_type = 'ID1515991410643754960468' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND valid_minus_1_email_status = 'Not Sent' AND (valid_end_minus_1 <= ${current_time})"
auto_operations.scaffolding_warning_1.operations = "record.send_scaffolding_warning(sa_session,1)"
auto_operations.scaffolding_warning_1.time_cached = True
auto_operations.scaffolding_warning_1.schedule.hour = "*"
auto_operations.scaffolding_warning_1.schedule.minute = "*"
auto_operations.scaffolding_warning_2.criterion = "certificate_type = 'ID1515991410643754960468' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND valid_plus_1_email_status = 'Not Sent' AND (valid_end_plus_1 <= ${current_time})"
auto_operations.scaffolding_warning_2.operations = "record.send_scaffolding_warning(sa_session,2)"
auto_operations.scaffolding_warning_2.time_cached = True
auto_operations.scaffolding_warning_2.schedule.hour = "*"
auto_operations.scaffolding_warning_2.schedule.minute = "*"
auto_operations.notification_15_day.criterion = "certificate_type = 'ID1515991410643754960468' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND (NOT notification_date_15_day IS NULL) AND (notification_date_15_day <= ${current_time})"
auto_operations.notification_15_day.operations = "record.send_15_day_notification(sa_session)"
auto_operations.notification_15_day.time_cached = True
auto_operations.notification_15_day.schedule.hour = "*"
auto_operations.notification_15_day.schedule.minute = "*"
auto_operations.confine_warning_2.criterion = "certificate_type = 'ID1515991375703687072609' AND (NOT status = 'Closed') AND (NOT status = 'Complete') AND valid_plus_1_email_status = 'Not Sent' AND (valid_end_plus_1 <= ${current_time})"
auto_operations.confine_warning_2.operations = "record.send_confine_warning(sa_session,2)"
auto_operations.confine_warning_2.time_cached = True
auto_operations.confine_warning_2.schedule.hour = "*"
auto_operations.confine_warning_2.schedule.minute = "*"