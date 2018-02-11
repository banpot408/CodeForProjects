import base64
from collections import OrderedDict
from sjsoft.Apps.Reports import Export
from j5.Database import Alchemy
from j5.IndustraForms.api import get_logbook_linked_forms
from j5.IndustraForms import beta_api_230
import logging

class DataSetHelper(Export.DataSetPlugin):
    permit_logclass = Alchemy.find_recordclass('permits')
    certificate_logclass = Alchemy.find_recordclass('certificates')
    permit_forms_logclass = Alchemy.find_recordclass('permit_forms')
    sf_form_register_logclass = Alchemy.find_recordclass('sf_form_register')

    certificates_required = {
        'PTTGC.PermitToWork.confined_space_entry': 'confined_space_certificate_no',
        'cranelist': 'crane_lifting_certificate_no',
        'PTTGC.PermitToWork.excavation_certificate': 'excavation_certificate_no',
        'boxup': 'box_up_certificate_no',
        'rad': 'radiography_certificate_no',
        'PTTGC.PermitToWork.diving': 'diving_certificate_no',
        'PTTGC.PermitToWork.scaffolding': 'scaffolding_certificate_no',
        'roadclose': 'road_close_certificate_no',
        'nearby': 'nearby_high_voltage_certificate_no'
    }
    #self.print_approvals_user('Cosigner approval for Work Permit', sa_session)
    def get_signature_from_user_fullname(self, fullname, sa_session):
        personnel_logclass = Alchemy.find_recordclass('personnel')
        personnel_record = sa_session.query(personnel_logclass).filter(personnel_logclass.lastname == fullname).first()
        image = None
        if personnel_record:
            store = personnel_logclass.logpage.get_resource("storage")
            store = store.substore("%s.%s" % ('signature_image', personnel_record.signature_image))
            files = store.listfiles()
            if files:
                filename = files[0]
                image = store.read(filename)
        return self.get_encoded_image(image)

    def get_signature_from_user_username(self, username, sa_session):
        personnel_logclass = Alchemy.find_recordclass('personnel')
        personnel_record = sa_session.query(personnel_logclass).filter(personnel_logclass.j5username == username).first()
        image = None
        if personnel_record:
            store = personnel_logclass.logpage.get_resource("storage")
            store = store.substore("%s.%s" % ('signature_image', personnel_record.signature_image))
            files = store.listfiles()
            if files:
                filename = files[0]
                image = store.read(filename)
        return self.get_encoded_image(image)



    #def get_scaffold_image_from_permit(self, permit):
        #image = None
        #permits_logclass = Alchemy.find_recordclass('permits')
        #if permit and permit.logid:
            ##store = permits_logclass.logpage.get_resource("storage")

            
