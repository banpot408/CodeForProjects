from dateutil import relativedelta
from j5.Database import Alchemy
from j5.IndustraForms.api import get_logbook_linked_forms
from j5.IndustraForms import beta_api_230
from j5.OS import datetime_tz
from j5.PermitToWork.PermitToWork import CertificatesMixin
from j5.PermitToWork.PermitToWork import PermitsMixin
from j5.PermitToWork import PermitToWork
from j5.Web.Server import RequestStack
from sjsoft.Library import RegisterWorkflow
from j5.PermitToWork.PermitToWork import PermitToWorkLogPage # For Edit Summary Plotplan
import sqlalchemy
import logging

class CustomPermitToWorkLogPage(PermitToWorkLogPage):
    def schematic_summary_fields(self):
        return ['permit_no','valid_start', 'valid_end', 'description_pttgc', 'status' , 'prepared_by']


class CustomCertificatesMixin(CertificatesMixin, RegisterWorkflow.RegisterWorkflowMixin):
    
    workflow_filename = "certificates.workflow"

    def before_session_insert(self, sa_session):
        CertificatesMixin.before_session_insert(self, sa_session)
        self.set_validity_fields()
        self.set_15_day_notification_field()
        self.section_count = 0
        return sqlalchemy.orm.EXT_CONTINUE

    def before_session_update(self, sa_session):
        
        committed_state = self.get_committed_state(['status','valid_start','valid_end'])
        logging.critical('------------------------------------------%s' % committed_state )
        if self.status != committed_state['status']:
            self.status_changed(sa_session, committed_state)
            logging.critical('-------------------------------------------self.status_changed(sa_session, committed_state)')
        if self.valid_end != committed_state['valid_end']:
            self.set_validity_fields()
            logging.critical('-------------------------------------------self.set_validity_fields()')
        if self.valid_start != committed_state['valid_start']:
            self.set_15_day_notification_field()
            logging.critical('-------------------------------------------self.set_15_day_notification_field()')
        CertificatesMixin.before_session_update(self, sa_session)
        logging.critical('-------------------------------------------CertificatesMixin.before_session_update(self, sa_session)')
        return sqlalchemy.orm.EXT_CONTINUE
    
    def set_validity_fields(self):
        self.valid_end_minus_1 = self.valid_end - relativedelta.relativedelta(days=1)            
        self.valid_end_plus_1 = self.valid_end + relativedelta.relativedelta(days=1)
        self.valid_minus_1_email_status = 'Not Sent'
        self.valid_plus_1_email_status = 'Not Sent'

    def set_15_day_notification_field(self):
        if not self.notification_date_15_day:
            self.notification_date_15_day = self.valid_start + relativedelta.relativedelta(days=15)
        while(self.notification_date_15_day < datetime_tz.datetime_tz.now()):
            self.notification_date_15_day += relativedelta.relativedelta(days=15)


    def send_15_day_notification(self, sa_session):
        forms = self.get_industraforms()
        if forms:
            nemail_body = self.get_url_data(forms)
            logging.critical('+++++++++++++++++++++++++++++++++++++++++++++ Runing in send_15_day_notification Sub Program : email_type = %s certificate_no = %s ' % (email_type, self.certificate_no))
            delta = datetime_tz.datetime_tz.now() - self.valid_start

            job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
            job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

            technical_approver_name = self.get_industraform_data(forms, ['TCA_Name'])
            technical_approver_mail = self.get_industraform_data(forms, ['TCA_Mail'])

            Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

            if technical_approver_name[0] and technical_approver_mail[0]:
                if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                    email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s 15 day warning' % self.certificate_no
                    email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (
                            self.certificate_no, delta.days)
                    email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                    email_body += nemail_body
                    self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                else:
                    email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (
                            self.certificate_no, delta.days)
                    email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s 15 day warning' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                    email_body += nemail_body
                    self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')

            if job_owner_name[0] and job_owner_mail[0]:
                if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                    email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s 15 day warning' % self.certificate_no
                    email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (
                            self.certificate_no, delta.days)
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                else:
                    email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (
                            self.certificate_no, delta.days)
                    email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s 15 day warning' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

            self.set_15_day_notification_field()



            # if Scaffolding_Height_over_21_Meters[0] == 'Yes':
            #     email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (self.certificate_no, delta.days)
            #     email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s 15 day warning' % self.certificate_no
            #     logging_detail = 'groups.technical_approvers scaffolding height over 21 meters Specific work permit 15 day warning'
            # else:
            #     email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> has been open for %d days. <br/><br/>Another warning email will be sent in 15 days time, unless the certificate is closed/complete' % (self.certificate_no, delta.days)
            #     email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s 15 day warning' % self.certificate_no
            #     logging_detail = 'groups.technical_approvers scaffolding Specific work permit 15 day warning'
            # self.send_emails(sa_session, technical_approvers, email_body, nemail_body, email_subject, logging_detail)


    def send_scaffolding_warning(self, sa_session, email_type):
        forms = self.get_industraforms()
        if forms:
            nemail_body = self.get_url_data(forms)
            logging.critical('+++++++++++++++++++++++++++++++++++++++++++++ Runing in send_scaffolding_warning Sub Program : email_type = %s certificate_no = %s ' % (email_type, self.certificate_no))
            job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
            job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
            technical_approver_name = self.get_industraform_data(forms, ['TCA_Name'])
            technical_approver_mail = self.get_industraform_data(forms, ['TCA_Mail'])
            Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

            if email_type == 1:

                if technical_approver_name[0] and technical_approver_mail[0]:
                    if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                        email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
                        email_body = 'Please note that Scaffolding height over 21 meters specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                        email_body += nemail_body
                        self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                    else:
                        email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s validity will end soon' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                        email_body += nemail_body
                        self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                if job_owner_name[0] and job_owner_mail[0]:
                    if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                        email_body = 'Please note that Scaffolding height over 21 meters specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_subject = 'Mail To Job Owners - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                    else:
                        email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_subject = 'Mail To Job Owners - Scaffolding Specific work permit %s validity will end soon' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

        else :

            if technical_approver_name[0] and technical_approver_mail[0]:
                if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                    email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
                    email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                    email_body += nemail_body
                    self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                else:
                    email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s validity has ended' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                    email_body += nemail_body
                    self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')

            if job_owner_name[0] and job_owner_mail[0]:
                if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                    email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_subject = 'Mail To Job Owners - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                else:
                    email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_subject = 'Mail To Job Owners - Scaffolding Specific work permit %s validity has ended' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

        if email_type == 1:
            self.valid_minus_1_email_status = 'Sent'
        else:
            self.valid_plus_1_email_status = 'Sent'





        #     Team_Select_2 = self.get_industraform_data(forms, ['Choice62'])
        #     Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])
        #     if Team_Select_2 and Team_Select_2[0]:
        #         area5_name, area5_desc, area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_banpot(sa_session, Team_Select_2[0])
        #     else:
        #         area5_name, area5_desc, area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_banpot(sa_session, None)
        #     #Get the email recipients
        #     job_owner_profiles = self.get_group_area_profiles_banpot(sa_session, 'groups.job_owner', area1_name, area2_name, area2_desc, area3_name, area3_desc)
        #     technical_approval_profiles = self.get_group_area_profiles_banpot(sa_session, 'groups.technical_approval', area1_name, area2_name, area2_desc, area3_name, area3_desc)
        #     job_owners = self.get_users_with_profiles_banpot(sa_session, job_owner_profiles)
        #     technical_approvers = self.get_users_with_profiles_banpot(sa_session, technical_approval_profiles)
        #     #Prepare and Send the emails
        #     if email_type == 1:
        #         if Scaffolding_Height_over_21_Meters[0] == 'Yes':
        #             email_body = 'Please note that Scaffolding height over 21 meters specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
        #             jo_email_subject = 'Mail To Job Owners - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
        #             jo_logging_detail = 'groups.job_owners Scaffolding height over 21 meters Specific work permit expiring soon'
        #             ta_email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s validity will end soon' % self.certificate_no
        #             ta_logging_detail = 'groups.technical_approvers Scaffolding height over 21 meters Specific work permit expiring soon'
        #         else:
        #             email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
        #             jo_email_subject = 'Mail To Job Owners - Scaffolding Specific work permit %s validity will end soon' % self.certificate_no
        #             jo_logging_detail = 'groups.job_owners Scaffolding Specific work permit expiring soon'
        #             ta_email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s validity will end soon' % self.certificate_no
        #             ta_logging_detail = 'groups.technical_approvers Scaffolding Specific work permit expiring soon'


        #     else:
        #         if Scaffolding_Height_over_21_Meters[0] == 'Yes':
        #             email_body = 'Please note that Scaffolding height over 21 meters Specific work permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
        #             jo_email_subject = 'Mail To Job Owners - Scaffolding height over 21 meters Specific work permit %s validity has ended' % self.certificate_no
        #             jo_logging_detail = 'groups.job_owners Scaffolding height over 21 meters Specific work permit expired'
        #             ta_email_subject = 'Mail To Technical Approvers - Scaffolding height over 21 meters Specific work permit %s validity has ended' % self.certificate_no
        #             ta_logging_detail = 'groups.technical_approvers Scaffolding height over 21 meters Specific work permit expired'
        #         else:
        #             email_body = 'Please note that Scaffolding Specific work permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
        #             jo_email_subject = 'Mail To Job Owners - Scaffolding Specific work permit %s validity has ended' % self.certificate_no
        #             jo_logging_detail = 'groups.job_owners Scaffolding Specific work permit expired'
        #             ta_email_subject = 'Mail To Technical Approvers - Scaffolding Specific work permit %s validity has ended' % self.certificate_no
        #             ta_logging_detail = 'groups.technical_approvers Scaffolding Specific work permit expired'
        #
        #     self.send_emails(sa_session, job_owners, email_body, nemail_body, jo_email_subject, jo_logging_detail)
        #     self.send_emails(sa_session, technical_approvers, email_body, nemail_body, ta_email_subject, ta_logging_detail)
        # if email_type == 1:
        #     self.valid_minus_1_email_status = 'Sent'
        # else:
        #     self.valid_plus_1_email_status = 'Sent'



    def send_confine_warning(self, sa_session, email_type):
        forms = self.get_industraforms()
        if forms:
            nemail_body = self.get_url_data(forms)
            logging.critical('+++++++++++++++++++++++++++++++++++++++++++++ Runing in send_confine_warning Sub Program : email_type = %s certificate_no = %s ' %(email_type , self.certificate_no))
            Team_Select_2 = self.get_industraform_data(forms, ['area1'])

            job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
            job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

            if job_owner_name[0] and job_owner_mail[0] :
                if email_type == 1:
                    email_subject = 'Mail To Permit Issuer Confine - Confine Certificate %s validity will end soon' % self.certificate_no
                    email_body = 'Please note that Confine Certificate number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                else:
                    email_subject = 'Mail To Permit Issuer Confine - Confine Certificate %s validity will end soon' % self.certificate_no
                    email_body = 'Please note that Confine Certificate number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

            if Team_Select_2 and Team_Select_2[0]:
                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                       'groups.permit_issuer_confine',
                                                                                       area1_name,
                                                                                       area2_name,
                                                                                       area2_desc,
                                                                                       area3_name,
                                                                                       area3_desc,
                                                                                       area4_name,
                                                                                       area4_desc)
                users = self.get_users_with_profiles(sa_session, profiles)
                logging.critical('-------------------------------------------------------users         = %s' % users)
                if users:
                    if email_type == 1:
                        email_body = 'Please note that Confine Certificate number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_subject = 'Mail To Permit Issuer Confine - Confine Certificate %s validity will end soon' % self.certificate_no
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_confine group')
                    else:
                        email_body = 'Please note that Confine Certificate number <b> # %s </b> has expired.  It was valid until %s.' % (self.certificate_no, self.format_date(self.valid_end))
                        email_subject = 'Mail To Permit Issuer Confine - Confine Certificate %s validity will end soon' % self.certificate_no
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_confine group')

            if email_type == 1:
                self.valid_minus_1_email_status = 'Sent'
            else:
                self.valid_plus_1_email_status = 'Sent'


            

    def format_date(self, date):
        if date:
            return date.astimezone(datetime_tz.localtz()).strftime('%d-%m-%Y, %H:%M')
        else:
            return 'Not specified'

    def get_area_data_form_areahierarchy_4_depth(self, sa_session, descriptions):

        area_desc_dict = {}
        area_name_dict = {}

        area_fields = ['area1', 'area2', 'area3', 'area4']
        for area in area_fields:
            area_desc_dict[area] = ''
            area_name_dict[area] = None

        depth = 1
        area_rc = Alchemy.find_recordclass('area_hierarchy')
        for description in descriptions:
            area_desc_dict['area'+str(depth)] = description
            if area_desc_dict['area'+str(depth)]:
                area = sa_session.query(area_rc).filter_by(depth=depth, description=area_desc_dict['area'+str(depth)], deleted=0).first()
                if not area:
                    logging.critical("Can't find a Level %d Area field that matches the one specified - %s" % (depth, area_desc_dict['area'+str(depth)]))
                    break
                else:
                    area_name_dict['area'+str(depth)] = area.name
            depth += 1

        return area_name_dict['area4'], area_desc_dict['area4'], area_name_dict['area3'], area_desc_dict['area3'], area_name_dict['area2'], area_desc_dict['area2'] ,area_name_dict['area1'], area_desc_dict['area1']

    def get_group_area_profiles_form_areahierarchy_4_depth(self, sa_session, groupname, area1_name, area2_name, area2_desc, area3_name, area3_desc, area4_name, area4_desc):
        profile_rc = Alchemy.find_recordclass('profile')

        if area4_name:
    #        logging.critical('------------------------Getting %s Profiles for Area1: %s, Area2: %s, Area3: %s, Area4: %s' % (groupname, area1_desc, area2_desc, area3_desc, area4_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%'),
                                                           profile_rc.area3.like('%' + area3_name + '%'),
                                                           profile_rc.area4.like('%' + area4_name + '%')).all()
        elif area3_name:
            logging.critical('------------------------Getting %s Profiles for Area1: PTTGC4, Area2: %s, Area3: %s' % (groupname, area2_desc, area3_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%'),
                                                           profile_rc.area3.like('%' + area3_name + '%')).all()
        elif area2_name:
            logging.critical('------------------------Getting %s Profiles for Area1: PTTGC4, Area2: %s, Area3: None' % (groupname, area2_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%')).all()
        else:
            logging.critical('------------------------Getting %s Profiles for all areas' % (groupname))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname).all()

        if not profiles:
            logging.critical('------------------------No profiles found for %s' % groupname)
        return profiles

    def get_users_with_profiles(self, sa_session, profiles):
        ss_users = set()
        personnel_rc = Alchemy.find_recordclass('personnel')
        for profile in profiles:
            if profile.description:
                logging.critical('------------------------Finding users who can fulfil profile %s' % profile.description)
            profile_users = sa_session.query(personnel_rc).filter(sqlalchemy.or_(personnel_rc.profile == profile.logid, personnel_rc.alt_profiles.like('%' + profile.logid + '%'))).all()
            for profile_user in profile_users:
                ss_users.add(profile_user.j5username)
        return ss_users



    # def send_emails(self, sa_session, users, email_body, nemail_body, email_subject, logging_detail=None):
    #     personnel_rc = Alchemy.find_recordclass('personnel')
    #     if users:
    #         recipients = sa_session.query(personnel_rc).filter(personnel_rc.j5username.in_(users)).all()
    #         email_body += nemail_body
    #     else:
    #         if logging_detail:
    #             logging.critical('------------------------No users provided for %s email' % logging_detail)
    #         recipients = []
    #     for recipient in recipients:
    #         if recipient and recipient.email:
    #             if logging_detail:
    #                 logging.critical('------------------------Sending %s email to %s' % (logging_detail, recipient.j5username))
    #             else:
    #                 logging.critical('------------------------Sending email to %s' % (recipient))
    #             email_greeting = 'Dear %s<br/><br/>' % recipient.lastname
    #             self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')
    #             if logging_detail:
    #                 logging.critical('------------------------Sent %s email to %s' % (logging_detail, recipient.email))
    #             else:
    #                 logging.critical('------------------------Sent email to %s' % (recipient))


    def send_emails(self, sa_session, users, email_body, nemail_body, email_subject, logging_detail=None):
        personnel_rc = Alchemy.find_recordclass('personnel')
        if users:
            recipients = sa_session.query(personnel_rc).filter(personnel_rc.j5username.in_(users)).all()
            email_body += nemail_body
        else:
            if logging_detail:
                logging.critical('------------------------No users provided for %s email' % logging_detail)
            recipients = []
        for recipient in recipients:
            if recipient and recipient.email:

                # logging.critical('****************************************************************************************************** recipient.email %s' % recipient.email)
                email_list = []
                email_user = recipient.email
                email_list.append(email_user)
                # logging.critical('****************************************************************************************************** recipient len  %s' % len(email_list)) #join(lists)
                # logging.critical('****************************************************************************************************** recipient type %s' % type(email_list))  # join(lists)  str(mylist)
                # logging.critical('****************************************************************************************************** recipient      %s' % email_list)  # join(lists)
                # logging.critical('****************************************************************************************************** recipient      %s' % email_list)  # join(lists)

                if logging_detail:
                    logging.critical('------------------------Sending %s email to %s' % (logging_detail, recipient.j5username))
                else:
                    logging.critical('------------------------Sending email to %s' % (recipient))
                email_greeting = 'Dear %s<br/><br/>' % recipient.lastname
                self.emailer.send(email_list, email_subject, email_greeting + email_body, contenttype='text/html')
                # self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')

                if logging_detail:
                    logging.critical('------------------------Sent %s email to %s' % (logging_detail, recipient.email))
                else:
                    logging.critical('------------------------Sent email to %s' % (recipient))


    
    def status_changed(self, sa_session, committed_state):

        certificate_type = self.get_certificate_type(sa_session)
        logging.critical('---')
        logging.critical('---')
        logging.critical('certificate_type = %s' % certificate_type)
        logging.critical('---')


        if certificate_type == 'Scaffolding':        # Scaffolding
            logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Scaffolding')
            forms = self.get_industraforms()

                        
            if forms:		
                section_1_gate_in_name  = 'Permit Request (1/6)'
                section_1_gate_out_name = 'Permit Request (2/6)'
                section_2_gate_in_name  = 'Permit Request (3/6)'
                section_2_gate_out_name = 'Permit Request (4/6)'
                section_3_gate_in_name  = 'Permit Request (5/6)'
                section_3_gate_out_name = 'Permit Request (6/6)'
                section_4_gate_in_name  = 'Inspection and Approval (1/6)'
                section_4_gate_out_name = 'Inspection and Approval (2/6)'
                section_5_gate_in_name  = 'Inspection and Approval (3/6)'
                section_5_gate_out_name = 'Inspection and Approval (4/6)'
                section_6_gate_in_name  = 'Inspection and Approval (5/6)'
                section_6_gate_out_name = 'Inspection and Approval (6/6)'
                section_7_gate_in_name  = 'Working'
                section_7_gate_out_name = 'Renewal of Specific (1/3)'
                section_8_gate_in_name  = 'Renewal of Specific (2/3)'
                section_8_gate_out_name = 'Renewal of Specific (3/3)'
                section_9_gate_in_name  = 'Dismantling (1/2)'
                section_9_gate_out_name = 'Dismantling (2/2)'  

                nemail_body = self.get_url_data(forms)

#Section 1 -------------------------------------------------------------------------------------------# Section 1 Technical Approver review Basic Data
                if committed_state['status'] in (None, '', section_1_gate_in_name) and  self.status == section_1_gate_out_name :
                    self.section_count = 1
                    job_owner_name  = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail  = self.get_industraform_data(forms, ['JON_Mail'])
                    eng_name        = self.get_industraform_data(forms, ['Eng_Name'])
                    eng_mail        = self.get_industraform_data(forms, ['Eng_Mail'])
                    technical_approver_name        = self.get_industraform_data(forms, ['TCA_Name'])
                    technical_approver_mail        = self.get_industraform_data(forms, ['TCA_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

                    if technical_approver_name[0] and technical_approver_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section permit request has been submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                            email_body += nemail_body
                            self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section permit request has been submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                            email_body += nemail_body
                            self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section permit request has been submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section permit request has been submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                        if eng_name[0] and eng_mail[0]:
                            email_subject = '<submitted><%s><scaffolding>Section permit request has been submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % eng_name
                            email_body += nemail_body
                            self.emailer.send(eng_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 1  Reject-------------------------------------------------------------------------------------------# Section 1 Technical Approver review Basic Data

                if committed_state['status'] in (None, '', section_1_gate_out_name) and  self.status == section_1_gate_in_name and  self.section_count == 1 :
                    self.section_count = 0
                    Scaffolding_Installer_Request_User_name = self.get_industraform_data(forms, ['SCRU_Name'])
                    Scaffolding_Installer_Request_User_mail = self.get_industraform_data(forms, ['SCRU_Mail'])
                    Scaffolding_Installer_Request_User_tel  = self.get_industraform_data(forms, ['SCRU_Tel'])
                    contractor_name = self.get_industraform_data(forms, ['CTT_Name'])
                    contractor_mail = self.get_industraform_data(forms, ['CTT_Mail'])
                    contractor_tel  = self.get_industraform_data(forms, ['CTT_Tel'])
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])
                    eng_name        = self.get_industraform_data(forms, ['Eng_Name'])
                    eng_mail        = self.get_industraform_data(forms, ['Eng_Mail'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            Scaffolding_Installer_Request_User_data = '<br/>Scaffolding Installer Request User Name : %s <br/>Scaffolding Installer Request User Mail : %s <br/>Scaffolding Installer Request User Tel : %s' % (Scaffolding_Installer_Request_User_name[0], Scaffolding_Installer_Request_User_mail[0],Scaffolding_Installer_Request_User_tel[0])
                            email_body += nemail_body
                            email_body += Scaffolding_Installer_Request_User_data
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            Scaffolding_Installer_Request_User_data = '<br/>Scaffolding Installer Request User Name : %s <br/>Scaffolding Installer Request User Mail : %s <br/>Scaffolding Installer Request User Tel : %s' % (Scaffolding_Installer_Request_User_name[0], Scaffolding_Installer_Request_User_mail[0],Scaffolding_Installer_Request_User_tel[0])
                            email_body += nemail_body
                            email_body += Scaffolding_Installer_Request_User_data
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if Scaffolding_Installer_Request_User_name[0] and Scaffolding_Installer_Request_User_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % Scaffolding_Installer_Request_User_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(Scaffolding_Installer_Request_User_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % Scaffolding_Installer_Request_User_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(Scaffolding_Installer_Request_User_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if contractor_name[0] and contractor_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if eng_name[0] and eng_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % eng_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(eng_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><scaffolding>Section permit request has been reject' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section permit request has been reject' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % eng_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(eng_mail, email_subject, email_greeting + email_body, contenttype='text/html')


#Section 2 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 2 Scaffolding Height over 21 Meters

                if committed_state['status'] in (None, '', section_2_gate_in_name) and  self.status == section_2_gate_out_name :
                    self.section_count = 2
                    technical_approver_name        = self.get_industraform_data(forms, ['TCA_Name'])
                    technical_approver_mail        = self.get_industraform_data(forms, ['TCA_Mail'])

                    if technical_approver_name[0] and technical_approver_mail[0]:
                        email_subject = '<submitted><%s><scaffolding>Section scaffolding height over 21 Meters has been submitted' % self.certificate_no
                        email_body = 'Please note that Scaffolding height over 21 meters number <b> # %s </b> Section Scaffolding Height over 21 Meters has been Submitted' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                        email_body += nemail_body
                        self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 3 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 3 Technical Approver review Basic Data
                            
                if committed_state['status'] in (None, '', section_3_gate_in_name) and  self.status == section_3_gate_out_name :
                    self.section_count = 3
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section technical approver review basic Data has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section Technical Approver review Basic Data has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section technical approver review basic Data has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section Technical Approver review Basic Data has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 4 ------------------------------------------------------------------------------------------------------------------------------------------------# Section 4 After Subcontract build scaffloding and submit to Technical Approver
				  
                if committed_state['status'] in (None, '', section_4_gate_in_name) and  self.status == section_4_gate_out_name :
                    self.section_count = 4
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])
                    technical_approver_name        = self.get_industraform_data(forms, ['TCA_Name'])
                    technical_approver_mail        = self.get_industraform_data(forms, ['TCA_Mail'])

                    if technical_approver_name[0] and technical_approver_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section After Subcontract build scaffloding and submit to Technical Approver has been Submitted' % self.certificate_no
                            email_body =    'Please note that Scaffolding height over 21 meters number <b> # %s </b> Section After Subcontract build scaffloding and submit to Technical Approver has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section After Subcontract build scaffloding and submit to Technical Approver has been Submitted' % self.certificate_no
                            email_body =    'Please note that Scaffolding number <b> # %s </b> Section After Subcontract build scaffloding and submit to Technical Approver has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name

                        self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')


#Section 5-----------------------------------------------permit_issuer----------------------------------------------------------------------------------------------------------------------------------------# Section 5 Technical Approver Inspection                             
                            
                if committed_state['status'] in (None, '', section_5_gate_in_name) and  self.status == section_5_gate_out_name :
                    self.section_count = 5

#Section 6 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 6 Result of Permit                              
                            
                if committed_state['status'] in (None, '', section_6_gate_in_name) and  self.status == section_6_gate_out_name :
                    self.section_count = 6
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section Result of Permit has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section Result of Permit has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section Result of Permit has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section Result of Permit has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 7 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 7 Renew Date Request
                            
                if committed_state['status'] in (None, '', section_7_gate_in_name) and  self.status == section_7_gate_out_name :
                    self.section_count = 7
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])
                    technical_approver_name        = self.get_industraform_data(forms, ['TCA_Name'])
                    technical_approver_mail        = self.get_industraform_data(forms, ['TCA_Mail'])

                    if technical_approver_name[0] and technical_approver_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section Renew Date Request has been Submitted' % self.certificate_no
                            email_body =    'Please note that Scaffolding height over 21 meters number <b> # %s </b> Section Renew Date Request has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section Renew Date Request has been Submitted' % self.certificate_no
                            email_body =    'Please note that Scaffolding number <b> # %s </b> Section Renew Date Request has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % technical_approver_name

                        self.emailer.send(technical_approver_mail, email_subject, email_greeting + email_body, contenttype='text/html')
#Section 8 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 8 Renew Date

                
                if committed_state['status'] in (None, '', section_8_gate_in_name) and  self.status == section_8_gate_out_name:
                    self.section_count = 8
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section Renew Date has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section Renew Date has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section Renew Date has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section Renew Date has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
     
#Section 9 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 6 Renew Date
 
                if committed_state['status'] in (None, '', section_9_gate_in_name) and  self.status == section_9_gate_out_name :
                    self.section_count = 9
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Scaffolding_Height_over_21_Meters = self.get_industraform_data(forms, ['ChecklistItem19'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Scaffolding_Height_over_21_Meters[0] == 'Yes':
                            email_subject = '<submitted><%s><scaffolding>Section Dismantling has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding Height Over 21 Meters number <b> # %s </b> Section Dismantling has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><scaffolding>Section Dismantling has been Submitted' % self.certificate_no
                            email_body = 'Please note that Scaffolding number <b> # %s </b> Section Dismantling has been Submitted' % self.certificate_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#confine----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# Section 6 Dismantling

        if certificate_type == 'Confine': #Confine
            forms = self.get_industraforms()
            logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Confine')

            if forms:
                section_1_gate_in_name  = 'Permit Request (1/4)'
                section_1_gate_out_name = 'Permit Request (2/4)'
                section_2_gate_in_name  = 'Permit Request (3/4)'
                section_2_gate_out_name = 'Permit Request (4/4)'
                section_3_gate_in_name  = 'Permit Preparation (1/2)'
                section_3_gate_out_name = 'Permit Preparation (2/2)'
                section_4_gate_in_name  = 'Permit Approval (1/4)'
                section_4_gate_out_name = 'Permit Approval (2/4)'
                section_5_gate_in_name  = 'Permit Approval (3/4)'
                section_5_gate_out_name = 'Permit Approval (4/4)'
                section_6_gate_in_name  = 'Working'
                section_6_gate_out_name = 'Gas Test (While working)'
                section_7_gate_in_name  = 'Gas Test (While working)'
                section_7_gate_out_name = 'Renewal of Specific (1/3)'
                section_8_gate_in_name  = 'Renewal of Specific (2/3)'
                section_8_gate_out_name = 'Renewal of Specific (3/3)'
                section_9_gate_in_name  = 'Finished (1/2)'
                section_9_gate_out_name = 'Finished (2/2)'
                
                nemail_body = self.get_url_data(forms)
#                logging.critical('---')
#                logging.critical('---')
#                logging.critical('IF forms = TRUE')
#                logging.critical('get_url_data nemail_body = %s' %nemail_body)
#                logging.critical('section_count------------- %s' % self.section_count )
#                logging.critical('---')
                
#Section 1  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_1_gate_in_name) and  self.status == section_1_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 1 Submitted')
                    self.section_count = 1
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    logging.critical('------------------------ job_owner_name  %s' % job_owner_name)
                    logging.critical('------------------------ job_owner_mail  %s' % job_owner_mail)

                    if job_owner_name[0] and job_owner_mail[0]:
                        logging.critical('**************************************** section 1')
                        email_subject = '<submitted><%s><confine>Section permit request has been submitted' % self.certificate_no
                        email_body = 'Confine job number <b> # %s </b> Section permit request has been submitted' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                    
#Section 1  Reject-------------------------------------------------------------------------------------------# Section 1 Technical Approver review Basic Data

                if committed_state['status'] in (None, '', section_1_gate_out_name) and  self.status == section_1_gate_in_name and  self.section_count == 1 :
                    logging.critical('********************************************************************************** Confine section 1 Reject')
                    self.section_count = 0
                    contractor_name = self.get_industraform_data(forms, ['Text1'])
                    contractor_mail = self.get_industraform_data(forms, ['Text226'])
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    job_owner_tel = self.get_industraform_data(forms, ['Text234'])

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<reject><%s><confine>Section confine space control verify data has been reject' % self.certificate_no
                        email_body = 'Edit or contact job owner that confine number <b> # %s </b> Section confine space control verify data has been reject' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s <br/>job owner Tel : %s' % (
                            job_owner_name[0], job_owner_mail[0], job_owner_tel[0])
                        email_body += nemail_body
                        email_body += job_owner_data
                        self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        
#Section 2  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
           
                if committed_state['status'] in (None, '', section_2_gate_in_name) and  self.status == section_2_gate_out_name:
                    logging.critical('********************************************************************************** Confine section 2 Submitted')
                    self.section_count = 2
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    confine_verify = self.get_industraform_data(forms, ['ChecklistItem147'])
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    if confine_verify[0] == 'Yes':
                        if Team_Select_2 and Team_Select_2[0]:
                            area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                            profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                               'groups.permit_issuer_confine',
                                                                                               area1_name,
                                                                                               area2_name,
                                                                                               area2_desc,
                                                                                               area3_name,
                                                                                               area3_desc,
                                                                                               area4_name,
                                                                                               area4_desc)
                            users = self.get_users_with_profiles(sa_session, profiles)
                            logging.critical('-------------------------------------------------------users         = %s' % users)
                            if users:
                                email_subject = '<submitted><%s><confine>Section confine space control verify data has been Submitted' % self.certificate_no
                                email_body = 'Please note that Confine number <b> # %s </b> Section confine space control verify data has been Submitted' % self.certificate_no
                                email_greeting = 'Dear Permit Issuer,<br/><br/>'
                                self.send_emails(sa_session, users, email_greeting + email_body, nemail_body, email_subject, 'permit_issuer_confine group')
                    else:
                        email_subject = '<reject><%s><confine>Section confine space control verify data has been reject' % self.certificate_no
                        email_body = 'Confine job number <b> # %s </b> Section confine space control verify data has been submitted' % self.certificate_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                           
#Section 3  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      

                if committed_state['status'] in (None, '', section_3_gate_in_name) and  self.status == section_3_gate_out_name:
                    logging.critical('********************************************************************************** Confine section 3 Submitted')
                    self.section_count = 3
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])

                    if Team_Select_2 and Team_Select_2[0]:
                        area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                        profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                           'groups.confine_space_approver',
                                                                                           area1_name,
                                                                                           area2_name,
                                                                                           area2_desc,
                                                                                           area3_name,
                                                                                           area3_desc,
                                                                                           area4_name,
                                                                                           area4_desc)
                        users = self.get_users_with_profiles(sa_session, profiles)
                        logging.critical('-------------------------------------------------------users         = %s' % users)
                        if users:
                            email_subject = '<submitted><%s><confine>Section permit preparation has been Submitted' % self.certificate_no
                            email_body = 'Please note that Coldwork Job number <b> # %s </b> Section permit preparation has been Submitted' % self.certificate_no
                            self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'confine_space_approver group')

