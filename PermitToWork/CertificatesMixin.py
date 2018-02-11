from j5.Database import Alchemy
from sjsoft.Library.BirtReports import BirtReportsMixin
import logging


class CertificatesMixin(BirtReportsMixin):

    PTGCC_SCAFFOLDING_FILENAME = "PTTGC.PermitToWork.scaffolding"
    PTGCC_CONFINED_SPACE_ENTRY_FILENAME = "PTTGC.PermitToWork.confined_space_entry"

    def generate_report(self, sa_session, params=None, output_format="pdf", locale=None, timezone=None, **kwargs):
        logging.critical("Setting the certificate_logid parameter to %s " % self.logid)
        params = {}

        report_config_logclass = Alchemy.find_recordclass('report_config')
        report_type = self.get_report_type()
        logging.critical("-----------------------report_type  %s " % report_type)
        if report_type == 'SCAFFOLDING':
            params['type'] = report_type
            report_config = sa_session.query(report_config_logclass).filter(report_config_logclass.filename == self.PTGCC_SCAFFOLDING_FILENAME).first()
        elif report_type == 'CONFINED_SPACE_ENTRY':
            logging.critical("-----------------------CONFINED_SPACE_ENTRY  ")
            params['type'] = report_type
            report_config = sa_session.query(report_config_logclass).filter(report_config_logclass.filename == self.PTGCC_CONFINED_SPACE_ENTRY_FILENAME).first()
            logging.critical("-----------------------else CONFINED_SPACE_ENTRY  ")
        else:
            report_config = None
        params['permit_logid'] = self.logid
        #logging.critical("-----------------------generate_report %s " % self._generate_report(sa_session, report_config, None, None, view_only=True, params=params))
        return self._generate_report(sa_session, report_config, None, None, view_only=True, params=params)

    def _generate_report(self, sa_session, report_config, timezone=None, locale=None, view_only=False, params=None):
        data = report_config.generate_report(sa_session, params=params, output_format="pdf", timezone=timezone, locale=locale)
        logging.critical("-----------------------data Get generate_report %s " % data)
        if report_config.archive_report == 'True' and not view_only:
            self._archive_report(sa_session, report_config, data, params, self.finish_time)

        return data

    def get_report_type(self):
        permit_forms_rc = Alchemy.find_recordclass('permit_forms')
        sf_form_register_rc = Alchemy.find_recordclass('sf_form_register')

        with Alchemy.closing(self.session_class()) as sa_session:
            scaffolding_type = sa_session.query(permit_forms_rc.logid).filter(
                permit_forms_rc.form_register_logid == sf_form_register_rc.logid,
                sf_form_register_rc.form_name == self.PTGCC_SCAFFOLDING_FILENAME).first()
            if scaffolding_type and self.certificate_type == scaffolding_type.logid:
                return 'SCAFFOLDING'

            confined_space_entry_type = sa_session.query(permit_forms_rc.logid).filter(
                permit_forms_rc.form_register_logid == sf_form_register_rc.logid,
                sf_form_register_rc.form_name == self.PTGCC_CONFINED_SPACE_ENTRY_FILENAME).first()
            if confined_space_entry_type and self.certificate_type == confined_space_entry_type.logid:
                return 'CONFINED_SPACE_ENTRY'

        return None

    report_type = property(get_report_type)