#store = store.substore("%s.%s" % ('scaffold_image', permit.scaffold_image))
            ##files = store.listfiles()
            #if files:
                #filename = files[0]
                #image = store.read(filename)
        #return self.get_encoded_image(image)
    def get_scaffold_image_from_permit(self, certificate):
        image = None
        certificate_logclass = Alchemy.find_recordclass('certificates')
        if certificate and certificate.logid:
            store = certificate_logclass.logpage.get_resource("storage")
            store = store.substore("%s.%s" % ('scaffold_image', certificate.scaffold_image))
            files = store.listfiles()
            if files:
                filename = files[0]
                image = store.read(filename)
        return self.get_encoded_image(image)
        
    def get_confined_space_entry_image_from_permit(self, certificate):
        image = None
        certificate_logclass = Alchemy.find_recordclass('certificates')
        if certificate and certificate.logid:
            store = certificate_logclass.logpage.get_resource("storage")
            store = store.substore("%s.%s" % ('confined_space_entry_image', certificate.confined_space_image))
            files = store.listfiles()
            if files:
                filename = files[0]
                image = store.read(filename)
        return self.get_encoded_image(image)    
    
    @staticmethod
    def get_encoded_image(image=None):
        if not image:
            return
        if isinstance(image, unicode):
            image = image.encode("utf8")
        return base64.b64encode(image)

    def get_permit_number(self, sa_session, permit_logid):
        permit_record = sa_session.query(self.permit_logclass.permit_no).filter_by(logid=permit_logid).first()
        if permit_record:
            return permit_record.permit_no

    @staticmethod
    def get_column_values(field_mapped_if_names, values, decimal_places):
        column_values = []
        for field in field_mapped_if_names:
            if field in values._labels:
                value = values[field]
                if isinstance(value, float):
                    decimal_formating = "{0:.%sf}" %decimal_places
                    value = decimal_formating.format(value)
                column_values.append(value)
            else:
                column_values.append("")
        return column_values

    def get_mapped_dict(self, dataset):
        metadata = self.get_metadata()[dataset]
        field_names = [f.field_name for f in metadata.fields]
        display_names = [f.display_name for f in metadata.fields]
        mapped_dict = OrderedDict(zip(field_names, display_names))
        return mapped_dict

    # def get_special_field_value(self, permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session):
    #     if display_name == 'PermitNumber':
    #         value = self.get_permit_number(sa_session, permit_logid)
    #     return value
    #entity_area1

    def get_special_field_value(self, permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session):
        if display_name == 'PermitNumber':
            value = self.get_permit_number(sa_session, permit_logid)
            logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ display_name PermitNumber = %s" % value)
        if field_name == 'restricted_area':
            value = self.get_area_hierarchy_value(value)
            logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ field_name area_hierarchy = %s" % value)
        if field_name == 'entity_area1':
            value = self.get_area_hierarchy_value(value)
            logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ field_name area_hierarchy = %s" % value)
        return value


    def get_full_name_and_signature(self, snapshot, section_name, sa_session):
        user_and_date = self.get_section_submission_user_and_date(snapshot, section_name)
        if user_and_date:
            username = user_and_date.SubmittedBy
            fullname = self.get_user_fullname_from_username(username, sa_session)
            signature = self.get_signature_from_user_username(username, sa_session)
            return fullname, signature
        else:
            return None, None



    def get_section_approvals_user(self,form_data_snapshot, section_title, sa_session, approval_spec_label=None):
        logging.debug("***************************************************** Getting data for '%s' Section" % section_title)
        section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'Approvals'])
        logging.debug(section_elements)
        approval_user = None
        approval_timestamp = None
        if section_elements:
            for section in section_elements:
                logging.debug("***************************************************** Found section '%s'" % section[0])
                if section[0] == section_title:
                    logging.debug("***************************************************** Current Section matches section we are looking for")
                    if approval_spec_label:
                        logging.debug("***************************************************** Now to find the requested approval; looking for %s approval" % approval_spec_label)
                    else:
                        logging.debug("***************************************************** Now to find the requested approval; looking for an empty/unspecified approval")
                    if (section[1] != []) and (section[1] != None):
                        for approver in section[1]:
                            if approver['approvalSpecLabel'] == approval_spec_label:
                                approval_user = approver['approvalUser']
                                approval_timestamp = approver['approvalTimestamp']
                                logging.debug("***************************************************** Section Title = '%s'" % section[0])
                                logging.debug("***************************************************** Section approvalUser = '%s'" % approval_user)
                                logging.debug("***************************************************** Section approvalTimestamp = '%s'" % approval_timestamp)
                        if approval_user:
                            fullname = self.get_user_fullname_from_username(approval_user, sa_session)
                            if fullname:
                                logging.debug("***************************************************** Section approvalUser Fullname  = '%s'" % fullname)
                                return fullname, approval_timestamp
                            else:
                                logging.debug("***************************************************** Section approvalUser does not have a Fullname, user username instead")
                                return approval_user, approval_timestamp
                        else:
                            if approval_spec_label:
                                logging.debug("***************************************************** Section does not have a %s Approval" % approval_spec_label)
                            else:
                                logging.debug("***************************************************** Section does not have an Approval with an empty Spec Label")
                            return None, None
        return None, None

    # def get_section_approvals_user(self,form_data_snapshot, section_title, sa_session, approval_spec_label=None):
    #     logging.debug("***************************************************** Getting data for '%s' Section" % section_title)
    #     section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'Approvals'])
    #     logging.debug(section_elements)
    #     approval_user = None
    #     approval_timestamp = None
    #     if section_elements:
    #         for section in section_elements:
    #             logging.debug("***************************************************** Found section '%s'" % section[0])
    #             if section[0] == section_title:
    #                 logging.debug("***************************************************** Current Section matches section we are looking for")
    #                 if approval_spec_label:
    #                     logging.debug("***************************************************** Now to find the requested approval; looking for %s approval" % approval_spec_label)
    #                 else:
    #                     logging.debug("***************************************************** Now to find the requested approval; looking for an empty/unspecified approval")
    #                 for approver in section[1]:
    #                     if approver['approvalSpecLabel'] == approval_spec_label:
    #                         approval_user = approver['approvalUser']
    #                         approval_timestamp = approver['approvalTimestamp']
    #                         logging.debug("***************************************************** Section Title = '%s'" % section[0])
    #                         logging.debug("***************************************************** Section approvalUser = '%s'" % approval_user)
    #                         logging.debug("***************************************************** Section approvalTimestamp = '%s'" % approval_timestamp)
    #                 if approval_user:
    #                     fullname = self.get_user_fullname_from_username(approval_user, sa_session)
    #                     if fullname:
    #                         logging.debug("***************************************************** Section approvalUser Fullname  = '%s'" % fullname)
    #                         return fullname, approval_timestamp
    #                     else:
    #                         logging.debug("***************************************************** Section approvalUser does not have a Fullname, user username instead")
    #                         return approval_user, approval_timestamp
    #                 else:
    #                     if approval_spec_label:
    #                         logging.debug("***************************************************** Section does not have a %s Approval" % approval_spec_label)
    #                     else:
    #                         logging.debug("***************************************************** Section does not have an Approval with an empty Spec Label")
    #                     return None, None
    #     return None, None
    #
    # def get_section_approvals_user(self,form_data_snapshot, section_title, sa_session):
    #     Section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'Approvals'])
    #     logging.debug('***************************************************** Section_elements : %s' % Section_elements)
    #     logging.debug('++++++++++++++++++++++++++ Section_elements type     *** %s' % type(Section_elements))#list
    #     logging.debug('++++++++++++++++++++++++++ section_title.index     *** %d' % Section_elements.index(section_title))
    #     for i in Section_elements:
    #         logging.debug('++++++++++++++++++++++++++ i type     *** %s' % type(i))
    #         logging.debug('++++++++++++++++++++++++++ i[0]     *** %s' % i[0])
    #         logging.debug('++++++++++++++++++++++++++ section_title     *** %s' % section_title)
    #         if i == section_title:
    #             approval_user = i[1]
    #             logging.debug('***************************************************** i[0], %s' % i[0])
    #             logging.debug('***************************************************** i[1], %s' % i[1])
    #             if (approval_user != []) and (approval_user != None):
    #                 approval_User = approval_user[0]
    #                 approvalTimestamp = approval_User['approvalTimestamp']
    #                 approvalUser = approval_User['approvalUser']
    #                 username = approvalUser
    #                 fullname = self.get_user_fullname_from_username(username, sa_session)
    #                 logging.debug('***************************************************** fullname  %s' % fullname)
    #                 logging.debug('***************************************************** approval Timestamp, %s' % approvalTimestamp)
    #                 return fullname , approvalTimestamp
    #             else:
    #                 return None, None
    #         return None, None



    def get_full_name_and_datetime(self, snapshot, section_name, sa_session):
        user_and_date = self.get_section_submission_user_and_date(snapshot, section_name)
        if user_and_date:
            username = user_and_date.SubmittedBy
            fullname = self.get_user_fullname_from_username(username, sa_session)
            datetime = user_and_date.SubmittedAt
            return fullname, datetime
        else:
            return None, None


    def get_header_row(self, dataset):
        mapped_dict = self.get_mapped_dict(dataset)
        # Populate header row
        dataset = [mapped_dict.keys()]
        return dataset

    def get_dataset_field_values(self, permit_logid, snapshot, dataset_name, sa_session, use_display_value=True):
        mapped_dict = self.get_mapped_dict(dataset_name)
        # Populate header row
        dataset = self.get_header_row(dataset_name)
        if use_display_value:
            industraform_values = snapshot.query(mapped_dict.values(), default_element_attribute='DisplayValue')
        else:
            industraform_values = snapshot.query(mapped_dict.values())
        column_values = []
        for field_name, display_name in iter(mapped_dict.items()):
            if display_name in industraform_values._labels:
                value = Export.render_value_for_birt(field_name, industraform_values[display_name], sa_session)
                value = self.get_special_field_value(permit_logid, field_name, display_name, value, dataset_name, industraform_values, snapshot, sa_session)
                column_values.append(value)
            else:
                column_values.append("")
        dataset.append(column_values)
        return dataset

    def get_linked_certificates(self, permit_logid, sa_session):
        logging.info("************************************************************************************* permit_logid %s" % permit_logid)
        required_certificates = sa_session.query(self.permit_logclass.required_certificates).filter_by(logid=permit_logid).first()
        logging.debug("************************************************************************************* required_certificates = %s" % required_certificates)
        # if not required_certificates == None:
        if required_certificates[0]:
            logging.debug("************************************************************************************* if required_certificates = %s" % required_certificates[0])
            required_certificates = required_certificates.required_certificates.strip(',').split(',')
            logging.info("I have found %d certificates" % len(required_certificates))

            certificates = sa_session.query(
                 self.certificate_logclass.logid, self.certificate_logclass.logdatetime, self.certificate_logclass.certificate_no,
                 self.permit_forms_logclass.logid,
                 self.sf_form_register_logclass.form_name)\
                .filter(self.certificate_logclass.logid.in_(required_certificates)) \
                .join(self.permit_forms_logclass, self.permit_forms_logclass.logid == self.certificate_logclass.certificate_type) \
                .join(self.sf_form_register_logclass,self.sf_form_register_logclass.logid == self.permit_forms_logclass.form_register_logid) \
                .order_by(self.certificate_logclass.logdatetime.desc())\
                .all()

            cert_types_found = []
            certificates_found_dict = {}
            for cert in certificates:
                logging.info("I have found a %s certificate, no %s" % (cert.form_name, cert.certificate_no))
                if cert.form_name in self.certificates_required.keys() and cert.form_name not in cert_types_found:
                    logging.info("Adding %s to cert_types_found" % cert.form_name)
                    cert_types_found.append(cert.form_name)
                if self.certificates_required[cert.form_name] in certificates_found_dict:
                    certificates_found_dict[self.certificates_required[cert.form_name]] += " , %s" % cert.certificate_no
                else:
                    certificates_found_dict[self.certificates_required[cert.form_name]] = cert.certificate_no
            logging.info("Returning list - %s" % certificates_found_dict)
        else:
            logging.debug("************************************************************************************* else required_certificates = %s" )
            certificates_found_dict = {}
        return certificates_found_dict


    # def print_approvals_user(self, Section_title, form_data_snapshot, sa_session):
    #     approvals_details = self.get_section_approvals(form_data_snapshot, Section_title)
    #     logging.debug('---------->>>>>>>>>><<<<<<<<<----------  approvals_details :  %s' % approvals_details)
    #     if approvals_details != [None,None] :
    #         username = approvals_details[0]
    #         personnel_rc = Alchemy.find_recordclass("personnel")
    #         personnel_record = sa_session.query(personnel_rc).filter_by(j5username=username).first()
    #         if personnel_record:
    #             logging.debug('---------->>>>>>>>>><<<<<<<<<----------  lastname %s'     % personnel_record.lastname)
    #             logging.debug('---------->>>>>>>>>><<<<<<<<<----------  Approvals @ %s'  % approvals_details[1])


    # def get_section_approvals(self, form_data_snapshot, section_title):
    #     Section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'Approvals'])
    #     logging.debug('***************************************************** Section_elements, %s' % Section_elements)
    #     for i in Section_elements:
    #         if i[0] == section_title:
    #             approval_user = i[1]
    #             if (approval_user != []) and (approval_user != None):
    #                 approval_User = approval_user[0]
    #                 approvalTimestamp = approval_User['approvalTimestamp']
    #                 approvalUser = approval_User['approvalUser']
    #                 returndata = []
    #                 returndata.append(approvalUser)
    #                 returndata.append(approvalTimestamp)
    #                 return (returndata)
    #             else:
    #                 return ([None, None])
    #         return ([None, None])



    def get_form_snapshot(self, sa_session, permit_logid):
        permit_record = sa_session.query(self.permit_logclass).filter_by(logid=permit_logid).first()
        form = get_logbook_linked_forms(permit_record)
        if form:
            return self.get_industraform_snapshot(form[0])




    @staticmethod
    def get_area_hierarchy_value(area_list_str):
        if not area_list_str:
            return
        value = area_list_str.replace("u'", "").replace("'", " ").replace(",", "  > ").strip("[").strip("]")
        logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  get_area_hierarchy_value = %s" % value)
        return value

    @staticmethod
    def get_industraform_snapshot(form):
        return form.get_form_data_snapshot()

    @staticmethod
    def get_section_submission_user_and_date(form_data_snapshot, section_title):
        section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'SubmittedBy', 'SubmittedAt'])
        logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  get_section_submission_user_and_date  = %s" % section_elements)
        for e in section_elements:
            if e.Title == section_title:
                return e
        return None





    @staticmethod
    def get_user_fullname_from_username(username, sa_session):
        personnel_rc = Alchemy.find_recordclass("personnel")
        personnel_record = sa_session.query(personnel_rc).filter_by(j5username=username).first()
        if personnel_record:
            return personnel_record.lastname