#Section 4  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      

                if committed_state['status'] in (None, '', section_4_gate_in_name) and  self.status == section_4_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 4 Submitted')
                    self.section_count = 4

#Section 5  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      

                if committed_state['status'] in (None, '', section_5_gate_in_name) and  self.status == section_5_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 5 Submitted')
                    self.section_count = 5
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<submitted><%s><confine>Section communicate with job owner has been submitted' % self.certificate_no
                    email_body = 'Please note that confine number <b> # %s </b> Section communicate with job owner has been submitted' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                            
#Section 6  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      

                if committed_state['status'] in (None, '', section_6_gate_in_name) and  self.status == section_6_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 6 Submitted')
                    self.section_count = 6

#Section 7  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      

                if committed_state['status'] in (None, '', section_7_gate_in_name) and  self.status == section_7_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 7 Submitted')
                    self.section_count = 7
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])

                    if Team_Select_2 and Team_Select_2[0]:
                        area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                        profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                           'groups.confine_space_approver',
                                                                                           area1_name,
                                                                                           area2_name,
                                                                                           area2_desc,
                                                                                           area3_name,
                                                                                           area3_desc,
                                                                                           area4_name,
                                                                                           area4_desc)
                        users = self.get_users_with_profiles(sa_session, profiles)
                        logging.critical('-------------------------------------------------------users         = %s' % users)
                        if users:
                            email_subject = '<submitted><%s><confine>Section permit reneval has been Submitted' % self.certificate_no
                            email_body = 'Please note that Coldwork Job number <b> # %s </b> Section permit reneval has been Submitted' % self.certificate_no
                            self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'confine_space_approver group')

