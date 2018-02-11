from j5.Database import Alchemy
from j5.IndustraForms.api import get_logbook_linked_forms
from PTTGC.PermitToWork.DataSets.DataSetHelper import DataSetHelper
from sjsoft.Apps.Reports import Export
import logging

class ConfinedSpaceEntryDataSet(DataSetHelper):
    def create_metadata(self):
        # Field labels correspond to IndustraForm cell or report template labels
        header_fields = [
            Export.FieldMetaData('moc_no', None, 'str', 'Text211'), #1
            Export.FieldMetaData('applicant_name', None, 'str', 'Text1'), #
            Export.FieldMetaData('applicant_area1', None, 'str', 'area1'), #ApplicantArea1Choice
            Export.FieldMetaData('telephone_no', None, 'str', 'Number1'),#Integer45
            Export.FieldMetaData('permit_no', None, 'str', 'Permit No.') # Permit Number from log #1
        ]

        #For datetime fields only
        datetime_fields = [
            Export.FieldMetaData('permit_request_installation_start_date', None, 'datetime', 'DateTimeStart'),#
            Export.FieldMetaData('permit_request_installation_end_date', None, 'datetime', 'DateTimeEnd'),#
            Export.FieldMetaData('hole_watch_man1', None, 'datetime', 'DateTime92'),#
            Export.FieldMetaData('DateTime87', None, 'datetime', 'DateTime87'),  #
            Export.FieldMetaData('DateTime95', None, 'datetime', 'DateTime95'),  #
            Export.FieldMetaData('DateTime56', None, 'datetime', 'DateTime56'),  #
            Export.FieldMetaData('hole_watch_man2', None, 'datetime', 'DateTime93'),#
            Export.FieldMetaData('Confine_name_1_start_date', None, 'datetime', 'DateTime11'),#
            Export.FieldMetaData('Confine_name_1_end_date', None, 'datetime', 'DateTime12'),#
            Export.FieldMetaData('Confine_name_2_start_date', None, 'datetime', 'DateTime13'),#
            Export.FieldMetaData('Confine_name_2_end_date', None, 'datetime', 'DateTime14'),#
            Export.FieldMetaData('Confine_name_3_start_date', None, 'datetime', 'DateTime15'),#
            Export.FieldMetaData('Confine_name_3_end_date', None, 'datetime', 'DateTime16'),#
            Export.FieldMetaData('Confine_name_4_start_date', None, 'datetime', 'DateTime17'),#
            Export.FieldMetaData('Confine_name_4_end_date', None, 'datetime', 'DateTime18'),#
            Export.FieldMetaData('Confine_name_5_start_date', None, 'datetime', 'DateTime19'),#
            Export.FieldMetaData('Confine_name_5_end_date', None, 'datetime', 'DateTime20'),#
            Export.FieldMetaData('Confine_name_6_start_date', None, 'datetime', 'DateTime21'),#
            Export.FieldMetaData('Confine_name_6_end_date', None, 'datetime', 'DateTime22'),#
            Export.FieldMetaData('Confine_name_7_start_date', None, 'datetime', 'DateTime23'),#
            Export.FieldMetaData('Confine_name_7_end_date', None, 'datetime', 'DateTime24'),#
            Export.FieldMetaData('Confine_name_8_start_date', None, 'datetime', 'DateTime25'),#
            Export.FieldMetaData('Confine_name_8_end_date', None, 'datetime', 'DateTime26'),#
            Export.FieldMetaData('Confine_name_9_start_date', None, 'datetime', 'DateTime27'),#
            Export.FieldMetaData('Confine_name_9_end_date', None, 'datetime', 'DateTime28'),#
            Export.FieldMetaData('Confine_name_10_start_date', None, 'datetime', 'DateTime29'),#
            Export.FieldMetaData('Confine_name_10_end_date', None, 'datetime', 'DateTime30'),#
            Export.FieldMetaData('Confine_name_11_start_date', None, 'datetime', 'DateTime31'),#
            Export.FieldMetaData('Confine_name_11_end_date', None, 'datetime', 'DateTime32'),#
            Export.FieldMetaData('Confine_name_12_start_date', None, 'datetime', 'DateTime33'),#
            Export.FieldMetaData('Confine_name_12_end_date', None, 'datetime', 'DateTime34'),#
            Export.FieldMetaData('DateTime53', None, 'datetime', 'DateTime53'),  #
            Export.FieldMetaData('license_approval_contractor_approve_date', None, 'date', 'Date3'),##
            Export.FieldMetaData('Date4', None, 'date', 'Date4'),  ##
            Export.FieldMetaData('Date5', None, 'date', 'Date5'),  ##
            Export.FieldMetaData('license_approval_confine_space_approver_date', None, 'datetime', 'DateTime90'),#
            Export.FieldMetaData('license_approval_permit_approve_date', None, 'datetime', 'DateTime91'),#
            Export.FieldMetaData('gas_detection_reading1', None, 'datetime', 'DateTime96'),#
            Export.FieldMetaData('gas_detection_reading2', None, 'datetime', 'DateTime97'),#
            Export.FieldMetaData('gas_detection_reading3', None, 'datetime', 'DateTime98'),#
            Export.FieldMetaData('gas_detection_reading4', None, 'datetime', 'DateTime99')           ]
        
        checklist_fields = [
            Export.FieldMetaData('checklist_item_1', None, 'str', 'ChecklistItem2'),#
            Export.FieldMetaData('checklist_item_2', None, 'str', 'ChecklistItem3'),#
            Export.FieldMetaData('checklist_item_3', None, 'str', 'ChecklistItem4'),#
            Export.FieldMetaData('checklist_item_4', None, 'str', 'ChecklistItem5'),#
            Export.FieldMetaData('checklist_item_5', None, 'str', 'ChecklistItem6'),#
            Export.FieldMetaData('checklist_item_6', None, 'str', 'ChecklistItem7'),#
            Export.FieldMetaData('checklist_item_7', None, 'str', 'ChecklistItem8')#
        ]

        ppe_fields = [
            Export.FieldMetaData('Checkbox4', None, 'str', 'Checkbox4'),
            Export.FieldMetaData('Checkbox5', None, 'str', 'Checkbox5'),
            Export.FieldMetaData('Checkbox7', None, 'str', 'Checkbox7'),
            Export.FieldMetaData('Checkbox8', None, 'str', 'Checkbox8'),
            Export.FieldMetaData('Checkbox9', None, 'str', 'Checkbox9'),
            Export.FieldMetaData('Checkbox10', None, 'str', 'Checkbox10'),
            Export.FieldMetaData('Checkbox11', None, 'str', 'Checkbox11'),
            Export.FieldMetaData('Checkbox12', None, 'str', 'Checkbox12')
        ]

        misc_fields = [
            Export.FieldMetaData('employee_number', None, 'str', 'Integer40'),#not Use
            Export.FieldMetaData('num_installation_days', None, 'str', 'Label80'),
            Export.FieldMetaData('contractor_company', None, 'str', 'Text3'),#Text3
            Export.FieldMetaData('Text232', None, 'str', 'Text232'),  #
            Export.FieldMetaData('entity_area1', None, 'str', 'EntityArea1Choice'),
            Export.FieldMetaData('entity_restricted_area', None, 'str', 'EntityRestrictedAreaChoice'),
            Export.FieldMetaData('entity_control_area', None, 'str', 'EntityControlAreaChoice'),
            Export.FieldMetaData('restricted_area', None, 'str', 'Choice60'),
            Export.FieldMetaData('control_area', None, 'str', 'Choice61'),
            Export.FieldMetaData('choice65', None, 'str', 'Choice65'),
            Export.FieldMetaData('confine_installation_area', None, 'str', 'Text6'),#Text212
            Export.FieldMetaData('installation_tool', None, 'str', 'Text4'),#Choice1
            Export.FieldMetaData('Text233', None, 'str', 'Text233'),  #
            Export.FieldMetaData('installation_tool_num', None, 'str', 'Text40'),#Choice1Text225
            Export.FieldMetaData('installation_tool_des', None, 'str', 'Text225'),#Choice1Text225
            Export.FieldMetaData('hole_watch_man1', None, 'str', 'Text44'),#
            Export.FieldMetaData('hole_watch_man2', None, 'str', 'Text45'),#
            Export.FieldMetaData('rescue_team', None, 'str', 'Text9'),##
            Export.FieldMetaData('rescue_team_commu', None, 'str', 'Text10'),#
            Export.FieldMetaData('hole_man1', None, 'str', 'Text17'),#
            Export.FieldMetaData('hole_man2', None, 'str', 'Text18'),#
            Export.FieldMetaData('hole_man3', None, 'str', 'Text19'),#
            Export.FieldMetaData('hole_man4', None, 'str', 'Text20'),#
            Export.FieldMetaData('hole_man5', None, 'str', 'Text21'),#
            Export.FieldMetaData('hole_man6', None, 'str', 'Text22'),#
            Export.FieldMetaData('hole_man7', None, 'str', 'Text23'),#
            Export.FieldMetaData('hole_man8', None, 'str', 'Text24'),#
            Export.FieldMetaData('hole_man9', None, 'str', 'Text25'),#
            Export.FieldMetaData('hole_man10', None, 'str', 'Text26'),#
            Export.FieldMetaData('hole_man11', None, 'str', 'Text27'),#
            Export.FieldMetaData('hole_man12', None, 'str', 'Text28'),#
            Export.FieldMetaData('main_work_permit_num', None, 'str', 'PermitNo'),#
            Export.FieldMetaData('description', None, 'str', 'Text225'),#gastest
            Export.FieldMetaData('head_contractor', None, 'str', 'Text12'),
            Export.FieldMetaData('hc_contact', None, 'str', 'Integer42'),
            Export.FieldMetaData('pttgc_job_owner', None, 'str', 'Text204'),
            Export.FieldMetaData('jo_employee_num', None, 'str', 'Integer41'),
            Export.FieldMetaData('other_ppe', None, 'str', 'Text16'),
            Export.FieldMetaData('Choice57', None, 'str', 'Choice57'),
            Export.FieldMetaData('Choice58', None, 'str', 'Choice58'),
            Export.FieldMetaData('Choice59', None, 'str', 'Choice59'),
            Export.FieldMetaData('Checkbox13', None, 'str', 'Checkbox13'),
            Export.FieldMetaData('lel_frequency', None, 'float', 'Number190'),#
            Export.FieldMetaData('o2_frequency', None, 'float', 'Number191'),#
            Export.FieldMetaData('h2o_frequency', None, 'float', 'Number192'),#
            Export.FieldMetaData('co_frequency', None, 'float', 'Number193'),#
            Export.FieldMetaData('other_frequency1', None, 'float', 'Number194'),#
            Export.FieldMetaData('other_frequency2', None, 'float', 'Number195'),#
            Export.FieldMetaData('lel_1', None, 'float', 'Number196'),  #
            Export.FieldMetaData('lel_2', None, 'float', 'Integer43'),#
            Export.FieldMetaData('lel_3', None, 'float', 'Integer49'),  #
            Export.FieldMetaData('lel_4', None, 'float', 'Integer55'),  #
            Export.FieldMetaData('lel_5', None, 'float', 'Integer61'),  #
            Export.FieldMetaData('02_1', None, 'float', 'Number197'),  #
            Export.FieldMetaData('02_2', None, 'float', 'Integer44'),  #
            Export.FieldMetaData('02_3', None, 'float', 'Integer50'),  #
            Export.FieldMetaData('02_4', None, 'float', 'Integer56'),  #
            Export.FieldMetaData('02_5', None, 'float', 'Integer62'),  #
            Export.FieldMetaData('h2s_1', None, 'float', 'Number198'),  #
            Export.FieldMetaData('h2s_2', None, 'float', 'Integer45'),  #
            Export.FieldMetaData('h2s_3', None, 'float', 'Integer51'),  #
            Export.FieldMetaData('h2s_4', None, 'float', 'Integer57'),  #
            Export.FieldMetaData('h2s_5', None, 'float', 'Integer63'),  #
            Export.FieldMetaData('other_1_1', None, 'float', 'Number199'),  #
            Export.FieldMetaData('other_1_2', None, 'float', 'Integer46'),  #
            Export.FieldMetaData('other_1_3', None, 'float', 'Integer52'),  #
            Export.FieldMetaData('other_1_4', None, 'float', 'Integer58'),  #
            Export.FieldMetaData('other_1_5', None, 'float', 'Integer64'),  #
            Export.FieldMetaData('other_2_1', None, 'float', 'Number200'),  #
            Export.FieldMetaData('other_2_2', None, 'float', 'Integer47'),  #
            Export.FieldMetaData('other_2_3', None, 'float', 'Integer53'),  #
            Export.FieldMetaData('other_2_4', None, 'float', 'Integer59'),  #
            Export.FieldMetaData('other_2_5', None, 'float', 'Integer65'),  #
            Export.FieldMetaData('other_3_1', None, 'float', 'Number201'),  #
            Export.FieldMetaData('other_3_2', None, 'float', 'Integer48'),  #
            Export.FieldMetaData('other_3_3', None, 'float', 'Integer54'),  #
            Export.FieldMetaData('other_3_4', None, 'float', 'Integer60'),  #
            Export.FieldMetaData('other_3_5', None, 'float', 'Integer66'),  #
            Export.FieldMetaData('h2o_standard', None, 'float', 'Integer45'),#
            Export.FieldMetaData('co_standard', None, 'float', 'Integer46'),#
            Export.FieldMetaData('other_standard1', None, 'float', 'Integer47'),#
            Export.FieldMetaData('other_standard2', None, 'float', 'Integer48'),#
            Export.FieldMetaData('agt_1', None, 'str', 'Text215'),  #
            Export.FieldMetaData('agt_2', None, 'str', 'Text216'),#
            Export.FieldMetaData('agt_3', None, 'str', 'Text220'),  #
            Export.FieldMetaData('agt_4', None, 'str', 'Text221'),  #
            Export.FieldMetaData('agt_5', None, 'str', 'Text222'),  #
            Export.FieldMetaData('Text229', None, 'str', 'JON_Name'),  #
            Export.FieldMetaData('other_1_measurement', None, 'str', 'Text203'),
            Export.FieldMetaData('other_2_measurement', None, 'str', 'Text223'),
            Export.FieldMetaData('other_3_measurement', None, 'str', 'Text224'),
            Export.FieldMetaData('Text41', None, 'str', 'Text41'),
            Export.FieldMetaData('Text42', None, 'str', 'Text42'),
            Export.FieldMetaData('Number184', None, 'float', 'Number184'),  #
            Export.FieldMetaData('Number185', None, 'float', 'Number185'),  #
            Export.FieldMetaData('Number186', None, 'float', 'Number186'),  #
            Export.FieldMetaData('Number187', None, 'float', 'Number187'),  #
            Export.FieldMetaData('Number188', None, 'float', 'Number188'),  #
            Export.FieldMetaData('Number189', None, 'float', 'Number189'),  #
            Export.FieldMetaData('Text38', None, 'str', 'Text38'),  #
            # Export.FieldMetaData('Submitter4', None, 'str', 'Section 4 Submit User'),  # Work out in code below
            # Export.FieldMetaData('Submitter8', None, 'str', 'Section 8 Submit User'),  # Work out in code below
            # Export.FieldMetaData('Submitter9', None, 'str', 'Section 9 Submit User')  # Work out in code below
            Export.FieldMetaData('Submitter2', None, 'str', 'Section 2 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter4', None, 'str', 'Section 4 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter9', None, 'str', 'Section 9 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter10', None, 'str', 'Section 10 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter2_datetime', None, 'datetime', 'Section 2 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter4_datetime', None, 'datetime', 'Section 4 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter9_datetime', None, 'datetime', 'Section 9 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter10_datetime', None, 'datetime', 'Section 10 Submit datetime')  # Work out in code below
        ]

        metadata = [Export.DataSetMetaData('1a_header.csv', '1a_header', header_fields)]
        metadata.extend([Export.DataSetMetaData('2a_checklist.csv', '2a_checklist', checklist_fields)])
        metadata.extend([Export.DataSetMetaData('3_ppe_fields.csv', '3_ppe_fields', ppe_fields)])
        metadata.extend([Export.DataSetMetaData('4_misc.csv', '4_misc', misc_fields)])
        metadata.extend([Export.DataSetMetaData('datetime_fields.csv', 'datetime_fields', datetime_fields)])
        return metadata

    def generate_datasets(self, sa_session, params, locale, timezone):
        datasets = {}
        # Retrieve fields of data sets
        header_fields_metadata = self.get_metadata()['1a_header']
        header_field_names = [f.field_name for f in header_fields_metadata.fields]
        header_display_names = [f.display_name for f in header_fields_metadata.fields]
        datetime_fields_metadata = self.get_metadata()['datetime_fields']
        datetime_fields_names = [f.field_name for f in datetime_fields_metadata.fields]
        datetime_fields_display_names = [f.display_name for f in datetime_fields_metadata.fields]
        checklist_fields_metadata = self.get_metadata()['2a_checklist']
        checklist_field_names = [f.field_name for f in checklist_fields_metadata.fields]
        checklist_display_names = [f.display_name for f in checklist_fields_metadata.fields]
        ppe_fields_metadata = self.get_metadata()['3_ppe_fields']
        ppe_field_names = [f.field_name for f in ppe_fields_metadata.fields]
        ppe_display_names = [f.display_name for f in ppe_fields_metadata.fields]
        misc_fields_metadata = self.get_metadata()['4_misc']
        misc_field_names = [f.field_name for f in misc_fields_metadata.fields]
        misc_display_names = [f.display_name for f in misc_fields_metadata.fields]


        # Populate header row of data sets
        datasets['1a_header'] = [header_field_names]
        datasets['2a_checklist'] = [checklist_field_names]
        datasets['3_ppe_fields'] = [ppe_field_names]
        datasets['4_misc'] = [misc_field_names]
        datasets['datetime_fields'] = [datetime_fields_names]

        # Get current Certificate
        certificate_class = Alchemy.find_recordclass('certificates')
        
        for param in params:
            logging.info("Param details: %s" % param)
        
        certificate = sa_session.query(certificate_class).filter(certificate_class.logid == params['permit_logid']).first()
        # Query data for each data set
        forms = get_logbook_linked_forms(logbook_record=certificate)
        if forms:
            form_data_snapshot = forms[0].get_form_data_snapshot()

            # ------
            # Header
            # ------
            header_non_attrs = ['Permit No.']
            header_attrs = [a for a in header_display_names if a not in header_non_attrs]
            header_attr_data = form_data_snapshot.query(header_attrs, default_element_attribute="DisplayValue")
            header_non_attr_data = [certificate.certificate_no]

            # Form data
            if header_attr_data:
                datasets['1a_header'].append([Export.render_value_for_birt(header_field_names[0], header_attr_data[0], sa_session)])
            for i, v in enumerate(header_attr_data[1:]):
                if v and isinstance(v, list):
                    v = str(v).replace("u'", "").replace(","," >").replace("'", "").strip("[").strip("]")
                datasets['1a_header'][1].extend([Export.render_value_for_birt(header_field_names[i], v, sa_session)])
            # Non-form data
            if not header_attr_data:
                datasets['1a_header'][1].append(header_non_attr_data)
            else:
                datasets['1a_header'][1].extend(header_non_attr_data)

            # Checklist from IndustraForms
            checklist_attr_data = form_data_snapshot.query(checklist_display_names,
                                                           default_element_attribute="DisplayValue")
            if checklist_attr_data:
                datasets['2a_checklist'].append(
                    [Export.render_value_for_birt(checklist_field_names[0], checklist_attr_data[0], sa_session)])
            for i, v in enumerate(checklist_attr_data[1:]):
                datasets['2a_checklist'][1].extend(
                    [Export.render_value_for_birt(checklist_field_names[i], v, sa_session)])

            # ---
            # PPE
            # ---
            ppe_fields_attr_data = form_data_snapshot.query(ppe_display_names)
            for i, v in enumerate(ppe_fields_attr_data):
                if i == 0:
                    datasets['3_ppe_fields'].append(
                        [Export.render_value_for_birt(ppe_field_names[i], v, sa_session)])
                else:
                    datasets['3_ppe_fields'][1].extend(
                        [Export.render_value_for_birt(ppe_field_names[i], v, sa_session)])

            # # # ---- Confine Space Control verify data from contractor
            # # # Misc
            # # # ----
            # # misc_non_attrs = ['Section 4 Submit User', 'Section 8 Submit User', 'Section 9 Submit User']
            # # misc_attrs = [a for a in misc_display_names if a not in misc_non_attrs]
            # # misc_attr_data = form_data_snapshot.query(misc_attrs, default_element_attribute="DisplayValue")
            # #
            # # section_4_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Preparation')
            # # section_4_submitter_user = section_4_submission_user_and_date.SubmittedBy
            # # section_4_submitter_name = self.get_user_fullname_from_username(section_4_submitter_user, sa_session)
            # #
            # # section_8_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Renew Request')
            # # section_8_submitter_user = section_4_submission_user_and_date.SubmittedBy
            # # section_8_submitter_name = self.get_user_fullname_from_username(section_4_submitter_user, sa_session)
            # #
            # # section_9_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Renew')
            # # section_9_submitter_user = section_4_submission_user_and_date.SubmittedBy
            # # section_9_submitter_name = self.get_user_fullname_from_username(section_4_submitter_user, sa_session)
            #
            # misc_non_attr_data = [section_4_submitter_name, section_8_submitter_name, section_9_submitter_name]

            # # ---- Confine Space Control verify data from contractor
            # # Misc
            # # ----
            # misc_non_attrs = ['Section 4 Submit User', 'Section 8 Submit User', 'Section 9 Submit User']
            misc_non_attrs = ['Section 2 Submit User', 'Section 4 Submit User', 'Section 9 Submit User', 'Section 10 Submit User', 'Section 2 Submit datetime', 'Section 4 Submit datetime', 'Section 9 Submit datetime', 'Section 10 Submit datetime']
            misc_attrs = [a for a in misc_display_names if a not in misc_non_attrs]
            misc_attr_data = form_data_snapshot.query(misc_attrs, default_element_attribute="DisplayValue")

            section_2_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Confine Space Control verify data from contractor')
            section_2_submitter_user = section_2_submission_user_and_date.SubmittedBy
            section_2_submitter_name = self.get_user_fullname_from_username(section_2_submitter_user, sa_session)
            section_2_submitter_datetime = section_2_submission_user_and_date.SubmittedAt

            section_4_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Approval')
            section_4_submitter_user = section_4_submission_user_and_date.SubmittedBy
            section_4_submitter_name = self.get_user_fullname_from_username(section_4_submitter_user, sa_session)
            section_4_submitter_datetime = section_4_submission_user_and_date.SubmittedAt

            section_9_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Renew')
            section_9_submitter_user = section_9_submission_user_and_date.SubmittedBy
            section_9_submitter_name = self.get_user_fullname_from_username(section_9_submitter_user, sa_session)
            section_9_submitter_datetime = section_9_submission_user_and_date.SubmittedAt

            section_10_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Close Permit')
            section_10_submitter_user = section_10_submission_user_and_date.SubmittedBy
            section_10_submitter_name = self.get_user_fullname_from_username(section_10_submitter_user, sa_session)
            section_10_submitter_datetime = section_10_submission_user_and_date.SubmittedAt

            # misc_non_attr_data = [section_4_submitter_name, section_8_submitter_name, section_9_submitter_name]
            misc_non_attr_data = [section_2_submitter_name, section_4_submitter_name, section_9_submitter_name, section_10_submitter_name, section_2_submitter_datetime, section_4_submitter_datetime, section_9_submitter_datetime, section_10_submitter_datetime]

            # Form data
            if misc_attr_data:
                datasets['4_misc'].append([Export.render_value_for_birt(misc_field_names[0], misc_attr_data[0], sa_session)])
            for i, v in enumerate(misc_attr_data[1:]):
                datasets['4_misc'][1].extend([Export.render_value_for_birt(misc_field_names[i], v, sa_session)])
            # Non-form data
            if not misc_attr_data:
                datasets['4_misc'][0].append(misc_non_attrs)
                datasets['4_misc'][1].append(misc_non_attr_data)
            else:
                datasets['4_misc'][0].extend(misc_non_attrs)
                datasets['4_misc'][1].extend(misc_non_attr_data)

            # ---------
            # Datetimes
            # ---------
            datetime_fields_attr_data = form_data_snapshot.query(datetime_fields_display_names)
            for i, v in enumerate(datetime_fields_attr_data):
                if i == 0:
                    datasets['datetime_fields'].append(
                        [Export.render_value_for_birt(datetime_fields_names[i], v, sa_session)])
                else:
                    datasets['datetime_fields'][1].extend(
                        [Export.render_value_for_birt(datetime_fields_names[i], v, sa_session)])

        return datasets

Plugin = ConfinedSpaceEntryDataSet
