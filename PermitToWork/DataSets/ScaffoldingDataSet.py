from j5.Database import Alchemy
from j5.IndustraForms.api import get_logbook_linked_forms
from PTTGC.PermitToWork.DataSets.DataSetHelper import DataSetHelper
from sjsoft.Apps.Reports import Export
import logging

class ScaffoldingDataSet(DataSetHelper):
    def create_metadata(self):
        # Field labels correspond to IndustraForm cell or report template labels
        # header_fields = [
        #     Export.FieldMetaData('moc_no', None, 'str', 'Text211'),
        #     #Export.FieldMetaData('permit_no', None, 'str', 'Permit No.') # Permit Number from log
        #     Export.FieldMetaData('permit_no', None, 'str', 'Permit No.') # Permit Number from log
        # ]

        header_fields = [
            Export.FieldMetaData('moc_no', None, 'str', 'Text211'), #1
            Export.FieldMetaData('applicant_name', None, 'str', 'Text1'), #
            Export.FieldMetaData('applicant_area1', None, 'str', 'area1'), #ApplicantArea1Choice
            Export.FieldMetaData('telephone_no', None, 'str', 'Number1'),#Integer45
            Export.FieldMetaData('permit_no', None, 'str', 'Permit No.') # Permit Number from log #1
        ]


        datetime_fields = [
            Export.FieldMetaData('permit_request_installation_start_date', None, 'datetime', 'DateTimeStart'),
            Export.FieldMetaData('permit_request_installation_end_date', None, 'datetime', 'DateTimeEnd'),
            Export.FieldMetaData('license_approval_contractor_approve_date', None, 'date', 'Date4'),
            Export.FieldMetaData('license_approval_ta_approve_date', None, 'date', 'Date5'),
            Export.FieldMetaData('license_approval_engineer_approve_date', None, 'date', 'Date6'),
            Export.FieldMetaData('license_approval_workshop_date', None, 'date', 'Date7'),
            Export.FieldMetaData('license_approval_jo_approve_date', None, 'date', 'Date9'),
            Export.FieldMetaData('dismantling_date', None, 'datetime', 'Date17'),
            Export.FieldMetaData('dismantling_hc_approve_date', None, 'date', 'Date13'),
            Export.FieldMetaData('dismantling_jo_approve_date', None, 'date', 'Date12'),
            Export.FieldMetaData('dismantling_ta_approve_date', None, 'date', 'Date18')
        ]

        permit_request_fields = [
            Export.FieldMetaData('employee_number', None, 'str', 'Integer40'),
            Export.FieldMetaData('applicant_name', None, 'str', 'SCRU_Name'),
            Export.FieldMetaData('applicant_area1', None, 'str', 'area1'),
            Export.FieldMetaData('applicant_restricted_area', None, 'str', 'ApplicantRestrictedAreaChoice'),
            Export.FieldMetaData('applicant_control_area', None, 'str', 'ApplicantControlAreaChoice'),
            Export.FieldMetaData('telephone_no', None, 'str', 'SCRU_Tel'),
            Export.FieldMetaData('num_installation_days', None, 'int', 'day_count'),
            Export.FieldMetaData('contractor_company', None, 'str', 'Text4'),
            Export.FieldMetaData('entity_area1', None, 'str', 'Choice65'),
            Export.FieldMetaData('entity_restricted_area', None, 'str', 'EntityRestrictedAreaChoice'),
            Export.FieldMetaData('entity_control_area', None, 'str', 'EntityControlAreaChoice'),
            Export.FieldMetaData('restricted_area', None, 'str', 'Text257'),#Text257Choice60
            Export.FieldMetaData('control_area', None, 'str', 'Choice61'),
            Export.FieldMetaData('scaffolding_installation_area', None, 'str', 'Text212'),
            Export.FieldMetaData('installation_characteristics', None, 'str', 'Choice1'),
            Export.FieldMetaData('scaffolding_material_type', None, 'str', 'Choice2'),
            Export.FieldMetaData('structural_scaffolding', None, 'str', 'Choice3'),
            Export.FieldMetaData('scaffolding_description_1', None, 'str', 'Text8'),
            Export.FieldMetaData('scaffolding_description_2', None, 'str', 'Text9'),
            Export.FieldMetaData('scaffolding_description_3', None, 'str', 'Text10'),
            Export.FieldMetaData('scaffolding_description_4', None, 'str', 'Text11'),
            Export.FieldMetaData('scaffolding_description_5', None, 'str', 'Text213'),
            Export.FieldMetaData('scaffolding_width_1', None, 'str', 'Number2'),
            Export.FieldMetaData('scaffolding_width_2', None, 'str', 'Number5'),
            Export.FieldMetaData('scaffolding_width_3', None, 'str', 'Number6'),
            Export.FieldMetaData('scaffolding_width_4', None, 'str', 'Number7'),
            Export.FieldMetaData('scaffolding_width_5', None, 'str', 'Number24'),
            Export.FieldMetaData('scaffolding_length_1', None, 'str', 'Number3'),
            Export.FieldMetaData('scaffolding_length_2', None, 'str', 'Number8'),
            Export.FieldMetaData('scaffolding_length_3', None, 'str', 'Number9'),
            Export.FieldMetaData('scaffolding_length_4', None, 'str', 'Number10'),
            Export.FieldMetaData('scaffolding_length_5', None, 'str', 'Number25'),
            Export.FieldMetaData('scaffolding_height_1', None, 'str', 'Number4'),
            Export.FieldMetaData('scaffolding_height_2', None, 'str', 'Number11'),
            Export.FieldMetaData('scaffolding_height_3', None, 'str', 'Number12'),
            Export.FieldMetaData('scaffolding_height_4', None, 'str', 'Number13'),
            Export.FieldMetaData('scaffolding_height_5', None, 'str', 'Number26'),
            Export.FieldMetaData('scaffolding_total_1', None, 'str', 'Number16'),
            Export.FieldMetaData('scaffolding_total_2', None, 'str', 'Number17'),
            Export.FieldMetaData('scaffolding_total_3', None, 'str', 'Number18'),
            Export.FieldMetaData('scaffolding_total_4', None, 'str', 'Number19'),
            Export.FieldMetaData('scaffolding_total_5', None, 'str', 'Number27'),
            Export.FieldMetaData('scaffolding_beyond_21_or_special', None, 'str', 'ChecklistItem19'),
            Export.FieldMetaData('head_contractor', None, 'str', 'CTT_Name'),
            Export.FieldMetaData('hc_contact', None, 'str', 'CTT_Tel'),
            Export.FieldMetaData('pttgc_job_owner', None, 'str', 'JON_Name'),
            Export.FieldMetaData('jo_employee_num', None, 'str', 'Number28'),
            Export.FieldMetaData('scaffold_image', None, 'str', 'Scaffold Image'),
            Export.FieldMetaData('technical_approver', None, 'str', 'Technical Approver'), # Section 4 Submission User
            Export.FieldMetaData('ta_sig', None, 'str', 'TA Signature'),
            Export.FieldMetaData('section_1_submit_date', None, 'datetime', 'Section 1 Submit Date')  # Section 1 Submit Date
        ]

        checklist_fields = [
            Export.FieldMetaData('checklist_item_1', None, 'str', 'ChecklistItem1'),
            Export.FieldMetaData('checklist_item_2', None, 'str', 'ChecklistItem2'),
            Export.FieldMetaData('checklist_item_3', None, 'str', 'ChecklistItem3'),
            Export.FieldMetaData('checklist_item_4', None, 'str', 'ChecklistItem4'),
            Export.FieldMetaData('checklist_item_5', None, 'str', 'ChecklistItem5'),
            Export.FieldMetaData('checklist_item_6', None, 'str', 'ChecklistItem6'),
            Export.FieldMetaData('checklist_item_7', None, 'str', 'ChecklistItem7'),
            Export.FieldMetaData('checklist_item_8', None, 'str', 'ChecklistItem8'),
            Export.FieldMetaData('checklist_item_9', None, 'str', 'ChecklistItem9'),
            Export.FieldMetaData('checklist_item_10', None, 'str', 'ChecklistItem10'),
            Export.FieldMetaData('checklist_item_11', None, 'str', 'ChecklistItem11'),
            Export.FieldMetaData('checklist_item_12', None, 'str', 'ChecklistItem12'),
            Export.FieldMetaData('checklist_item_13', None, 'str', 'ChecklistItem13'),
            Export.FieldMetaData('checklist_item_14', None, 'str', 'ChecklistItem14'),
            Export.FieldMetaData('checklist_item_15', None, 'str', 'ChecklistItem15'),
            Export.FieldMetaData('checklist_item_16', None, 'str', 'ChecklistItem16'),
            Export.FieldMetaData('checklist_item_17', None, 'str', 'ChecklistItem17'),
            Export.FieldMetaData('checklist_item_18', None, 'str', 'ChecklistItem18')
        ]

        license_approval_results_fields = [

            Export.FieldMetaData('contractor_name', None, 'str', 'Text13'),
            Export.FieldMetaData('contractor_contact', None, 'str', 'Integer43'),
            Export.FieldMetaData('scaff_tag', None, 'str', 'Checkbox1'),
            Export.FieldMetaData('scaff_tag_number', None, 'str', 'Number21'),
            Export.FieldMetaData('no_scaffolding_permitted', None, 'str', 'Checkbox2'),
            Export.FieldMetaData('text14', None, 'str', 'Text14'),
            Export.FieldMetaData('suggestion', None, 'str', 'Text214'),
            Export.FieldMetaData('engineer_name', None, 'str', 'Text16'),
            Export.FieldMetaData('pttgc_job_owner', None, 'str', 'Text205'),
            Export.FieldMetaData('num_days', None, 'str', 'Number22'),
            Export.FieldMetaData('pttgc_job_owner_2', None, 'str', 'Text254'),
            Export.FieldMetaData('technical_approver', None, 'str', 'Technical Approver'),
            Export.FieldMetaData('ta_sig', None, 'str', 'TA Signature'),

            Export.FieldMetaData('Submitter3', None, 'str', 'Section 3 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter5', None, 'str', 'Section 5 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter7', None, 'str', 'Section 7 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter8', None, 'str', 'Section 8 Submit User'),  # Work out in code below
            Export.FieldMetaData('Submitter9', None, 'str', 'Section 9 Submit User'),  # Work out in code below

            Export.FieldMetaData('Submitter3_datetime', None, 'datetime', 'Section 3 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter5_datetime', None, 'datetime', 'Section 5 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter7_datetime', None, 'datetime', 'Section 7 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter8_datetime', None, 'datetime', 'Section 8 Submit datetime'),  # Work out in code below
            Export.FieldMetaData('Submitter9_datetime', None, 'datetime', 'Section 9 Submit datetime')  # Work out in code below

        ]

        dismantling_fields = [
            Export.FieldMetaData('dismantling_job_owner', None, 'str', 'Text215'),
            Export.FieldMetaData('telephone_number', None, 'str', 'Number23'),
            Export.FieldMetaData('head_contractor', None, 'str', 'Text255'),
            Export.FieldMetaData('pttgc_job_owner', None, 'str', 'Text256'),
            Export.FieldMetaData('technical_approver', None, 'str', 'Technical Approver'),
            Export.FieldMetaData('ta_sig', None, 'str', 'TA Signature'),
        ]

        metadata = [Export.DataSetMetaData('1a_header.csv', '1a_header', header_fields)]
        metadata.extend([Export.DataSetMetaData('datetime_fields.csv', 'datetime_fields', datetime_fields)])
        metadata.extend([Export.DataSetMetaData('1b_permit_request.csv', '1b_permit_request', permit_request_fields)])
        metadata.extend([Export.DataSetMetaData('2a_checklist.csv', '2a_checklist', checklist_fields)])
        metadata.extend([Export.DataSetMetaData('2b_license_approval_results.csv', '2b_license_approval_results', license_approval_results_fields)])
        metadata.extend([Export.DataSetMetaData('3_dismantling.csv', '3_dismantling', dismantling_fields)])

        return metadata

    # def get_special_field_value(self, permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session):
    #     value = super(ColdWorkDataSet, self).get_special_field_value(permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session)
    #     if field_name == 'entity_area1':
    #         value = self.get_area_hierarchy_value(value)
    #     return value

    def generate_datasets(self, sa_session, params, locale, timezone):
        datasets = {}
        # Retrieve fields of data sets
        header_fields_metadata = self.get_metadata()['1a_header']
        header_field_names = [f.field_name for f in header_fields_metadata.fields]
        header_display_names = [f.display_name for f in header_fields_metadata.fields]
        datetime_fields_metadata = self.get_metadata()['datetime_fields']
        datetime_fields_names = [f.field_name for f in datetime_fields_metadata.fields]
        datetime_fields_display_names = [f.display_name for f in datetime_fields_metadata.fields]
        permit_request_fields_metadata = self.get_metadata()['1b_permit_request']
        permit_request_field_names = [f.field_name for f in permit_request_fields_metadata.fields]
        permit_request_display_names = [f.display_name for f in permit_request_fields_metadata.fields]
        checklist_fields_metadata = self.get_metadata()['2a_checklist']
        checklist_field_names = [f.field_name for f in checklist_fields_metadata.fields]
        checklist_display_names = [f.display_name for f in checklist_fields_metadata.fields]
        license_approval_fields_metadata = self.get_metadata()['2b_license_approval_results']
        license_approval_field_names = [f.field_name for f in license_approval_fields_metadata.fields]
        license_approval_display_names = [f.display_name for f in license_approval_fields_metadata.fields]
        dismantling_fields_metadata = self.get_metadata()['3_dismantling']
        dismantling_field_names = [f.field_name for f in dismantling_fields_metadata.fields]
        dismantling_display_names = [f.display_name for f in dismantling_fields_metadata.fields]

        # Populate header row of data sets
        datasets['1a_header'] = [header_field_names]
        datasets['datetime_fields'] = [datetime_fields_names]
        datasets['1b_permit_request'] = [permit_request_field_names]
        datasets['2a_checklist'] = [checklist_field_names]
        datasets['2b_license_approval_results'] = [license_approval_field_names]
        datasets['3_dismantling'] = [dismantling_field_names]

        # Get current permit
        #permit_class = Alchemy.find_recordclass('permits')
        #permit = sa_session.query(permit_class).filter(permit_class.logid == params['permit_logid']).first()
        certificate_class = Alchemy.find_recordclass('certificates')
        
        for param in params:
            logging.info("Param details: %s" % param)
        
        certificate = sa_session.query(certificate_class).filter(certificate_class.logid == params['permit_logid']).first()
        # Query data for each data set
        #forms = get_logbook_linked_forms(logbook_record=permit)
        forms = get_logbook_linked_forms(logbook_record=certificate)
        if forms:
            form_data_snapshot = forms[0].get_form_data_snapshot()

            # Header
            header_non_attrs = ['Permit No.']
            #header_non_attrs = ['Permit No.']
            header_attrs = [a for a in header_display_names if a not in header_non_attrs]
            header_attr_data = form_data_snapshot.query(header_attrs, default_element_attribute="DisplayValue")
            #header_non_attr_data = [permit.permit_no]
            header_non_attr_data = [certificate.certificate_no]
            # Datetime Fields
            datetime_fields_attr_data = form_data_snapshot.query(datetime_fields_display_names)

            # Permit Request
            permit_request_non_attrs = ['Scaffold Image', 'Technical Approver', 'TA Signature', 'Section 1 Submit Date']
            permit_request_attrs = [a for a in permit_request_display_names if a not in permit_request_non_attrs]
            permit_request_attr_data = form_data_snapshot.query(permit_request_attrs, default_element_attribute="DisplayValue")

            #scaffold_image = self.get_scaffold_image_from_permit(permit)
            scaffold_image = self.get_scaffold_image_from_permit(certificate)
            section_4_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Technical Approver review Basic Data')
            ta_user = section_4_submission_user_and_date.SubmittedBy
            logging.critical('********************************** ta_user ********** %s' % ta_user)
            ta_name = self.get_user_fullname_from_username(ta_user, sa_session)
            ta_signature = self.get_signature_from_user_username(ta_user, sa_session)
            section_1_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Request')
            section_1_submit_datetime = section_1_submission_user_and_date.SubmittedAt
            permit_request_non_attr_data = [scaffold_image] + [ta_name] + [ta_signature] + [section_1_submit_datetime]




            # Checklist
            checklist_attr_data = form_data_snapshot.query(checklist_display_names, default_element_attribute="DisplayValue")

            # misc_non_attrs = ['Section 2 Submit User', 'Section 4 Submit User', 'Section 9 Submit User', 'Section 10 Submit User', 'Section 2 Submit datetime', 'Section 4 Submit datetime', 'Section 9 Submit datetime', 'Section 10 Submit datetime']
            # misc_attrs = [a for a in misc_display_names if a not in misc_non_attrs]
            # misc_attr_data = form_data_snapshot.query(misc_attrs, default_element_attribute="DisplayValue")
            #
            # section_2_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Confine Space Control verify data from contractor')
            # section_2_submitter_user = section_2_submission_user_and_date.SubmittedBy
            # section_2_submitter_name = self.get_user_fullname_from_username(section_2_submitter_user, sa_session)
            # section_2_submitter_datetime = section_2_submission_user_and_date.SubmittedAt
            #
            # section_4_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Approval')
            # section_4_submitter_user = section_4_submission_user_and_date.SubmittedBy
            # section_4_submitter_name = self.get_user_fullname_from_username(section_4_submitter_user, sa_session)
            # section_4_submitter_datetime = section_4_submission_user_and_date.SubmittedAt
            #
            # section_9_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Permit Renew')
            # section_9_submitter_user = section_9_submission_user_and_date.SubmittedBy
            # section_9_submitter_name = self.get_user_fullname_from_username(section_9_submitter_user, sa_session)
            # section_9_submitter_datetime = section_9_submission_user_and_date.SubmittedAt
            #
            # section_10_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Close Permit')
            # section_10_submitter_user = section_10_submission_user_and_date.SubmittedBy
            # section_10_submitter_name = self.get_user_fullname_from_username(section_10_submitter_user, sa_session)
            # section_10_submitter_datetime = section_10_submission_user_and_date.SubmittedAt




            # License Approval
            license_approval_non_attrs = ['Technical Approver', 'TA Signature', 'Section 3 Submit User', 'Section 5 Submit User', 'Section 7 Submit User', 'Section 8 Submit User', 'Section 9 Submit User', 'Section 3 Submit datetime', 'Section 5 Submit datetime', 'Section 7 Submit datetime', 'Section 8 Submit datetime', 'Section 9 Submit datetime']
            license_approval_attrs = [a for a in license_approval_display_names if a not in license_approval_non_attrs]
            license_approval_attr_data = form_data_snapshot.query(license_approval_attrs, default_element_attribute="DisplayValue")                                               
            section_7_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Result of Permit')
            
            if not section_7_submission_user_and_date[0] == None :      
                ta_user = section_7_submission_user_and_date.SubmittedBy
                logging.critical('********************************** ta_user ********** %s' % ta_user)
                
            ta_name = self.get_user_fullname_from_username(ta_user, sa_session)            
            logging.critical('********************************** ta_name ********** %s' % ta_name)
            ta_signature = self.get_signature_from_user_username(ta_user, sa_session)
            logging.critical('********************************** ta_signature ********** ')
            #license_approval_non_attr_data = [ta_name] + [ta_signature]





            section_3_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Technical Approver review Basic Data')
            section_3_submitter_user = section_3_submission_user_and_date.SubmittedBy
            section_3_submitter_name = self.get_user_fullname_from_username(section_3_submitter_user, sa_session)
            section_3_submitter_datetime = section_3_submission_user_and_date.SubmittedAt

            section_5_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Technical Approver Inspection')
            section_5_submitter_user = section_5_submission_user_and_date.SubmittedBy
            section_5_submitter_name = self.get_user_fullname_from_username(section_5_submitter_user, sa_session)
            section_5_submitter_datetime = section_5_submission_user_and_date.SubmittedAt

            section_7_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Renew Date Request')
            section_7_submitter_user = section_7_submission_user_and_date.SubmittedBy
            section_7_submitter_name = self.get_user_fullname_from_username(section_7_submitter_user, sa_session)
            section_7_submitter_datetime = section_7_submission_user_and_date.SubmittedAt

            section_8_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Renew Date')
            section_8_submitter_user = section_8_submission_user_and_date.SubmittedBy
            section_8_submitter_name = self.get_user_fullname_from_username(section_8_submitter_user, sa_session)
            section_8_submitter_datetime = section_8_submission_user_and_date.SubmittedAt

            section_9_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Dismantling')
            section_9_submitter_user = section_9_submission_user_and_date.SubmittedBy
            section_9_submitter_name = self.get_user_fullname_from_username(section_9_submitter_user, sa_session)
            section_9_submitter_datetime = section_9_submission_user_and_date.SubmittedAt

            license_approval_non_attr_data = [ta_name] + [ta_signature] + [section_3_submitter_name, section_5_submitter_name, section_7_submitter_name, section_8_submitter_name, section_9_submitter_name, section_3_submitter_datetime, section_5_submitter_datetime, section_7_submitter_datetime, section_8_submitter_datetime, section_9_submitter_datetime]
            logging.critical('********************************** license_approval_non_attr_data ********** %s' % license_approval_non_attr_data)




            # Dismantling
            dismantling_non_attrs = ['Technical Approver', 'TA Signature']
            logging.critical('********************************** dismantling_non_attrs ********** %s' % dismantling_non_attrs)
            dismantling_attrs = [a for a in dismantling_display_names if a not in dismantling_non_attrs]
            logging.critical('********************************** dismantling_attrs ********** %s' % dismantling_attrs)
            dismantling_attr_data = form_data_snapshot.query(dismantling_attrs, default_element_attribute="DisplayValue")
            # logging.critical('********************************** dismantling_attr_data ********** %s' % dismantling_attr_data)
            section_8_submission_user_and_date = self.get_section_submission_user_and_date(form_data_snapshot, 'Dismantling')
            # logging.critical('********************************** section_8_submission_user_and_date ********** %s' % section_8_submission_user_and_date)
            if not section_8_submission_user_and_date[0] == None:
                ta_user = section_8_submission_user_and_date.SubmittedBy
                logging.critical('********************************** ta_user ********** %s' % ta_user)

            ta_name = self.get_user_fullname_from_username(ta_user, sa_session)
            logging.critical('********************************** ta_name ********** %s' % ta_name)
            ta_signature = self.get_signature_from_user_username(ta_user, sa_session)
            logging.critical('********************************** ta_signature **********')
            dismantling_non_attr_data = [ta_name] + [ta_signature]
            logging.critical('********************************** dismantling_non_attr_data ********** %s' % dismantling_non_attr_data)



            # Append data to data sets
            #
            # Header
            # # Form data
            # if header_attr_data:
            #     datasets['1a_header'].append([Export.render_value_for_birt(header_field_names[0], header_attr_data[0], sa_session)])
            # for i, v in enumerate(header_attr_data[1:]):
            #     datasets['1a_header'][1].extend([Export.render_value_for_birt(header_field_names[i], v, sa_session)])
            # # Non-form data
            # if not header_attr_data:
            #     datasets['1a_header'][1].append(header_non_attr_data)
            # else:
            #     datasets['1a_header'][1].extend(header_non_attr_data)

            # Form data
            # logging.critical('********************************** Line 271 ********************************** header_attr_data ********** %s' % header_attr_data)


            if  header_attr_data:
                datasets['1a_header'].append([Export.render_value_for_birt(header_field_names[0], header_attr_data[0], sa_session)])
                logging.critical('********************************** Line 274    if  header_attr_data: **********' )
            for i, v in enumerate(header_attr_data[1:]):
                if v and isinstance(v, list):
                    v = str(v).replace("u'", "").replace(","," >").replace("'", "").strip("[").strip("]")
                    logging.critical('********************************** Line 278 ********************************** v ********** %s' % v)
                datasets['1a_header'][1].extend([Export.render_value_for_birt(header_field_names[i], v, sa_session)])

            if not header_attr_data:
                datasets['1a_header'][1].append(header_non_attr_data)
                logging.critical('********************************** Line 283    if not header_attr_data:: **********')
            else:
                datasets['1a_header'][1].extend(header_non_attr_data)
                logging.critical('********************************** Line 286    if not header_attr_data:: **********')

            # Datetimes
            for i, v in enumerate(datetime_fields_attr_data):
                if i == 0:
                    datasets['datetime_fields'].append([Export.render_value_for_birt(datetime_fields_names[i], v, sa_session)])
                else:
                    datasets['datetime_fields'][1].extend([Export.render_value_for_birt(datetime_fields_names[i], v, sa_session)])

            # Permit Request
            for i, v in enumerate(permit_request_attr_data):
                if i == 0:
                    datasets['1b_permit_request'].append([Export.render_value_for_birt(permit_request_field_names[i], v, sa_session)])
                else:
                    datasets['1b_permit_request'][1].extend([Export.render_value_for_birt(permit_request_field_names[i], v, sa_session)])
    
            if not permit_request_attr_data:
                for i, v in enumerate(permit_request_non_attr_data):
                    datasets['1b_permit_request'][1].append([Export.render_value_for_birt(permit_request_non_attrs[i], v, sa_session)])
            else:
                for i, v in enumerate(permit_request_non_attr_data):
                    datasets['1b_permit_request'][1].extend([Export.render_value_for_birt(permit_request_non_attrs[i], v, sa_session)])

            # Checklist
            for i, v in enumerate(checklist_attr_data):
                if i == 0:
                    datasets['2a_checklist'].append(
                        [Export.render_value_for_birt(checklist_field_names[i], v, sa_session)])
                else:
                    datasets['2a_checklist'][1].extend(
                        [Export.render_value_for_birt(checklist_field_names[i], v, sa_session)])
    
            # License Approval
            for i, v in enumerate(license_approval_attr_data):
                if i == 0:
                    datasets['2b_license_approval_results'].append(
                        [Export.render_value_for_birt(license_approval_field_names[i], v, sa_session)])
                else:
                    datasets['2b_license_approval_results'][1].extend(
                        [Export.render_value_for_birt(license_approval_field_names[i], v, sa_session)])

            if not license_approval_attr_data:
                for i, v in enumerate(license_approval_non_attr_data):
                    datasets['2b_license_approval_results'][1].append(
                        [Export.render_value_for_birt(license_approval_non_attrs[i], v, sa_session)])
            else:
                for i, v in enumerate(license_approval_non_attr_data):
                    datasets['2b_license_approval_results'][1].extend(
                        [Export.render_value_for_birt(license_approval_non_attrs[i], v, sa_session)])
    
            # Dismantling
            for i, v in enumerate(dismantling_attr_data):
                if i == 0:
                    datasets['3_dismantling'].append(
                        [Export.render_value_for_birt(dismantling_field_names[i], v, sa_session)])
                else:
                    datasets['3_dismantling'][1].extend(
                        [Export.render_value_for_birt(dismantling_field_names[i], v, sa_session)])

            if not dismantling_attr_data:
                for i, v in enumerate(dismantling_non_attr_data):
                    datasets['3_dismantling'][1].append(
                        [Export.render_value_for_birt(dismantling_non_attrs[i], v, sa_session)])
            else:
                for i, v in enumerate(dismantling_non_attr_data):
                    datasets['3_dismantling'][1].extend(
                        [Export.render_value_for_birt(dismantling_non_attrs[i], v, sa_session)])

        return datasets

Plugin = ScaffoldingDataSet