#Section 8  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
                            
                if committed_state['status'] in (None, '', section_8_gate_in_name) and self.status == section_8_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 8 Submitted')
                    self.section_count = 8
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<submitted><%s><confine>Section permit reneval has been submitted' % self.certificate_no
                    email_body = 'Please note that confine number <b> # %s </b> Section permit reneval has been submitted' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 9  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_9_gate_in_name) and self.status == section_9_gate_out_name :
                    logging.critical('********************************************************************************** Confine section 9 Submitted')
                    self.section_count = 9
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<finished><%s><confine>Permit has been finished' % self.certificate_no
                    email_body = 'Please note that confine number <b> # %s </b> Section Permit Request has been Finished' % self.certificate_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#------------------------------------------------------------------------------------------------------------------------------------------------------                   

    def get_certificate_type(self, sa_session):
        rc = Alchemy.find_recordclass('permit_forms')
        form = sa_session.query(rc.title).filter(rc.logid == self.certificate_type).first()
        if form:
            return form.title
        return None

    def get_industraforms(self):
        return get_logbook_linked_forms(logbook_record=self)

    def get_industraform_data(self, forms, list_of_fields, value_type="DisplayValue"):
        data_dict = []
        if forms:
            form_data_snapshot = forms[0].get_form_data_snapshot()
            data_dict = form_data_snapshot.query(list_of_fields, default_element_attribute=value_type)
        return data_dict

    def get_section_submission_user_and_date(self, form_data_snapshot, Section_title):
        Section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'SubmittedBy', 'SubmittedAt'])
        for e in Section_elements:
            if e.Title == Section_title:
                return e
        return [None, None]

        # This Section checks the specified Section's for the submitter, looks them up in the personnel logbook and send them an email (if they have an email address)

    def send_submitter_email(self, Section_title, sa_session):
        forms = get_logbook_linked_forms(logbook_record=self)
        form_data_snapshot = forms[0].get_form_data_snapshot()
        submission_details = self.get_section_submission_user_and_date(form_data_snapshot, Section_title)

        if submission_details and submission_details['SubmittedBy']:
            rc = Alchemy.find_recordclass('personnel')
            recipient = sa_session.query(rc).filter(sqlalchemy.and_(rc.email != None, rc.email != '', rc.j5username == submission_details['SubmittedBy'])).first()
            if recipient:
                name = recipient.lastname if recipient.lastname else recipient.j5username
                email_subject = 'Email Notification for submitting Section %s of certificate # %s' % (Section_title, self.certificate_no)
                email_body = 'Thank you for submitting Section %s of certificate # %s' % (Section_title, self.certificate_no)
                email_greeting = 'Dear, %s<br/><br/>' % name
                self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')

    def send_submitter_email_url(self, Section_title, nemail_body, sa_session):
        forms = get_logbook_linked_forms(logbook_record=self)
        form_data_snapshot = forms[0].get_form_data_snapshot()
        submission_details = self.get_Section_submission_user_and_date(form_data_snapshot, Section_title)
        if submission_details and submission_details['SubmittedBy']:
            rc = Alchemy.find_recordclass('personnel')
            recipient = sa_session.query(rc).filter(sqlalchemy.and_(rc.email != None, rc.email != '', rc.j5username == submission_details['SubmittedBy'])).first()
            if recipient:
                name = recipient.lastname if recipient.lastname else recipient.j5username
                email_subject = 'Email Notification for submitting Section %s of certificate # %s' % (Section_title, self.certificate_no)
                email_body = 'Thank you for submitting Section %s of certificate # %s' % (Section_title, self.certificate_no)
                email_body += nemail_body
                email_greeting = 'Dear, %s<br/><br/>' % name
                self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')

    def get_expanding_status(self):
        path_info = RequestStack.request_stack.environ.get('PATH_INFO')
        if path_info == "view/certificates" or (path_info and '/expanded/' in path_info):
            return 'True'
        return 'False'

    expanding = property(get_expanding_status)

    def get_url_data(self, forms):
        url = self.logpage.logmodel.get_view_log_url(self.logid)
        if forms[0].uuid and url:
            url_start_length = url.find('/view/')
            if url_start_length > 0:
                url_start_length += 6
                url_end = "certificates#Lv01/certificates/%s/%s" % (self.logid, forms[0].uuid)
                url = url[:url_start_length] + url_end
                email_body = ' '
                if url:
                    email_body += ' Click <b><a href="%s">here</a></b> to view it' % url
                    return email_body
        return None

class CertificateLogModel(PermitToWork.CertificateLogModel):

    def get_default_log_sa(self, defaults, session, kwargs):
        now = datetime_tz.datetime_tz.now()
        tomorrow = now + datetime_tz.timedelta(days=1)
        defaults.update({"valid_start": tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)})
        defaults.update({"valid_end": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0)})
        # Apply the defaults
        default_row = self.logclass(**defaults)
        return default_row


#------------------------------------------------------------------------------------------------------------------------------
#class CustomCertificatesMixin(CertificatesMixin):
class CustomPermitsMixin(PermitsMixin, RegisterWorkflow.RegisterWorkflowMixin):    

    workflow_filename = "permits.workflow"

    #def init_instance(self, mapper, class_, oldinit, args, kwargs):
    #    now = datetime_tz.datetime_tz.now()
    #    self.valid_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    #    return sqlalchemy.orm.EXT_CONTINUE

    #@classmethod
    def on_logbook_start(cls, sa_session_class, logbook_handler_model, get_resource):
        cls.emailer = get_resource("email")

    def before_session_insert(self, sa_session):
        PermitsMixin.before_session_insert(self, sa_session)
        self.set_validity_fields()
        self.section_count = 0
        return sqlalchemy.orm.EXT_CONTINUE

    def before_session_update(self, sa_session):
        
        committed_state = self.get_committed_state(['status','valid_start','valid_end'])
        logging.critical('------------------------------------------%s' % committed_state )
        if self.status != committed_state['status']:
            self.status_changed(sa_session, committed_state)
            logging.critical('-------------------------------------------self.status_changed(sa_session, committed_state)')
        if self.valid_end != committed_state['valid_end']:
            self.set_validity_fields()
            logging.critical('-------------------------------------------self.set_validity_fields()')
        PermitsMixin.before_session_update(self, sa_session)
        logging.critical('-------------------------------------------CertificatesMixin.before_session_update(self, sa_session)')
        return sqlalchemy.orm.EXT_CONTINUE
    
    def set_validity_fields(self):
        #self.valid_end_minus_1 = self.valid_end - relativedelta.relativedelta(days=1)            
        self.valid_end_plus_1 = self.valid_end + relativedelta.relativedelta(days=1)
        #self.valid_minus_1_email_status = 'Not Sent'
        self.valid_plus_1_email_status = 'Not Sent'


    def send_hotwork_warning(self, sa_session, email_type):
        forms = self.get_industraforms()
        if forms:
            nemail_body = self.get_url_data(forms)
            logging.critical('+++++++++++++++++++++++++++++++++++++++++++++ Runing in send_hotwork_warning Sub Program : email_type = %s permit_no = %s ' %(email_type , self.permit_no))
            job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
            job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
            Team_Select_2 = self.get_industraform_data(forms, ['area1'])

            if Team_Select_2 and Team_Select_2[0]:
                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                   'groups.permit_issuer_hotwork',
                                                                                   area1_name,
                                                                                   area2_name,
                                                                                   area2_desc,
                                                                                   area3_name,
                                                                                   area3_desc,
                                                                                   area4_name,
                                                                                   area4_desc)
                users = self.get_users_with_profiles(sa_session, profiles)
                logging.critical('-------------------------------------------------------users         = %s' % users)

                if users:
                    if email_type == 1:
                        email_subject = 'Mail To Permit Issuer Hot Work  - Hot Work Permit %s validity will end soon' % self.permit_no
                        email_body = 'Please note that Hot Work Permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_hotwork group')
                        if job_owner_name[0] and job_owner_mail[0]:
                            jo_email_subject = 'Mail To Job Owner - Hot Work Permit %s validity will end soon' % self.permit_no
                            jo_email_body = 'Please note that Hot Work Permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                            jo_email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            jo_email_body += nemail_body
                            self.emailer.send(job_owner_mail, jo_email_subject, jo_email_greeting + jo_email_body, contenttype='text/html')
                    else:
                        email_subject = 'Mail To Permit Issuer Hot Work - Hot Work Permit %s validity has ended' % self.permit_no
                        email_body = 'Please note that Hot Work Permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_hotwork group')
                        if job_owner_name[0] and job_owner_mail[0]:
                            jo_email_subject = 'Mail To Job Owner - Hot Work Permit %s validity has ended' % self.permit_no
                            jo_email_body = 'Please note that Hot Work Permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                            jo_email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            jo_email_body += nemail_body
                            self.emailer.send(job_owner_mail, jo_email_subject, jo_email_greeting + jo_email_body, contenttype='text/html')

        if email_type == 1:
            self.valid_minus_1_email_status = 'Sent'
        else:
            self.valid_plus_1_email_status = 'Sent'




    def send_coldwork_warning(self, sa_session, email_type):
        forms = self.get_industraforms()
        if forms:
            nemail_body = self.get_url_data(forms)
            logging.critical('+++++++++++++++++++++++++++++++++++++++++++++ Runing in send_coldwork_warning Sub Program : email_type = %s permit_no = %s ' % (email_type, self.permit_no))
            job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
            job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
            Team_Select_2 = self.get_industraform_data(forms, ['area1'])
            if Team_Select_2 and Team_Select_2[0]:
                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                   'groups.permit_issuer_coldwork',
                                                                                   area1_name,
                                                                                   area2_name,
                                                                                   area2_desc,
                                                                                   area3_name,
                                                                                   area3_desc,
                                                                                   area4_name,
                                                                                   area4_desc)
                users = self.get_users_with_profiles(sa_session, profiles)
                logging.critical('-------------------------------------------------------users         = %s' % users)
                if users:
                    if email_type == 1:
                        email_subject = 'Mail To Permit Issuer Cold Work  - Cold Work Permit %s validity will end soon' % self.permit_no
                        email_body = 'Please note that Cold Work Permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_coldwork group')
                        if job_owner_name[0] and job_owner_mail[0]:
                            jo_email_subject = 'Mail To Job Owner - Cold Work Permit %s validity will end soon' % self.permit_no
                            jo_email_body = 'Please note that Cold Work Permit number <b> # %s </b> is due to expire soon.  It is valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                            jo_email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            jo_email_body += nemail_body
                            self.emailer.send(job_owner_mail, jo_email_subject, jo_email_greeting + jo_email_body, contenttype='text/html')
                    else:
                        email_subject = 'Mail To Permit Issuer Cold Work - Cold Work Permit %s validity has ended' % self.permit_no
                        email_body = 'Please note that Cold Work Permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                        self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_coldwork group')
                        if job_owner_name[0] and job_owner_mail[0]:
                            jo_email_subject = 'Mail To Job Owner - Cold Work Permit %s validity has ended' % self.permit_no
                            jo_email_body = 'Please note that Cold Work Permit number <b> # %s </b> has expired.  It was valid until %s.' % (self.permit_no, self.format_date(self.valid_end))
                            jo_email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            jo_email_body += nemail_body
                            self.emailer.send(job_owner_mail, jo_email_subject, jo_email_greeting + jo_email_body, contenttype='text/html')
        if email_type == 1:
            self.valid_minus_1_email_status = 'Sent'
        else:
            self.valid_plus_1_email_status = 'Sent'

            

    def format_date(self, date):
        if date:
            return date.astimezone(datetime_tz.localtz()).strftime('%d-%m-%Y, %H:%M')
        else:
            return 'Not specified'


    def get_area_data_form_areahierarchy_4_depth(self, sa_session, descriptions):

        area_desc_dict = {}
        area_name_dict = {}

        area_fields = ['area1', 'area2', 'area3', 'area4']
        for area in area_fields:
            area_desc_dict[area] = ''
            area_name_dict[area] = None

        depth = 1
        area_rc = Alchemy.find_recordclass('area_hierarchy')
        for description in descriptions:
            area_desc_dict['area'+str(depth)] = description
            if area_desc_dict['area'+str(depth)]:
                area = sa_session.query(area_rc).filter_by(depth=depth, description=area_desc_dict['area'+str(depth)], deleted=0).first()
                if not area:
                    logging.critical("Can't find a Level %d Area field that matches the one specified - %s" % (depth, area_desc_dict['area'+str(depth)]))
                    break
                else:
                    area_name_dict['area'+str(depth)] = area.name
            depth += 1

        return area_name_dict['area4'], area_desc_dict['area4'], area_name_dict['area3'], area_desc_dict['area3'], area_name_dict['area2'], area_desc_dict['area2'] ,area_name_dict['area1'], area_desc_dict['area1']


    def get_group_area_profiles_form_areahierarchy_4_depth(self, sa_session, groupname, area1_name, area2_name, area2_desc, area3_name, area3_desc, area4_name, area4_desc):
        profile_rc = Alchemy.find_recordclass('profile')

        if area4_name:
    #        logging.critical('------------------------Getting %s Profiles for Area1: %s, Area2: %s, Area3: %s, Area4: %s' % (groupname, area1_desc, area2_desc, area3_desc, area4_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%'),
                                                           profile_rc.area3.like('%' + area3_name + '%'),
                                                           profile_rc.area4.like('%' + area4_name + '%')).all()
        elif area3_name:
            logging.critical('------------------------Getting %s Profiles for Area1: PTTGC4, Area2: %s, Area3: %s' % (groupname, area2_desc, area3_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%'),
                                                           profile_rc.area3.like('%' + area3_name + '%')).all()
        elif area2_name:
            logging.critical('------------------------Getting %s Profiles for Area1: PTTGC4, Area2: %s, Area3: None' % (groupname, area2_desc))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname,
                                                           profile_rc.area1.like('%' + area1_name + '%'),
                                                           profile_rc.area2.like('%' + area2_name + '%')).all()
        else:
            logging.critical('------------------------Getting %s Profiles for all areas' % (groupname))
            profiles = sa_session.query(profile_rc).filter(profile_rc.groups == groupname).all()

        if not profiles:
            logging.critical('------------------------No profiles found for %s' % groupname)
        return profiles


    def get_users_with_profiles(self, sa_session, profiles):
        ss_users = set()
        personnel_rc = Alchemy.find_recordclass('personnel')
        for profile in profiles:
            if profile.description:
                logging.critical('------------------------Finding users who can fulfil profile %s' % profile.description)
            profile_users = sa_session.query(personnel_rc).filter(sqlalchemy.or_(personnel_rc.profile == profile.logid, personnel_rc.alt_profiles.like('%' + profile.logid + '%'))).all()
            for profile_user in profile_users:
                ss_users.add(profile_user.j5username)
        return ss_users



    def send_emails(self, sa_session, users, email_body, nemail_body, email_subject, logging_detail=None):
        personnel_rc = Alchemy.find_recordclass('personnel')
        if users:
            recipients = sa_session.query(personnel_rc).filter(personnel_rc.j5username.in_(users)).all()
            email_body += nemail_body
        else:
            if logging_detail:
                logging.critical('------------------------No users provided for %s email' % logging_detail)
            recipients = []
        for recipient in recipients:
            if recipient and recipient.email:

                # logging.critical('****************************************************************************************************** recipient.email %s' % recipient.email)
                email_list = []
                email_user = recipient.email
                email_list.append(email_user)
                # logging.critical('****************************************************************************************************** recipient len  %s' % len(email_list)) #join(lists)
                # logging.critical('****************************************************************************************************** recipient type %s' % type(email_list))  # join(lists)  str(mylist)
                # logging.critical('****************************************************************************************************** recipient      %s' % email_list)  # join(lists)
                # logging.critical('****************************************************************************************************** recipient      %s' % email_list)  # join(lists)

                if logging_detail:
                    logging.critical('------------------------Sending %s email to %s' % (logging_detail, recipient.j5username))
                else:
                    logging.critical('------------------------Sending email to %s' % (recipient))
                email_greeting = 'Dear %s<br/><br/>' % recipient.lastname
                self.emailer.send(email_list, email_subject, email_greeting + email_body, contenttype='text/html')
                # self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')

                if logging_detail:
                    logging.critical('------------------------Sent %s email to %s' % (logging_detail, recipient.email))
                else:
                    logging.critical('------------------------Sent email to %s' % (recipient))


        
    def status_changed(self, sa_session, committed_state):
        logging.critical('------------------------------def status_changed(self, sa_session, committed_state):')
        permit_type = self.get_permit_type(sa_session)
        logging.critical('------------------------------permit_type = %s' % permit_type)
        
        if permit_type == 'Hot Work':
            forms = self.get_industraforms()
            logging.critical('------------------------ Hot Work %s' %permit_type )
            # The status has changed from Drafting to Submitted
            
            if forms:
                section_1_gate_in_name   = 'Permit Request (1/4)'
                section_1_gate_out_name  = 'Permit Request (2/4)'
                section_2_gate_in_name   = 'Permit Request (3/4)'
                section_2_gate_out_name  = 'Permit Request (4/4)'
                section_3_gate_in_name   = 'Cosigner Approval (1/2)'
                section_3_gate_out_name  = 'Cosigner Approval (2/2)'
                section_4_gate_in_name   = 'Permit Preparation (1/4)'
                section_4_gate_out_name  = 'Permit Preparation (2/4)'
                section_5_gate_in_name   = 'Permit Preparation (3/4)'
                section_5_gate_out_name  = 'Permit Preparation (4/4)'
                section_6_gate_in_name   = 'Permit Non-Open Flammable Approval (1/4)'
                section_6_gate_out_name  = 'Permit Non-Open Flammable Approval (2/4)'
                section_7_gate_in_name   = 'Permit Open Flammable Approval (1/4)'
                section_7_gate_out_name  = 'Permit Open Flammable Approval (2/4)'
                section_8_gate_in_name   = 'Permit Non-Open Flammable Approval (3/4)'
                section_8_gate_out_name  = 'Permit Non-Open Flammable Approval (4/4)'
                section_9_gate_in_name   = 'Permit Open Flammable Approval (3/4)'
                section_9_gate_out_name  = 'Permit Open Flammable Approval (4/4)'
                section_10_gate_in_name  = 'Working'
                section_10_gate_out_name = 'Gas Test (While working)'
                section_11_gate_in_name  = 'Renewal of Permit (1/4)'
                section_11_gate_out_name = 'Renewal of Permit (2/4)'
                section_12_gate_in_name  = 'Renewal of Permit Non-Open Flammable (3/4)'#Non-Open Flammable
                section_12_gate_out_name = 'Renewal of Permit Non-Open Flammable (4/4)'#Non-Open Flammable
                section_13_gate_in_name  = 'Renewal of Permit Open Flammable (3/4)'#Open Flammable
                section_13_gate_out_name = 'Renewal of Permit Open Flammable (4/4)'#Open Flammable
                section_14_gate_in_name  = 'Permit Non-Open Flammable Finished (1/2)'#Non-Open Flammable
                section_14_gate_out_name = 'Permit Non-Open Flammable Finished (2/2)'#Non-Open Flammable
                section_15_gate_in_name  = 'Permit Open Flammable Finished (1/2)'#Open Flammable
                section_15_gate_out_name = 'Permit Open Flammable Finished (2/2)'#Open Flammable

                nemail_body = self.get_url_data(forms)

#Section 1  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                

                if committed_state['status'] in (None, '', section_1_gate_in_name) and  self.status == section_1_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 1 Submitted')
                    self.section_count = 1
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    Hotwork_Type   = self.get_industraform_data(forms, ['Choice62'])
                    logging.critical('------------------------ job_owner_name  %s' % job_owner_name )
                    logging.critical('------------------------ job_owner_mail  %s' % job_owner_mail )
                    logging.critical('------------------------ Hotwork_Type  %s' % Hotwork_Type )
                    
                    if job_owner_name[0] and job_owner_mail[0]:
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<submitted><%s><hotwork>Section contractor fill the data has been submitted' % self.permit_no
                            email_body    = 'Please note that hotwork open flammable job number <b> # %s </b> Section contractor fill the data has been submitted.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submitted><%s><hotwork>Section contractor fill the data has been submitted' % self.permit_no
                            email_body    = 'Please note that hotwork non-open flammable job number <b> # %s </b> Section contractor fill the data has been submitted.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 1  Reject ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                

                if committed_state['status'] in (None, '', section_1_gate_out_name) and  self.status == section_1_gate_in_name and  self.section_count == 1 :
                    logging.critical('********************************************************************************** Hotwork section 1 Reject')
                    self.section_count = 0
                    contractor_name = self.get_industraform_data(forms, ['HWRU_Name'])
                    contractor_mail = self.get_industraform_data(forms, ['HWRU_Mail'])
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    job_owner_tel = self.get_industraform_data(forms, ['JON_Tel'])
                    Hotwork_Type   = self.get_industraform_data(forms, ['Choice62'])
                    logging.critical('------------------------ contractor_name  %s' %contractor_name )
                    logging.critical('------------------------ contractor_mail  %s' %contractor_mail )

                    if contractor_name[0] and contractor_mail[0]:
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s <br/>job owner Tel : %s'% (job_owner_name[0], job_owner_mail[0], job_owner_tel[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork non-Open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 2  Submitted **************************************************************************************************************************************************

                if committed_state['status'] in (None, '', section_2_gate_in_name) and  self.status == section_2_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 2 Submitted')
                    self.section_count  = 2
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    Hotwork_Type   = self.get_industraform_data(forms, ['Choice62'])
                    cosign_name = self.get_industraform_data(forms, ['Text250'])
                    cosign_mail = self.get_industraform_data(forms, ['Text206'])
                    cosign_request = self.get_industraform_data(forms, ['ChecklistItem146'])
                    logging.critical('----------------------------------------- cosign_name %s'%cosign_name)
                    logging.critical('----------------------------------------- cosign_mail %s'%cosign_mail)

                    if cosign_request[0] == 'Yes':
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Request = Yes')
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<cosign-request><%s><hotwork>Section job owner verify data has been submitted' % self.permit_no
                            email_body    = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Section job owner verify data has been submitted' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % cosign_name
                            email_body += nemail_body
                            self.emailer.send(cosign_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<cosign-request><%s><hotwork>Section job owner verify data has been submitted' % self.permit_no
                            email_body    = 'Please note that Hot Work number <b> # %s </b> Section job owner verify data has been submitted.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % cosign_name
                            email_body += nemail_body
                            self.emailer.send(cosign_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                    else:
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Request = No')
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_issuer_hotwork',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<submitted><%s><hotwork>Section job owner verify data has been submitted' % self.permit_no
                                    email_body = 'Please note that Hotwork Open Flammable Job number <b> # %s </b> Section job owner verify data has been submitted' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject,'permit_issuer_hotwork group')
                        else:
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_issuer_hotwork',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<submitted><%s><hotwork>Section job owner verify data has been submitted' % self.permit_no
                                    email_body = 'Please note that Hotwork Non-Open Flammable Job number <b> # %s </b> Section job owner verify data has been submitted' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject,'permit_issuer_hotwork group')

# Section 2  Reject ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_2_gate_out_name) and self.status == section_2_gate_in_name and self.section_count == 2:
                    logging.critical('********************************************************************************** Hotwork section 1 Reject')
                    self.section_count = 1
                    contractor_name     = self.get_industraform_data(forms, ['HWRU_Name'])
                    contractor_mail     = self.get_industraform_data(forms, ['HWRU_Mail'])
                    job_owner_name      = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail      = self.get_industraform_data(forms, ['JON_Mail'])
                    job_owner_tel       = self.get_industraform_data(forms, ['JON_Tel'])
                    Hotwork_Type        = self.get_industraform_data(forms, ['Choice62'])
                    logging.critical('------------------------ contractor_name  %s' % contractor_name)
                    logging.critical('------------------------ contractor_mail  %s' % contractor_mail)

                    if contractor_name[0] and contractor_mail[0]:
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s <br/>job owner Tel : %s' % (job_owner_name[0], job_owner_mail[0], job_owner_tel[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork non-Open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s' % (job_owner_name[0], job_owner_mail[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if job_owner_name[0] and job_owner_mail[0]:
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><hotwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Please note that hotwork non-Open flammable job number <b> # %s </b> Section job owner verify data has been reject.' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
#                    logging.critical('Team_Select 2        = %s' % Team_Select_2)
#
#                    if Team_Select_2 and Team_Select_2[0]:
#                        area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
#                        profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session, 'groups.permit_approver_hotwork_openframe', area1_name, area2_name, area2_desc, area3_name, area3_desc, area4_name, area4_desc)
#                        users = self.get_users_with_profiles(sa_session, profiles)
#                        logging.critical('-------------------------------------------------------users         = %s' % users)
#                        if users:
#                            email_subject = 'Mail To permit_approver_hotwork_openframe Hotwork number %s section Permit Request been Submitted' % self.permit_no
#                            email_body = 'Please note that Hotwork number <b> # %s </b> section Permit Request has been Submitted' % self.permit_no
#                            self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_hotwork_openframe group')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Section 3  Submitted **************************************************************************************************************************************************

                if committed_state['status'] in (None, '', section_3_gate_in_name) and  self.status == section_3_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 3 Submitted')
                    self.section_count  = 3
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    Hotwork_Type   = self.get_industraform_data(forms, ['Choice62'])
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
                    cosign_name = self.get_industraform_data(forms, ['Text250'])
                    cosign_mail = self.get_industraform_data(forms, ['Text206'])
                    cosign_approve = self.get_industraform_data(forms, ['ChecklistItem148'])
                    logging.critical('------------------------ cosign_name  %s' %cosign_name )
                    logging.critical('------------------------ cosign_mail  %s' %cosign_mail )
                    logging.critical('------------------------ cosign_approve  %s' %cosign_approve )
                    
                    if cosign_approve[0] == 'Yes':
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Approve = Yes')
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_issuer_hotwork',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<approved><%s><hotwork>Section cosigner approval has been approved' % self.permit_no
                                    email_body = 'Please note that Hotwork number <b> # %s </b> Section cosigner approval has been approved.' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject,'permit_issuer_hotwork group')
                        else:
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_issuer_hotwork',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<approved><%s><hotwork>Section cosigner approval has been approved' % self.permit_no
                                    email_body = 'Please note that Hotwork number <b> # %s </b> Section cosigner approval has been approved.' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject,'permit_issuer_hotwork group')
                    else:
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Request = No')
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<reject><%s><hotwork>Section cosigner approval has been reject' % self.permit_no
                            email_body    = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Section cosigner approval has been reject' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><hotwork>Section cosigner approval has been reject' % self.permit_no
                            email_body    = 'Please note that Hot Work Non-Open Flammable Job number <b> # %s </b> Section cosigner approval has been reject' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 3  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
#                                                        
#                if committed_state['status'] in (None, '', section_3_gate_in_name) and  self.status == section_3_gate_out_name: 
#                    self.section_count  = 3
#                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
#                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])
#                    if job_owner_name[0] and job_owner_mail[0]:
#                        email_subject = 'Mail To To Job Owner Hot Work number %s Section Approve (Non-Open Flammable) has been Submitted' % self.permit_no
#                        email_body    = 'Please note that Hot Work number <b> # %s </b> Section Approve (Non-Open Flammable) has been has been Submitted' % self.permit_no
#                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
#                        email_body += nemail_body
#                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
#
#Section 4  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                        
                if committed_state['status'] in (None, '', section_4_gate_in_name) and  self.status == section_4_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 4 Submitted')
                    self.section_count = 4
                    Hotwork_Type   = self.get_industraform_data(forms, ['Choice62'])
                    job_owner_name  = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail  = self.get_industraform_data(forms, ['JON_Mail'])
                    permit_issuer_verify = self.get_industraform_data(forms, ['ChecklistItem144'])

                    if permit_issuer_verify[0] == 'Yes':
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<submit><%s><hotwork>Section permit Issuer verify data has been submitted' % self.permit_no
                            email_body    = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Section permit Issuer verify data has been submitted' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<submit><%s><hotwork>Section permit Issuer verify data has been submitted' % self.permit_no
                            email_body    = 'Please note that Hot Work number <b> # %s </b> Section permit Issuer verify data has been submitted' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                    else:
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            email_subject = '<reject><%s><hotwork>Section permit Issuer verify data has been reject' % self.permit_no
                            email_body    = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Section permit Issuer verify data has been reject' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')
                        else:
                            email_subject = '<reject><%s><hotwork>Section permit Issuer verify data has been reject' % self.permit_no
                            email_body    = 'Please note that Hot Work number <b> # %s </b> Section permit Issuer verify data has been reject' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 5  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_5_gate_in_name) and  self.status == section_5_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 5 Submitted')
                    self.section_count  = 5
                    job_owner_name      = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail      = self.get_industraform_data(forms, ['JON_Mail'])
                    contractor_name     = self.get_industraform_data(forms, ['HWRU_Name'])
                    contractor_mail     = self.get_industraform_data(forms, ['HWRU_Mail'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        email_subject = '<submitted><%s><hotwork>Section permit issuer preparation area has been submitted' % self.permit_no
                        email_body = 'Please note that Hotwork number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<submitted><%s><hotwork>Section permit issuer preparation area has been submitted' % self.permit_no
                        email_body = 'Please note that Hotwork number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        email_body += nemail_body
                        self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')

# Section 5  Approved ----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_5_gate_out_name) and (self.status == section_6_gate_in_name or self.status == section_7_gate_in_name) :
                    logging.critical('********************************************************************************** Hotwork section 5 Approved')
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    Hotwork_Type = self.get_industraform_data(forms, ['Choice62'])

                    # if Hotwork_Type[0] == 'Open Flammable Job':
                    #     logging.critical('********************************************************************************** Hotwork section 5 Submitted Hotwork_Type Is : Open Flammable Job')
                    #     if Team_Select_2 and Team_Select_2[0]:
                    #         area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(
                    #             sa_session, Team_Select_2[0])
                    #         profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                    #                                                                            'groups.permit_approver_hotwork_openframe',
                    #                                                                            area1_name,
                    #                                                                            area2_name,
                    #                                                                            area2_desc,
                    #                                                                            area3_name,
                    #                                                                            area3_desc,
                    #                                                                            area4_name,
                    #                                                                            area4_desc)
                    #         users = self.get_users_with_profiles(sa_session, profiles)
                    #         logging.critical(
                    #             '-------------------------------------------------------users         = %s' % users)
                    #         if users:
                    #             email_subject = '<submitted><%s><hotwork>Section permit issuer preparation area has been submitted' % self.permit_no
                    #             email_body = 'Please note that Hotwork number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                    #             self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_hotwork_openframe group')
                    #
                    # else:
                    #     logging.critical('********************************************************************************** Hotwork section 5 Submitted Hotwork_Type Is : Non Open Flammable Job')
                    #     if Team_Select_2 and Team_Select_2[0]:
                    #         area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(
                    #             sa_session, Team_Select_2[0])
                    #         profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                    #                                                                            'groups.permit_approver_hotwork_non_openframe',
                    #                                                                            area1_name,
                    #                                                                            area2_name,
                    #                                                                            area2_desc,
                    #                                                                            area3_name,
                    #                                                                            area3_desc,
                    #                                                                            area4_name,
                    #                                                                            area4_desc)
                    #         users = self.get_users_with_profiles(sa_session, profiles)
                    #         logging.critical('-------------------------------------------------------users         = %s' % users)
                    #         if users:
                    #             email_subject = '<submitted><%s><hotwork>Section permit issuer preparation area has been submitted' % self.permit_no
                    #             email_body = 'Please note that Hotwork number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                    #             self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_approver_non_openframe group')




#------------------------------------ Don't Send to onsite-verifier -----------------------------
#                    if onsite_investsite[0] == 'Yes':
#                        if Hotwork_Type[0] == 'Open Flammable Job':
#                            email_subject = 'Mail To Onsite Verifier Hot Work Open Flammable Job number %s Section Permit Issuer Open Flamable would like to sign before work' % self.permit_no
#                            email_body    = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Section Permit Issuer Open Flamable would like to sign before work' % self.permit_no
#                            email_greeting = 'Dear, %s<br/><br/>' % onsite_name
#                            email_body += nemail_body
#                            self.emailer.send(onsite_mail, email_subject, email_greeting + email_body, contenttype='text/html')
#                        else:
#                            email_subject = 'Mail To To Onsite Verifier Hot Work Job number %s Section Permit Issuer Non Open Flamable would like to sign before work' % self.permit_no
#                            email_body    = 'Please note that Hot Work number <b> # %s </b> Section Permit Issuer Non Open Flamable would like to sign before work' % self.permit_no
#                            email_greeting = 'Dear, %s<br/><br/>' % onsite_name
#                            email_body += nemail_body
#                            self.emailer.send(onsite_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 6  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_6_gate_in_name) and  self.status == section_6_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 6 Submitted')
                    self.section_count  = 6
                    job_owner_name      = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail      = self.get_industraform_data(forms, ['JON_Mail'])
                    contractor_name     = self.get_industraform_data(forms, ['HWRU_Name'])
                    contractor_mail     = self.get_industraform_data(forms, ['HWRU_Mail'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        email_subject = '<working><%s><hotwork>Permit has been working' % self.permit_no
                        email_body = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Work Permit Approval (Open Flammable)' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<submitted><%s><hotwork>Permit has been working' % self.permit_no
                        email_body = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Work Permit Approval (Open Flammable)' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        email_body += nemail_body
                        self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 7  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_7_gate_in_name) and  self.status == section_7_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 7 Submitted')
                    self.section_count  = 7
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])


                    email_subject = '<working><%s><hotwork>Permit has been working' % self.permit_no
                    email_body = 'Please note that Hot Work Open Flammable Job number <b> # %s </b> Work Permit Approval (Open Flammable)' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body,contenttype='text/html')

#Section 8  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_8_gate_in_name) and  self.status == section_8_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 8 Submitted')
                    self.section_count  = 8


#Section 9 Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_9_gate_in_name) and  self.status == section_9_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 9 Submitted')
                    self.section_count  = 9

             
#Section 10  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
                            
                if committed_state['status'] in (None, '', section_10_gate_in_name) and  self.status == section_10_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 10 Submitted')
                    self.section_count  = 10

#Section 11  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_11_gate_in_name) and  self.status == section_11_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 11 Submitted')
                    self.section_count  = 11
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    Hotwork_Type = self.get_industraform_data(forms, ['Choice62'])
                    Renewal_Type = self.get_industraform_data(forms, ['ChecklistItem140'])

                    if Renewal_Type[0] == 'Yes':
                        if Hotwork_Type[0] == 'Open Flammable Job':
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_approver_hotwork_openframe',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<submitted><%s><hotwork>Section renewal of permit request has been submitted' % self.permit_no
                                    email_body = 'Please note that Hotwork number <b> # %s </b> Section renewal of permit request has been submitted' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_hotwork_openframe group')
                        else:
                            if Team_Select_2 and Team_Select_2[0]:
                                area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                                profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                                   'groups.permit_approver_hotwork_non_openframe',
                                                                                                   area1_name,
                                                                                                   area2_name,
                                                                                                   area2_desc,
                                                                                                   area3_name,
                                                                                                   area3_desc,
                                                                                                   area4_name,
                                                                                                   area4_desc)
                                users = self.get_users_with_profiles(sa_session, profiles)
                                logging.critical('-------------------------------------------------------users         = %s' % users)
                                if users:
                                    email_subject = '<submitted><%s><hotwork>Section renewal of permit request has been submitted' % self.permit_no
                                    email_body = 'Please note that Hotwork number <b> # %s </b> Section renewal of permit request has been submitted' % self.permit_no
                                    self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_hotwork_non_openframe group')

#Section 12  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_12_gate_in_name) and  self.status == section_12_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 12 Submitted')
                    self.section_count  = 12
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<approve><%s><hotwork>Section renewal of permit request has been approved' % self.permit_no
                    email_body = '<approve> Please note that Hot Work Non-Open Flammable Job number <b> # %s </b> Section renewal of permit request has been approved' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body,contenttype='text/html')
                    
#Section 13  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_13_gate_in_name) and self.status == section_13_gate_out_name:
                    logging.critical('********************************************************************************** Hotwork section 12 Submitted')
                    self.section_count = 12
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<approve><%s><hotwork>Section renewal of permit request has been approved' % self.permit_no
                    email_body = '<approve> Please note that Hot Work Open Flammable Job number <b> # %s </b> Section renewal of permit request has been approved' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 14  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_14_gate_in_name) and  self.status == section_14_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 14 Submitted')
                    self.section_count  = 14
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<finished><%s><hotwork>Permit has been finished' % self.permit_no
                    email_body = 'Please note that Hot Work Job number <b> # %s </b> Permit has been Finished' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body,contenttype='text/html')

#Section 15  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_15_gate_in_name) and  self.status == section_15_gate_out_name :
                    logging.critical('********************************************************************************** Hotwork section 15 Submitted')
                    self.section_count  = 15
                    job_owner_name = self.get_industraform_data(forms, ['JON_Name'])
                    job_owner_mail = self.get_industraform_data(forms, ['JON_Mail'])

                    email_subject = '<finished><%s><hotwork>Permit has been finished' % self.permit_no
                    email_body = 'Please note that Hot Work Job number <b> # %s </b> Permit has been Finished' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body,contenttype='text/html')

#############################################################################################################################################################                    
        
        if permit_type == 'Cold Work':            
            forms = self.get_industraforms()
            logging.critical('------------------------------cold work IF Permit_type = TRUE')
            logging.critical('------------------------------cold work From = %s' % forms)
            # The status has changed from Drafting to Submitted
            if forms:
                section_1_gate_in_name   = 'Permit Request (1/4)'
                section_1_gate_out_name  = 'Permit Request (2/4)'
                section_2_gate_in_name   = 'Permit Request (3/4)'
                section_2_gate_out_name  = 'Permit Request (4/4)'
                section_3_gate_in_name   = 'Cosigner Approval (1/2)'
                section_3_gate_out_name  = 'Cosigner Approval (2/2)'
                section_4_gate_in_name   = 'Permit Preparation (1/2)'
                section_4_gate_out_name  = 'Permit Preparation (2/2)'
                # section_5_gate_in_name   = 'Permit Preparation (3/4)'
                # section_5_gate_out_name  = 'Permit Preparation (4/4)'
                section_6_gate_in_name   = 'Permit Approval (1/4)'
                section_6_gate_out_name  = 'Permit Approval (2/4)'
                section_7_gate_in_name   = 'Permit Approval (3/4)'
                section_7_gate_out_name  = 'Permit Approval (4/4)'
                section_8_gate_in_name   = 'Working'
                section_8_gate_out_name  = 'Renewal of Permit (1/3)'
                section_9_gate_in_name   = 'Renewal of Permit (2/3)'
                section_9_gate_out_name  = 'Renewal of Permit (3/3)'
                section_10_gate_in_name   = 'Finished (1/2)'
                section_10_gate_out_name  = 'Finished (2/2)'
                
                nemail_body = self.get_url_data(forms)

#Section 1  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                

                if committed_state['status'] in (None, '', section_1_gate_in_name) and  self.status == section_1_gate_out_name :

                    logging.critical('********************************************************************************** Coldwork section 1 Submitted')
                    self.section_count = 1
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    
                    if job_owner_name[0] and job_owner_mail[0]:
                            email_subject = '<submitted><%s><coldwork>Section contractor fill the data has been submitted' % self.permit_no
                            email_body    = 'Cold Work job number <b> # %s </b> Section contractor fill the data has been submitted' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                            email_body += nemail_body
                            self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 1  Reject ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                

                if committed_state['status'] in (None, '', section_1_gate_out_name) and  self.status == section_1_gate_in_name and  self.section_count == 1 :
                    logging.critical('********************************************************************************** Coldwork section 1 Reject')
                    self.section_count = 0
                    contractor_name = self.get_industraform_data(forms, ['Text1'])
                    contractor_mail = self.get_industraform_data(forms, ['Text249'])
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    job_owner_tel = self.get_industraform_data(forms, ['Text263'])

                    if contractor_name[0] and contractor_mail[0]:
                            email_subject = '<reject><%s><coldwork>Section job owner verify data has been reject' % self.permit_no
                            email_body = 'Edit or contact job owner that cold work job number <b> # %s </b> Section job owner verify data has edit or reject' % self.permit_no
                            email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                            job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s <br/>job owner Tel : %s' % (
                            job_owner_name[0], job_owner_mail[0], job_owner_tel[0])
                            email_body += nemail_body
                            email_body += job_owner_data
                            self.emailer.send(contractor_mail, email_subject, email_greeting + email_body,contenttype='text/html')
                    
#Section 2  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
                            
                if committed_state['status'] in (None, '', section_2_gate_in_name) and  self.status == section_2_gate_out_name:

                    logging.critical('********************************************************************************** Coldwork section 2 Reject')
                    self.section_count = 2
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    cosign_name = self.get_industraform_data(forms, ['Text264'])
                    cosign_mail = self.get_industraform_data(forms, ['Text265'])
                    cosign_request = self.get_industraform_data(forms, ['ChecklistItem146'])

                    if cosign_request[0] == 'Yes':
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Request = Yes')
                        email_subject = '<cosign-request><%s><coldwork>Section job owner verify data has been submitted' % self.permit_no
                        email_body = 'Please note that coldwork Job number <b> # %s </b> Section job owner verify data has been submitted.' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % cosign_name
                        email_body += nemail_body
                        self.emailer.send(cosign_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    else:
                        logging.critical('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cosign-Request = No')
                        if Team_Select_2 and Team_Select_2[0]:
                            area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                            profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                               'groups.permit_issuer_coldwork',
                                                                                               area1_name,
                                                                                               area2_name,
                                                                                               area2_desc,
                                                                                               area3_name,
                                                                                               area3_desc,
                                                                                               area4_name,
                                                                                               area4_desc)
                            users = self.get_users_with_profiles(sa_session, profiles)
                            logging.critical('-------------------------------------------------------users         = %s' % users)
                            if users:
                                email_subject = '<submitted><%s><coldwork>Section job owner verify data has been submitted' % self.permit_no
                                email_body = 'Please note that Coldwork Job number <b> # %s </b> Section job owner verify data has been submitted' % self.permit_no
                                self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_coldwork group')

# Section 2  Reject ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_2_gate_out_name) and self.status == section_2_gate_in_name and self.section_count == 2:
                    logging.critical('********************************************************************************** Coldwork section 2 Reject')
                    self.section_count = 1
                    contractor_name = self.get_industraform_data(forms, ['Text1'])
                    contractor_mail = self.get_industraform_data(forms, ['Text249'])
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    job_owner_tel = self.get_industraform_data(forms, ['Text263'])

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<reject><%s><coldwork>Section job owner verify data has been reject' % self.permit_no
                        email_body = 'Edit or contact job owner that cold work job number <b> # %s </b> Section job owner verify data has been reject' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        job_owner_data = '<br/>job owner Name : %s <br/>job owner Mail : %s <br/>job owner Tel : %s' % (job_owner_name[0], job_owner_mail[0], job_owner_tel[0])
                        email_body += nemail_body
                        email_body += job_owner_data
                        self.emailer.send(contractor_mail, email_subject, email_greeting + email_body, contenttype='text/html')


#Section 3  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------      
                                                        
                if committed_state['status'] in (None, '', section_3_gate_in_name) and  self.status == section_3_gate_out_name:
                    logging.critical('********************************************************************************** Coldwork section 3 Reject')
                    self.section_count  = 3
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    # cosign_name = self.get_industraform_data(forms, ['Text264'])
                    # cosign_mail = self.get_industraform_data(forms, ['Text265'])
                    cosign_approve = self.get_industraform_data(forms, ['ChecklistItem148'])

                    if cosign_approve[0] == 'Yes':
                        if Team_Select_2 and Team_Select_2[0]:
                            area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(sa_session, Team_Select_2[0])
                            profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                               'groups.permit_issuer_coldwork',
                                                                                               area1_name,
                                                                                               area2_name,
                                                                                               area2_desc,
                                                                                               area3_name,
                                                                                               area3_desc,
                                                                                               area4_name,
                                                                                               area4_desc)
                            users = self.get_users_with_profiles(sa_session, profiles)
                            logging.critical('-------------------------------------------------------users         = %s' % users)
                            if users:
                                email_subject = '<submitted><%s><coldwork>Section cosigner approval has been submitted' % self.permit_no
                                email_body = 'Please note that Coldwork Job number <b> # %s </b> Section cosigner approval has been submitted' % self.permit_no
                                self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_issuer_coldwork group')
                    else:
                        email_subject = '<reject><%s><coldwork>Section cosigner approval has been reject' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section cosigner approval has been reject' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 4  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_4_gate_in_name) and  self.status == section_4_gate_out_name:
                    logging.critical('********************************************************************************** Coldwork section 4 Reject')
                    self.section_count  = 4
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    contractor_name = self.get_industraform_data(forms, ['Text1'])
                    contractor_mail = self.get_industraform_data(forms, ['Text249'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        email_subject = '<submitted><%s><coldwork>Section permit issuer preparation area has been submitted' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<submitted><%s><coldwork>Section permit issuer preparation area has been submitted' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        email_body += nemail_body
                        self.emailer.send(contractor_name, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 4  Approve----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_4_gate_out_name) and  self.status == section_6_gate_in_name:
                    logging.critical('********************************************************************************** Coldwork section 5 Reject')
                    self.section_count  = 5
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])

                    # if Team_Select_2 and Team_Select_2[0]:
                    #     area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(
                    #         sa_session, Team_Select_2[0])
                    #     profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                    #                                                                        'groups.permit_approver_coldwork',
                    #                                                                        area1_name,
                    #                                                                        area2_name,
                    #                                                                        area2_desc,
                    #                                                                        area3_name,
                    #                                                                        area3_desc,
                    #                                                                        area4_name,
                    #                                                                        area4_desc)
                    #     users = self.get_users_with_profiles(sa_session, profiles)
                    #     logging.critical('-------------------------------------------------------users         = %s' % users)
                    #     if users:
                    #         email_subject = '<submitted><%s><coldwork>Section permit issuer preparation area has been submitted' % self.permit_no
                    #         email_body = 'Please note that coldwork number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                    #         self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_coldwork group')

                    if job_owner_name[0] and job_owner_mail[0]:
                        email_subject = '<submitted><%s><coldwork>Section permit issuer preparation area has been submitted' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section permit issuer preparation area has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')



#Section 5  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------
                            
                if committed_state['status'] in (None, '', section_6_gate_in_name) and  self.status == section_6_gate_out_name:
                    logging.critical('********************************************************************************** Coldwork section 6 Reject')
                    self.section_count  = 6

                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    contractor_name = self.get_industraform_data(forms, ['Text1'])
                    contractor_mail = self.get_industraform_data(forms, ['Text249'])

                    if job_owner_name[0] and job_owner_mail[0]:
                        email_subject = '<submitted><%s><coldwork>Section Work permit Approval has been submitted' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section Work permit Approval has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                        email_body += nemail_body
                        self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

                    if contractor_name[0] and contractor_mail[0]:
                        email_subject = '<submitted><%s><coldwork>Section Work permit Approval has been submitted' % self.permit_no
                        email_body = 'Please note that Cold Work Job number <b> # %s </b> Section Work permit Approval has been submitted' % self.permit_no
                        email_greeting = 'Dear, %s<br/><br/>' % contractor_name
                        email_body += nemail_body
                        self.emailer.send(contractor_mail, email_subject, email_greeting + email_body,contenttype='text/html')

#Section 6  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_7_gate_in_name) and  self.status == section_7_gate_out_name :
                    logging.critical('********************************************************************************** Coldwork section 7 Reject')
                    self.section_count  = 7
                    # job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    # job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    #
                    # email_subject = '<working><%s><coldwork>Permit has been working' % self.permit_no
                    # email_body = 'Please note that Coldwork Job number <b> # %s </b> Section Permit Request has Working' % self.permit_no
                    # email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    # email_body += nemail_body
                    # self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')

#Section 7  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_8_gate_in_name) and  self.status == section_8_gate_out_name :
                    logging.critical('********************************************************************************** Coldwork section 8 Reject')
                    self.section_count  = 8
                    Team_Select_2 = self.get_industraform_data(forms, ['area1'])
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])
                    Renewal_Type = self.get_industraform_data(forms, ['ChecklistItem140'])

                    if Renewal_Type[0] == 'Yes':
                        if Team_Select_2 and Team_Select_2[0]:
                            area4_name, area4_desc, area3_name, area3_desc, area2_name, area2_desc, area1_name, area1_desc = self.get_area_data_form_areahierarchy_4_depth(
                                sa_session, Team_Select_2[0])
                            profiles = self.get_group_area_profiles_form_areahierarchy_4_depth(sa_session,
                                                                                               'groups.permit_approver_coldwork',
                                                                                               area1_name,
                                                                                               area2_name,
                                                                                               area2_desc,
                                                                                               area3_name,
                                                                                               area3_desc,
                                                                                               area4_name,
                                                                                               area4_desc)
                            users = self.get_users_with_profiles(sa_session, profiles)
                            logging.critical(
                                '-------------------------------------------------------users         = %s' % users)
                            if users:
                                email_subject = '<submitted><%s><coldwork>Section renewal of permit has been submitted' % self.permit_no
                                email_body = 'Please note that coldwork number <b> # %s </b> Section renewal of permit has been submitted.' % self.permit_no
                                self.send_emails(sa_session, users, email_body, nemail_body, email_subject, 'permit_approver_coldwork group')

# Section 8  Submitted----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_9_gate_in_name) and  self.status == section_9_gate_out_name :
                    logging.critical('********************************************************************************** Coldwork section 9 Reject')
                    self.section_count  = 9
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])

                    email_subject = '<approve><%s><coldwork>Section renewal of permit has been approved' % self.permit_no
                    email_body = 'Please note that coldwork Job number <b> # %s </b> Section renewal of permit has been approved' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')


# Section 9  Submitted---------------------------------------------------------------------------------------------------------------------------------------------------------------

                if committed_state['status'] in (None, '', section_10_gate_in_name) and  self.status == section_10_gate_out_name :
                    logging.critical('********************************************************************************** Coldwork section 10 Reject')
                    self.section_count  = 10
                    job_owner_name = self.get_industraform_data(forms, ['Text261'])
                    job_owner_mail = self.get_industraform_data(forms, ['Text262'])

                    email_subject = '<finished><%s><coldwork>Permit has been finished' % self.permit_no
                    email_body = 'Please note that coldwork Job number <b> # %s </b> Permit has been Finished' % self.permit_no
                    email_greeting = 'Dear, %s<br/><br/>' % job_owner_name
                    email_body += nemail_body
                    self.emailer.send(job_owner_mail, email_subject, email_greeting + email_body, contenttype='text/html')





############################################################################################################################################################################################################
    def get_permit_type(self, sa_session):
        rc = Alchemy.find_recordclass('permit_forms')
        form = sa_session.query(rc.title).filter(rc.logid == self.permit_type).first()
        if form:
            return form.title
        return None

    def get_industraforms(self):
        return get_logbook_linked_forms(logbook_record=self)

    def get_industraform_data(self, forms, list_of_fields, value_type="DisplayValue"):
        data_dict = []
        if forms:
            form_data_snapshot = forms[0].get_form_data_snapshot()
            data_dict = form_data_snapshot.query(list_of_fields, default_element_attribute=value_type)
        return data_dict

        # This Section checks the specified Section's for the submitter, looks them up in the personnel logbook and send them an email (if they have an email address)

    def send_submitter_email(self, Section_title, sa_session):
        forms = get_logbook_linked_forms(logbook_record=self)
        logging.critical('---------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        form_data_snapshot = forms[0].get_form_data_snapshot()
        logging.critical('---------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        submission_details = self.get_Section_submission_user_and_date(form_data_snapshot, Section_title)
        logging.critical('---------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> submission_details ')
        if submission_details and submission_details['SubmittedBy']:
            rc = Alchemy.find_recordclass('personnel')
            recipient = sa_session.query(rc).filter(sqlalchemy.and_(rc.email != None, rc.email != '', rc.j5username == submission_details['SubmittedBy'])).first()
            if recipient:
                name = recipient.lastname if recipient.lastname else recipient.j5username
                email_subject = 'Email Notification for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_body = 'Thank you for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_greeting = 'Dear, %s<br/><br/>' % name
                self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')
                logging.critical('---------->>>>>>>>>>  send_submitter_email(self, Section_title, sa_session):')
                logging.critical('---------->>>>>>>>>>  Send Mail to %s' % recipient.email)
                logging.critical('---------->>>>>>>>>>  Dear, %s' % name)
                logging.critical('---------->>>>>>>>>>  email_subject : Email Notification for submitting Section %s of Permit # %s' % (Section_title, self.permit_no))

    def send_submitter_email_url_banpot(self, Section_title, email_subject, nemail_body, sa_session):
        forms = get_logbook_linked_forms(logbook_record=self)
        form_data_snapshot = forms[0].get_form_data_snapshot()
        submission_details = self.get_Section_submission_user_and_date(form_data_snapshot, Section_title)
        if submission_details and submission_details['SubmittedBy']:
            rc = Alchemy.find_recordclass('personnel')
            recipient = sa_session.query(rc).filter(sqlalchemy.and_(rc.email != None, rc.email != '', rc.j5username == submission_details['SubmittedBy'])).first()
            if recipient:
                name = recipient.lastname if recipient.lastname else recipient.j5username
                email_subject = 'Email Notification for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_body = 'Thank you for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_body += nemail_body
                email_greeting = 'Dear, %s<br/><br/>' % name
                self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')

    def send_submitter_email_url(self, Section_title, nemail_body, sa_session):
        forms = get_logbook_linked_forms(logbook_record=self)
        form_data_snapshot = forms[0].get_form_data_snapshot()
        submission_details = self.get_Section_submission_user_and_date(form_data_snapshot, Section_title)
        if submission_details and submission_details['SubmittedBy']:
            rc = Alchemy.find_recordclass('personnel')
            recipient = sa_session.query(rc).filter(sqlalchemy.and_(rc.email != None, rc.email != '', rc.j5username == submission_details['SubmittedBy'])).first()
            if recipient:
                name = recipient.lastname if recipient.lastname else recipient.j5username
                email_subject = 'Email Notification for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_body = 'Thank you for submitting Section %s of Permit # %s' % (Section_title, self.permit_no)
                email_body += nemail_body
                email_greeting = 'Dear, %s<br/><br/>' % name
                self.emailer.send(recipient.email, email_subject, email_greeting + email_body, contenttype='text/html')
                logging.critical('---------->>>>>>>>>>  send_submitter_email_url(self, Section_title, nemail_body, sa_session):')
                logging.critical('---------->>>>>>>>>>  Send Mail to %s' % recipient.email)
                logging.critical('---------->>>>>>>>>>  Dear, %s' % name)
                logging.critical('---------->>>>>>>>>>  email_subject : Email Notification for submitting Section %s of Permit # %s' % (Section_title, self.permit_no))

    def get_Section_submission_user_and_date(self, form_data_snapshot, Section_title):
        Section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['Title', 'SubmittedBy', 'SubmittedAt'])
        for e in Section_elements:
            if e.Title == Section_title:
                return e
        return [None, None]

    def get_section_approver_user_and_date(self, form_data_snapshot, Section_title):
        form_data_snapshot_t = form_data_snapshot
        logging.critical('---------->>>>>>>>>>  Section_elements, %s' % form_data_snapshot_t)
        Section_elements = beta_api_230.form_data_snapshot_query_sections(form_data_snapshot, ['ApprovedBy'])#APPROVED
        logging.critical('---------->>>>>>>>>>  Section_elements, %s' % Section_elements)
        for e in Section_elements:
            if e.Title == Section_title:
                return e
        return [None, None]

    def get_expanding_status(self):
        path_info = RequestStack.request_stack.environ.get('PATH_INFO')
        if path_info == "view/permits" or (path_info and '/expanded/' in path_info):
            return 'True'
        return 'False'
    expanding = property(get_expanding_status)

    def get_url_data(self, forms):
        url = self.logpage.logmodel.get_view_log_url(self.logid)
        if forms[0].uuid and url:
            url_start_length = url.find('/view/')
            if url_start_length > 0:
                url_start_length += 6
                url_end = "permits#Lv01/permits/%s/%s" % (self.logid, forms[0].uuid)
                url = url[:url_start_length] + url_end
                email_body = ' '
                if url:
                    email_body += ' Click <b><a href="%s">here</a></b> to view it ' % url
                    return email_body
        return None

class PTWLogModel(PermitToWork.PermitToWorkLogModel):
    def get_default_log_sa(self, defaults, session, kwargs):
        now = datetime_tz.datetime_tz.now()
        tomorrow = now + datetime_tz.timedelta(days=1)
        defaults.update({"valid_start": tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)})
        defaults.update({"valid_end": tomorrow.replace(hour=17, minute=0, second=0, microsecond=0)})
        # Apply the defaults
        default_row = self.logclass(**defaults)
        return default_row

