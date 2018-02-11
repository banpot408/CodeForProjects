from j5.Database import Alchemy
from j5.IndustraForms.api import get_logbook_linked_forms
from j5.IndustraForms import beta_api_230
from PTTGC.PermitToWork.DataSets.DataSetHelper import DataSetHelper
from sjsoft.Apps.Reports import Export
import logging

class ColdWorkDataSet(DataSetHelper):
    _PERMIT_HEADING_FIELDS_DATASET = 'permit_heading_fields'
    _PERMIT_DATETIME_FIELDS_DATASET = 'permit_datetime_fields'
    _PERMIT_SIGNATURE_AND_NAME_FIELDS_DATASET = 'permit_signature_and_name_fields'
    _OTHER_RELEVANT_DOCUMENTS_FIELDS_DATASET = 'other_relevant_documents_fields'
    _CERTIFICATE_FIELDS_DATASET = 'certificate_fields'
    _SAFETY_REQUIREMENTS_FIELDS_DATASET = 'safety_requirements_fields'
    _PERSONAL_PROTECTIVE_EQUIPMENT_REQUIRED_FIELDS_DATASET = 'personal_protective_equipment_required_fields'
    _GAS_MEASUREMENT_RESULTS_FIELDS_DATASET = 'gas_measurement_results_fields'
    _APPROVAL_NON_FLAMABLE_FIELDS_DATASET = 'approval_non_flamable_fields'
    _APPROVAL_FLAMABLE_FIELDS_DATASET = 'approval_flamable_fields'
    _COMMUNICATE_WITH_REQUESTOR_FIELDS_DATASET = 'communicate_with_requestor_fields'
    _GAS_DETECTION_FIELDS_DATASET = 'gas_detection_fields'
    _WORK_PERMIT_RENEWAL_FIELDS_DATASET = 'work_permit_renewal_fields'
    _CLOSE_WORK_PERMIT_FIELDS_DATASET = 'close_work_permit_fields'

    _SECTION_1_TITLE    = 'Contractors fill the information data and attach document for Work Permit'   # job owner
    _SECTION_2_TITLE    = 'Countersign / Cosign for high-risk job'                                      # job owner
    _SECTION_3_TITLE    = 'Cosigner approval for Work Permit'                                           # cosign
    _SECTION_4_TITLE    = 'Permit Issuer verify data'                                                   # Permit Issuer
    _SECTION_5_TITLE    = 'Permit Issuer preparation area'                                              # Permit Issuer
    _SECTION_6_TITLE    = 'Work Permit Approval'                                                        # Approve
    _SECTION_7_TITLE    = 'Communicate with Requestor'                                                  # Approve
    _SECTION_8_TITLE    = 'Renewal of Perrmit Request'                                                  # Permit Issuer
    _SECTION_9_TITLE    = 'Renewal of Perrmit'                                                          # Permit Issuer
    _SECTION_10_TITLE   = 'Close Permit'                                                                # Permit Issuer

    
    def create_metadata(self):

        permit_heading_fields = [
            Export.FieldMetaData('moc_no', None, 'str', 'Text211'),
            Export.FieldMetaData('permit_no', None, 'str', 'PermitNumber'),
            Export.FieldMetaData('applicant_name', None, 'str', 'Text1'),
            Export.FieldMetaData('contractor_company', None, 'str', 'Text2'),
            Export.FieldMetaData('phone_number', None, 'str', 'Text254'),
            Export.FieldMetaData('number_of_operators', None, 'int', 'Integer1'),
            Export.FieldMetaData('restricted_area', None, 'str', 'area1'),
            Export.FieldMetaData('control_area', None, 'str', 'area1'), #Choice61
            Export.FieldMetaData('workplace', None, 'str', 'Text220'),
            Export.FieldMetaData('device_name', None, 'str', 'Text3'),
            Export.FieldMetaData('device_number', None, 'str', 'Text4'),
            Export.FieldMetaData('description', None, 'str', 'Text225'),
            Export.FieldMetaData('area_hierarchy', None, 'str', 'Choice66'),              
            Export.FieldMetaData('job_owner_name', None, 'str', 'Text261')
        ]

        # Datetime Dataset fields
        permit_datetime_fields = [
            Export.FieldMetaData('header_from_date', None, 'datetime', 'DateTimeStart'),
            Export.FieldMetaData('header_to_date', None, 'datetime', 'DateTimeEnd'),
            Export.FieldMetaData('header_job_owner_signed_date', None, 'date', 'Date3'),
            Export.FieldMetaData('gas_measurement_datetime', None, 'datetime', 'DateTime87'),
            Export.FieldMetaData('approval_non_flamable_datetime', None, 'datetime', 'DateTime88'),
            Export.FieldMetaData('approval_flamable_datetime', None, 'datetime', 'DateTime90'),
            Export.FieldMetaData('approval_cosign_datetime', None, 'datetime', 'DateTime91'),
            Export.FieldMetaData('requestor_non_flamable_datetime', None, 'datetime', 'DateTime105'),
            Export.FieldMetaData('requestor_flamable_datetime', None, 'datetime', 'DateTime92'),
            Export.FieldMetaData('gas_detection_reading1', None, 'datetime', 'DateTime79'),
            Export.FieldMetaData('gas_detection_reading2', None, 'datetime', 'DateTime100'),
            Export.FieldMetaData('gas_detection_reading3', None, 'datetime', 'DateTime101'),
            Export.FieldMetaData('wp_renew_non_flamable_datetime', None, 'datetime', 'DateTime108'),
            Export.FieldMetaData('wp_permit_non_flamable_approver_datetime', None, 'datetime', 'DateTime107'),
            Export.FieldMetaData('wp_renew_flamable_datetime', None, 'datetime', 'DateTime97'),
            Export.FieldMetaData('wp_permit_flamable_approver_datetime', None, 'datetime', 'DateTime104'),
            Export.FieldMetaData('close_restore_license_datetime_non_flamable', None, 'datetime', 'DateTime36'),
            Export.FieldMetaData('close_audit_accept_datetime_non_flamable', None, 'datetime', 'DateTime38'),
            Export.FieldMetaData('close_restore_license_datetime_flamable', None, 'datetime', 'DateTime94'),
            Export.FieldMetaData('close_audit_accept_datetime_flamable', None, 'datetime', 'DateTime99')
        ]

        # # Datetime Dataset fields
        # permit_signature_and_name_fields = [
        #     Export.FieldMetaData('approval_non_flamable_name_section_4_or_5', None, 'any', 'section4_user'),        # Job Owner   date
        #     Export.FieldMetaData('approval_non_flamable_signature_section_4_or_5', None, 'any', 'section5_user'),   # Cosign
        #     Export.FieldMetaData('approval_non_flamable_name_section_6', None, 'any', 'section6_user'),             # Issuer
        #     Export.FieldMetaData('approval_non_flamable_signature_section_6', None, 'any', 'section11_user'),       # Approver
        #     Export.FieldMetaData('wp_name_section_11_or_12', None, 'any', 'section12_user'),
        #     Export.FieldMetaData('wp_signature_section_11_or_12', None, 'any', 'section12_user')
        # ]

        # # Datetime Dataset fields
        # permit_signature_and_name_fields = [
        #     Export.FieldMetaData('approval_non_flamable_name_section_4_or_5', None, 'date', 'section4_user'),        # Job Owner   date
        #     Export.FieldMetaData('approval_non_flamable_signature_section_4_or_5', None, 'datetime', 'section4_user'),   # Cosign
        #     Export.FieldMetaData('approval_non_flamable_name_section_6', None, 'any', 'section6_user'),             # Issuer
        #     Export.FieldMetaData('approval_non_flamable_signature_section_6', None, 'any', 'section11_user'),       # Approver
        #     Export.FieldMetaData('wp_name_section_11_or_12', None, 'any', 'section12_user'),
        #     Export.FieldMetaData('wp_signature_section_11_or_12', None, 'any', 'section12_user')
        # ]

        permit_signature_and_name_fields = [
            Export.FieldMetaData('contractor_submit_name', None, 'str', 'section1_approval_user'),
            Export.FieldMetaData('contractor_submit_datetime', None, 'datetime', 'section1_approval_datetime'),
            Export.FieldMetaData('job_owner_submit_name', None, 'str', 'section2_user'),
            Export.FieldMetaData('job_owner_submit_datetime', None, 'datetime', 'section2_datetime'),
            Export.FieldMetaData('cosign_submit_name', None, 'str', 'section3_user'),
            Export.FieldMetaData('cosign_submit_datetime', None, 'datetime', 'section3_datetime'),
            Export.FieldMetaData('permit_issuer_verify_name', None, 'str', 'section4_approval_user'),
            Export.FieldMetaData('permit_issuer_verify_datetime', None, 'datetime', 'section4_approval_datetime'),
            Export.FieldMetaData('permit_issuer_submit_name', None, 'str', 'section5_approval_user'),
            Export.FieldMetaData('permit_issuer_submit_datetime', None, 'datetime', 'section5_approval_datetime'),
            Export.FieldMetaData('permit_approve_submit_name', None, 'str', 'section6_user'),
            Export.FieldMetaData('permit_approve_submit_datetime', None, 'datetime', 'section6_datetime'),
            Export.FieldMetaData('communicate_requestor_name', None, 'str', 'section7_user'),
            Export.FieldMetaData('communicate_requestor_datetime', None, 'datetime', 'section7_datetime'),
            Export.FieldMetaData('renewal_permit_request_name', None, 'str', 'section8_user'),
            Export.FieldMetaData('renewal_permit_request', None, 'datetime', 'section8_datetime'),
            Export.FieldMetaData('renewal_permit_submit_name', None, 'str', 'section9_user'),
            Export.FieldMetaData('renewal_permit_submit_datetime', None, 'datetime', 'section9_datetime'),
            Export.FieldMetaData('Close_Permit_submit_name', None, 'str', 'section10_user'),
            Export.FieldMetaData('Close_Permit_submit_datetime', None, 'datetime', 'section10_datetime')
        ]



        # Certificate Dataset fields
        certificate_fields = [
            Export.FieldMetaData('confined_space_certificate_no', None, 'str', 'confined_space_certificate_no'),
            Export.FieldMetaData('crane_lifting_certificate_no', None, 'str', 'crane_lifting_certificate_no'),
            Export.FieldMetaData('excavation_certificate_no', None, 'str', 'excavation_certificate_no'),
            Export.FieldMetaData('box_up_certificate_no', None, 'str', 'box_up_certificate_no'),
            Export.FieldMetaData('radiography_certificate_no', None, 'str', 'radiography_certificate_no'),
            Export.FieldMetaData('diving_certificate_no', None, 'str', 'diving_certificate_no'),
            Export.FieldMetaData('scaffolding_certificate_no', None, 'str', 'scaffolding_certificate_no'),
            Export.FieldMetaData('road_close_certificate_no', None, 'str', 'road_close_certificate_no'),
            Export.FieldMetaData('nearby_high_voltage_certificate_no', None, 'str', 'nearby_high_voltage_certificate_no')
        ]
        logging.critical('++++++++++++++++++++++++++ certificate_fields ************************* %s' % certificate_fields )
        # other_relevant_documents Dataset fields
        other_relevant_documents_fields = [
            Export.FieldMetaData('jsea_safety_environment', None, 'str', 'Text234'),
            Export.FieldMetaData('p_id_route_attachment', None, 'str', 'Text235'),
            Export.FieldMetaData('p_id_route', None, 'str', 'Text235'),
            Export.FieldMetaData('safety_datasheet', None, 'str', 'Text16'),
            Export.FieldMetaData('safety_datasheet_attachment', None, 'str', 'Text16'),
            Export.FieldMetaData('other_title', None, 'str', 'Text236'),
            Export.FieldMetaData('job_description', None, 'str', 'Choice62'),
            Export.FieldMetaData('job_owner_integer41', None, 'int', 'Integer41'),
            Export.FieldMetaData('surname', None, 'str', 'Text204')
        ]
        logging.critical('++++++++++++++++++++++++++ other_relevant_documents_fields ************************* %s' % other_relevant_documents_fields )
        
        # safety_requirements Dataset fields
        safety_requirements_fields = [
            Export.FieldMetaData('last_used_device_condition', None, 'str', 'Text22'),
            Export.FieldMetaData('device_paused_checklist', None, 'str', 'ChecklistItem125'),
            Export.FieldMetaData('device_cut_off_check', None, 'str', 'Checkbox17'),
            Export.FieldMetaData('device_cut_off_text', None, 'str', 'Text23'),
            Export.FieldMetaData('is_pressure_our_checklist', None, 'str', 'ChecklistItem126'),
            Export.FieldMetaData('attach_logic_control_diagram', None, 'str', 'Text24'),
            Export.FieldMetaData('liquid_is_released_checklist', None, 'str', 'ChecklistItem127'),
            Export.FieldMetaData('isolation_plan_check', None, 'str', 'Checkbox18'),
            Export.FieldMetaData('not_attached_logic_control_diagram', None, 'str', 'Text25'),
            Export.FieldMetaData('liquid_residues_checklistitem', None, 'str', 'ChecklistItem128'),
            Export.FieldMetaData('pressure_drop_checklistitem', None, 'str', 'ChecklistItem129'),
            Export.FieldMetaData('local_switch_check', None, 'str', 'Checkbox19'),
            Export.FieldMetaData('by_pass', None, 'str', 'Text26'),
            Export.FieldMetaData('pipe_has_been_cut_checklistitem', None, 'str', 'ChecklistItem130'),
            Export.FieldMetaData('breaker_check', None, 'str', 'Checkbox20'),
            Export.FieldMetaData('breaker', None, 'str', 'Text27'),
            Export.FieldMetaData('equipment_cleaned_checklistitem', None, 'str', 'ChecklistItem131'),
            Export.FieldMetaData('other_breaker', None, 'str', 'Text191'),
            Export.FieldMetaData('remove_pipe_joints_checklistitem', None, 'str', 'ChecklistItem132'),
            Export.FieldMetaData('cleaning_with_nitrogen_checklistitem', None, 'str', 'ChecklistItem133'),
            Export.FieldMetaData('attach_electric_plan_check', None, 'str', 'Checkbox21'),
            Export.FieldMetaData('steam_cleaning_checklistitem', None, 'str', 'ChecklistItem134'),
            Export.FieldMetaData('no_electricity_plan_check', None, 'str', 'Checkbox22'),
            Export.FieldMetaData('cleaning_the_water_checklistitem', None, 'str', 'ChecklistItem135'),
            Export.FieldMetaData('electrical_equipment_cut_checklistitem', None, 'str', 'ChecklistItem136'),
            Export.FieldMetaData('defeat_check', None, 'str', 'Checkbox23'),
            Export.FieldMetaData('defeat', None, 'str', 'Text30'),
            Export.FieldMetaData('other_defeat_checklistitem', None, 'str', 'ChecklistItem137'),
            Export.FieldMetaData('by_pass_check', None, 'str', 'Checkbox26'),
            Export.FieldMetaData('sparking_block_fireproof_cover', None, 'str', 'Text31'),
            Export.FieldMetaData('by_pass_description', None, 'str', 'Text230'),
            Export.FieldMetaData('attach_logic_control_diagram_check', None, 'str', 'Checkbox24'),
            Export.FieldMetaData('make_on_site_verifier_checklistitem', None, 'str', 'ChecklistItem138'),
            Export.FieldMetaData('not_attach_logic_control_diagram_check', None, 'str', 'Checkbox25'),
            Export.FieldMetaData('contact_on_site_verifier', None, 'str', 'Text227'),
            Export.FieldMetaData('recommended_actions', None, 'str', 'Text194'),
            Export.FieldMetaData('block_work_area_check', None, 'str', 'Checkbox27'),
            Export.FieldMetaData('personal_gas_meter_check', None, 'str', 'Checkbox36'),
            Export.FieldMetaData('personal_gas_meter', None, 'str', 'Text33'),
            Export.FieldMetaData('cover_drain_in_radius_check', None, 'str', 'Checkbox28'),
            Export.FieldMetaData('connect_spray_line_check', None, 'str', 'Checkbox37'),
            Export.FieldMetaData('prepare_ventilator_check', None, 'str', 'Checkbox29'),
            Export.FieldMetaData('warning_signs_check', None, 'str', 'Checkbox38'),
            Export.FieldMetaData('water_spray_baffle_check', None, 'str', 'Checkbox30'),
            Export.FieldMetaData('leaky_hydrocarbon_stop_working_check', None, 'str', 'Checkbox39'),
            Export.FieldMetaData('sparking_block_fireproof_cover_check', None, 'str', 'Checkbox31'),
            Export.FieldMetaData('do_not_release_liquid_check', None, 'str', 'Checkbox40'),
            Export.FieldMetaData('fire_extinguishers_in_work_area_check', None, 'str', 'Checkbox32'),
            Export.FieldMetaData('communicate_with_staff_check', None, 'str', 'Checkbox41'),
            Export.FieldMetaData('standby_fire_extinguisher_check', None, 'str', 'Checkbox33'),
            Export.FieldMetaData('destroy_pyrophoric_substances_check', None, 'str', 'Checkbox42'),
            Export.FieldMetaData('eye_washer_availability_check', None, 'str', 'Checkbox34'),
            Export.FieldMetaData('be_careful_side_effects_check', None, 'str', 'Checkbox43'),
            Export.FieldMetaData('drill_pipe_gas_detection_check', None, 'str', 'Checkbox35'),
            Export.FieldMetaData('other_safety_requirements_check', None, 'str', 'Checkbox44'),
            Export.FieldMetaData('other_safety_requirements', None, 'str', 'Text34'),
            Export.FieldMetaData('data_to_tag_cut', None, 'str', 'Text229'),
            Export.FieldMetaData('data_to_onsite', None, 'str', 'Text230'),
            Export.FieldMetaData('more_caution', None, 'str', 'Text196')
        ]

        # personal_protective_equipment_required Dataset fields
        personal_protective_equipment_required_fields = [
            Export.FieldMetaData('standard_ppe_check', None, 'str', 'Checkbox50'),
            Export.FieldMetaData('safety_glasses_check', None, 'str', 'Checkbox54'),
            Export.FieldMetaData('chemical_mask_check', None, 'str', 'Checkbox51'),
            Export.FieldMetaData('full_body_harness_check', None, 'str', 'Checkbox55'),
            Export.FieldMetaData('ear_plugs_check', None, 'str', 'Checkbox52'),
            Export.FieldMetaData('dust_prevention_kit_check', None, 'str', 'Checkbox56'),
            Export.FieldMetaData('glove_check', None, 'str', 'Checkbox53'),
            Export.FieldMetaData('chemical_protection_suit_check', None, 'str', 'Checkbox57'),
            Export.FieldMetaData('other_ppe_check', None, 'str', 'Checkbox58'),
            Export.FieldMetaData('other_ppe', None, 'str', 'Text41')
        ]

        # gas_measurement_results Dataset fields
        gas_measurement_results_fields = [
            Export.FieldMetaData('agt_choice', None, 'str', 'Choice57'),
            Export.FieldMetaData('lel_frequency', None, 'float', 'Number184'),
            Export.FieldMetaData('o2_frequency', None, 'float', 'Number185'),
            Export.FieldMetaData('h2o_frequency', None, 'float', 'Number186'),
            Export.FieldMetaData('co_frequency', None, 'float', 'Number187'),
            Export.FieldMetaData('other_frequency', None, 'float', 'Number188'),
            Export.FieldMetaData('lel_standard', None, 'int', 'Integer19'),
            Export.FieldMetaData('o2_standard', None, 'int', 'Integer20'),
            Export.FieldMetaData('h2o_standard', None, 'int', 'Integer21'),
            Export.FieldMetaData('co_standard', None, 'int', 'Integer22'),
            Export.FieldMetaData('other_standard', None, 'int', 'Integer23'),
            Export.FieldMetaData('gas_measurement_other', None, 'str', 'Text215'),
            Export.FieldMetaData('gas_measurement_na', None, 'str', 'Text203')
        ]

        # approval_non_flamable Dataset fields
        approval_non_flamable_fields = [
            Export.FieldMetaData('non_flamable_employee_number', None, 'int', 'Integer45'),
            Export.FieldMetaData('non_flamable_surname', None, 'str', 'Text209'),
            Export.FieldMetaData('non_flamable_validated_check', None, 'str', 'Checkbox65')
        ]

        # approval_flamable Dataset fields
        approval_flamable_fields = [
            Export.FieldMetaData('flamable_employee_number', None, 'int', 'Integer46'),
            Export.FieldMetaData('flamable_employee_surname', None, 'str', 'Text210'),
            Export.FieldMetaData('flamable_validated_check', None, 'str', 'Checkbox67'),
            Export.FieldMetaData('permit_requires_co_sign_checklistitem', None, 'str', 'ChecklistItem143'),
            Export.FieldMetaData('employee_coordinator_code', None, 'int', 'Integer42'),
            Export.FieldMetaData('employee_coordinator_surname', None, 'str', 'Choice65'),
            Export.FieldMetaData('cosign_validated', None, 'str', 'Checkbox68')
        ]

        # communicate_with_requestor Dataset fields
        communicate_with_requestor_fields = [
            Export.FieldMetaData('requestor_non_flamable_check', None, 'str', 'Checkbox66'),
            Export.FieldMetaData('requesto_flamable_check', None, 'str', 'Checkbox69'),
            Export.FieldMetaData('requestor_supervisor_non_flamable', None, 'str', 'Text228'),
            Export.FieldMetaData('requestor_supervisor_flamable', None, 'str', 'Label765'),
            Export.FieldMetaData('requestor_verifier_non_flamable', None, 'str', 'Text231'),
            Export.FieldMetaData('requestor_verifier_flamable', None, 'str', 'Label768')
        ]

        # gas_detection Dataset fields
        gas_detection_fields = [
            Export.FieldMetaData('lel_reading1', None, 'int', 'Integer2'),
            Export.FieldMetaData('o2_reading1', None, 'int', 'Integer7'),
            Export.FieldMetaData('h2o_reading1', None, 'int', 'Integer17'),
            Export.FieldMetaData('co_reading1', None, 'int', 'Integer18'),
            Export.FieldMetaData('other_reading1', None, 'int', 'Integer28'),
            Export.FieldMetaData('agt_reading1', None, 'str', 'Text216'),
            Export.FieldMetaData('lel_reading2', None, 'int', 'Integer24'),
            Export.FieldMetaData('o2_reading2', None, 'int', 'Integer25'),
            Export.FieldMetaData('h2o_reading2', None, 'int', 'Integer26'),
            Export.FieldMetaData('co_reading2', None, 'int', 'Integer27'),
            Export.FieldMetaData('other_reading2', None, 'int', 'Integer29'),
            Export.FieldMetaData('agt_reading2', None, 'str', 'Text223'),
            Export.FieldMetaData('lel_reading3', None, 'int', 'Integer30'),
            Export.FieldMetaData('o2_reading3', None, 'int', 'Integer31'),
            Export.FieldMetaData('h2o_reading3', None, 'int', 'Integer32'),
            Export.FieldMetaData('co_reading3', None, 'int', 'Integer33'),
            Export.FieldMetaData('other_reading3', None, 'int', 'Integer34'),
            Export.FieldMetaData('agt_reading3', None, 'str', 'Text224')
        ]

        # work_permit_renewal Dataset fields
        work_permit_renewal_fields = [
            Export.FieldMetaData('renew_license', None, 'str', 'ChecklistItem140'),
            Export.FieldMetaData('renew_non_flamable_employee_number', None, 'int', 'Integer43'),
            Export.FieldMetaData('renew_non_flamable_surname', None, 'str', 'Text207'),
            Export.FieldMetaData('permit_non_flamable_approver_check', None, 'str', 'Checkbox74'),
            Export.FieldMetaData('renew_flamable_employee_number', None, 'int', 'Integer44'),
            Export.FieldMetaData('renew_flamable_surname', None, 'str', 'Text239'),
            Export.FieldMetaData('permit_flamable_approver_check', None, 'str', 'Checkbox75'),
            Export.FieldMetaData('supervisor_acknowledged_non_flamable', None, 'str', 'Text237'),
            Export.FieldMetaData('supervisor_acknowledged_flamable', None, 'str', 'Text237')
        ]

        # close_work_permit Dataset fields
        close_work_permit_fields = [
            Export.FieldMetaData('lock_removed_non_flamable_checklistitem', None, 'str', 'ChecklistItem142'),
            Export.FieldMetaData('lock_removed_not_reason_non_flamable', None, 'str', 'Text197'),
            Export.FieldMetaData('license_closing_non_flamable_check', None, 'str', 'Checkbox70'),
            Export.FieldMetaData('work_complete_non_flamable_check', None, 'str', 'Checkbox71'),
            Export.FieldMetaData('unfinished_work_reason_non_flamable', None, 'str', 'Text54'),
            Export.FieldMetaData('restore_license_supervisor_non_flamable', None, 'str', 'Text56'),
            Export.FieldMetaData('audit_accept_non_flamable_check', None, 'str', 'Checkbox76'),
            Export.FieldMetaData('audit_accept_no_reason_non_flamable_check', None, 'str', 'Checkbox77'),
            Export.FieldMetaData('audit_accept_no_reason_non_flamable', None, 'str', 'Text55'),
            Export.FieldMetaData('lock_removed_flamable_checklistitem', None, 'str', 'ChecklistItem142'),
            Export.FieldMetaData('lock_removed_not_reason_flamable', None, 'str', 'Text198'),
            Export.FieldMetaData('license_closing_flamable_check', None, 'str', 'Checkbox70'),
            Export.FieldMetaData('work_complete_flamable_check', None, 'str', 'Checkbox71'),
            Export.FieldMetaData('unfinished_work_reason_flamable', None, 'str', 'Text199'),
            Export.FieldMetaData('restore_license_supervisor_flamable', None, 'str', 'Text200'),
            Export.FieldMetaData('audit_accept_flamable_check', None, 'str', 'Checkbox76'),
            Export.FieldMetaData('audit_accept_no_reason_flamable_check', None, 'str', 'Checkbox77'),
            Export.FieldMetaData('audit_accept_no_reason_flamable', None, 'str', 'Text202'),
            Export.FieldMetaData('permit_issuer_non_flamable', None, 'str', 'Label799'),
            Export.FieldMetaData('permit_issuer_flamable', None, 'str', 'Text232')
        ]

        metadata = [Export.DataSetMetaData('permit_heading_fields.csv', self._PERMIT_HEADING_FIELDS_DATASET, permit_heading_fields)]
        metadata.extend([Export.DataSetMetaData('permit_datetime_fields.csv', self._PERMIT_DATETIME_FIELDS_DATASET, permit_datetime_fields)])
        metadata.extend([Export.DataSetMetaData('permit_signature_and_name_fields.csv', self._PERMIT_SIGNATURE_AND_NAME_FIELDS_DATASET, permit_signature_and_name_fields)])
        metadata.extend([Export.DataSetMetaData('certificate_fields.csv', self._CERTIFICATE_FIELDS_DATASET, certificate_fields)])
        metadata.extend([Export.DataSetMetaData('other_relevant_documents_fields.csv', self._OTHER_RELEVANT_DOCUMENTS_FIELDS_DATASET, other_relevant_documents_fields)])
        metadata.extend([Export.DataSetMetaData('safety_requirements_fields.csv',self._SAFETY_REQUIREMENTS_FIELDS_DATASET, safety_requirements_fields)])
        metadata.extend([Export.DataSetMetaData('personal_protective_equipment_required_fields.csv',self._PERSONAL_PROTECTIVE_EQUIPMENT_REQUIRED_FIELDS_DATASET, personal_protective_equipment_required_fields)])
        metadata.extend([Export.DataSetMetaData('gas_measurement_results_fields.csv', self._GAS_MEASUREMENT_RESULTS_FIELDS_DATASET, gas_measurement_results_fields)])
        metadata.extend([Export.DataSetMetaData('approval_non_flamable_fields.csv', self._APPROVAL_NON_FLAMABLE_FIELDS_DATASET, approval_non_flamable_fields)])
        metadata.extend([Export.DataSetMetaData('approval_flamable_fields.csv', self._APPROVAL_FLAMABLE_FIELDS_DATASET, approval_flamable_fields)])
        metadata.extend([Export.DataSetMetaData('communicate_with_requestor_fields.csv', self._COMMUNICATE_WITH_REQUESTOR_FIELDS_DATASET, communicate_with_requestor_fields)])
        metadata.extend([Export.DataSetMetaData('gas_detection_fields.csv', self._GAS_DETECTION_FIELDS_DATASET, gas_detection_fields)])
        metadata.extend([Export.DataSetMetaData('work_permit_renewal_fields.csv', self._WORK_PERMIT_RENEWAL_FIELDS_DATASET, work_permit_renewal_fields)])
        metadata.extend([Export.DataSetMetaData('close_work_permit_fields.csv', self._CLOSE_WORK_PERMIT_FIELDS_DATASET, close_work_permit_fields)])

        return metadata

    def generate_datasets(self, sa_session, params, locale, timezone):
        datasets = {}
        permit_logid = params.get('permit_logid')
        if permit_logid:
            snapshot = self.get_form_snapshot(sa_session, permit_logid)
            # permit_heading
            datasets[self._PERMIT_HEADING_FIELDS_DATASET] = self.get_permit_heading_fields_dataset(permit_logid, snapshot, self._PERMIT_HEADING_FIELDS_DATASET, sa_session)
            # permit_datetimes
            datasets[self._PERMIT_DATETIME_FIELDS_DATASET] = self.get_permit_datetime_fields_dataset(permit_logid, snapshot, self._PERMIT_DATETIME_FIELDS_DATASET, sa_session)
            # permit_signatures and names
            datasets[self._PERMIT_SIGNATURE_AND_NAME_FIELDS_DATASET] = self.get_permit_signature_and_name_fields_dataset(permit_logid, snapshot, self._PERMIT_SIGNATURE_AND_NAME_FIELDS_DATASET, sa_session)
            # certificate_fields
            datasets[self._CERTIFICATE_FIELDS_DATASET] = self.get_certificate_fields_dataset(permit_logid, snapshot, self._CERTIFICATE_FIELDS_DATASET, sa_session)
            # other_relevant_documents
            datasets[self._OTHER_RELEVANT_DOCUMENTS_FIELDS_DATASET] = self.get_other_relevant_documents_fields_dataset(permit_logid, snapshot, self._OTHER_RELEVANT_DOCUMENTS_FIELDS_DATASET, sa_session)
            # safety_requirements
            datasets[self._SAFETY_REQUIREMENTS_FIELDS_DATASET] = self.get_safety_requirements_fields_dataset(permit_logid, snapshot, self._SAFETY_REQUIREMENTS_FIELDS_DATASET, sa_session)
            # personal_protective_equipment_required
            datasets[self._PERSONAL_PROTECTIVE_EQUIPMENT_REQUIRED_FIELDS_DATASET] = self.get_personal_protective_equipment_required_fields_dataset(permit_logid, snapshot, self._PERSONAL_PROTECTIVE_EQUIPMENT_REQUIRED_FIELDS_DATASET, sa_session)
            # gas_measurement_results
            datasets[self._GAS_MEASUREMENT_RESULTS_FIELDS_DATASET] = self.get_gas_measurement_results_fields_dataset(permit_logid, snapshot, self._GAS_MEASUREMENT_RESULTS_FIELDS_DATASET, sa_session)
            # approval_non_flamable
            datasets[self._APPROVAL_NON_FLAMABLE_FIELDS_DATASET] = self.get_approval_non_flamable_fields_dataset(permit_logid, snapshot, self._APPROVAL_NON_FLAMABLE_FIELDS_DATASET, sa_session)
            # approval_flamable
            datasets[self._APPROVAL_FLAMABLE_FIELDS_DATASET] = self.get_approval_flamable_fields_dataset(permit_logid, snapshot, self._APPROVAL_FLAMABLE_FIELDS_DATASET, sa_session)
            # communicate_with_requestor
            datasets[self._COMMUNICATE_WITH_REQUESTOR_FIELDS_DATASET] = self.get_communicate_with_requestor_fields_dataset(permit_logid, snapshot, self._COMMUNICATE_WITH_REQUESTOR_FIELDS_DATASET, sa_session)
            # gas_detection
            datasets[self._GAS_DETECTION_FIELDS_DATASET] = self.get_gas_detection_fields_dataset(permit_logid, snapshot, self._GAS_DETECTION_FIELDS_DATASET, sa_session)
            # work_permit_renewal
            datasets[self._WORK_PERMIT_RENEWAL_FIELDS_DATASET] = self.get_work_permit_renewal_fields_dataset(permit_logid, snapshot, self._WORK_PERMIT_RENEWAL_FIELDS_DATASET, sa_session)
            # close_work_permit
            datasets[self._CLOSE_WORK_PERMIT_FIELDS_DATASET] = self.get_close_work_permit_fields_dataset(permit_logid, snapshot, self._CLOSE_WORK_PERMIT_FIELDS_DATASET, sa_session)
        return datasets

    def get_special_field_value(self, permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session):
        value = super(ColdWorkDataSet, self).get_special_field_value(permit_logid, field_name, display_name, value, dataset, industraform_values, snapshot, sa_session)
        if field_name == 'area_hierarchy':
            value = self.get_area_hierarchy_value(value)
        return value

          
        

    @staticmethod
    def get_area_hierarchy_value(area_list_str):
        if not area_list_str:
            return
    #   value = area_list_str.replace("u'", "").replace("'", "").strip("[").strip("]")
        value = area_list_str.replace("u'", "").replace("'", " ").replace(",", "  > ").strip("[").strip("]")
        return value

    def get_permit_heading_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        logging.critical("************************************************************************************* heading dataset = %s" % dataset)
        return dataset

    def get_permit_heading_fields_dataset_3(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        logging.info("heading dataset = %s" % dataset)
        return dataset

    def get_permit_datetime_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session, use_display_value=False)
        return dataset

    #self.print_approvals_user('Cosigner approval for Work Permit', sa_session) _SECTION_9_TITLE
    def get_permit_signature_and_name_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        logging.critical('************************************** get_permit_signature_and_name_fields_dataset, %s' % self._SECTION_1_TITLE)
        logging.critical('************************************** get_permit_signature_and_name_fields_dataset, %s' % self._SECTION_4_TITLE)
        logging.critical('************************************** get_permit_signature_and_name_fields_dataset, %s' % self._SECTION_5_TITLE)
        section1_approval_user, section1_approval_datetime    = self.get_section_approvals_user(snapshot, self._SECTION_1_TITLE, sa_session)
        section2_user, section2_datetime    = self.get_full_name_and_datetime(snapshot, self._SECTION_2_TITLE, sa_session)
        section3_user, section3_datetime    = self.get_section_approvals_user(snapshot, self._SECTION_3_TITLE, sa_session)
        section4_user, section4_datetime    = self.get_full_name_and_datetime(snapshot, self._SECTION_4_TITLE, sa_session)
        section5_user, section5_datetime    = self.get_full_name_and_datetime(snapshot, self._SECTION_5_TITLE, sa_session)
        section6_user, section6_datetime    = self.get_section_approvals_user(snapshot, self._SECTION_6_TITLE, sa_session)
        section7_user, section7_datetime    = self.get_full_name_and_datetime(snapshot, self._SECTION_7_TITLE, sa_session)
        section8_user, section8_datetime    = self.get_full_name_and_datetime(snapshot, self._SECTION_8_TITLE, sa_session)
        section9_user, section9_datetime    = self.get_section_approvals_user(snapshot, self._SECTION_9_TITLE, sa_session)
        section10_user, section10_datetime  = self.get_section_approvals_user(snapshot, self._SECTION_10_TITLE, sa_session)
        section4_approval_user, section4_approval_datetime  = self.get_section_approvals_user(snapshot, self._SECTION_5_TITLE, sa_session)
        section5_approval_user, section5_approval_datetime  = self.get_section_approvals_user(snapshot, self._SECTION_5_TITLE, sa_session)
        dataset = self.get_header_row(dataset)
        colum_values = [section1_approval_user,     #
                        section1_approval_datetime, #
                        section2_user,     #
                        section2_datetime, #
                        section3_user,     #
                        section3_datetime, #
                        section4_approval_user,
                        section4_approval_datetime,
                        section5_approval_user,
                        section5_approval_datetime,
                        section6_user,
                        section6_datetime,
                        section7_user,
                        section7_datetime,
                        section8_user,
                        section8_datetime,
                        section9_user,
                        section9_datetime,
                        section10_user,
                        section10_datetime
                        ]
        logging.critical('++++++++++++++++++++++++++ section1_approval_user         *** %s'     % section1_approval_user)
        logging.critical('++++++++++++++++++++++++++ section1_approval_datetime     *** %s'     % section1_approval_datetime)
        logging.critical('++++++++++++++++++++++++++ section3_approval_user         *** %s'     % section3_user)
        logging.critical('++++++++++++++++++++++++++ section3_approval_datetime     *** %s'     % section3_datetime)
        logging.critical('++++++++++++++++++++++++++ section4_approval_user         *** %s'     % section4_approval_user)
        logging.critical('++++++++++++++++++++++++++ section4_approval_datetime     *** %s'     % section4_approval_datetime)
        logging.critical('++++++++++++++++++++++++++ section5_approval_user         *** %s'     % section5_approval_user)
        logging.critical('++++++++++++++++++++++++++ section5_approval_datetime     *** %s'     % section5_approval_datetime)
        logging.critical('++++++++++++++++++++++++++ section9_approval_user         *** %s'     % section9_user)
        logging.critical('++++++++++++++++++++++++++ section9_approval_datetime     *** %s'     % section9_datetime)
        logging.critical('++++++++++++++++++++++++++ section10_approval_user         *** %s'     % section10_user)
        logging.critical('++++++++++++++++++++++++++ section10_approval_datetime     *** %s'     % section10_datetime)
        dataset.append(colum_values)
        return dataset



    def get_certificate_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        certificates = self.get_linked_certificates(permit_logid, sa_session)
        dataset = self.get_header_row(dataset)
        column_values = [
            certificates.get('confined_space_certificate_no', ''),
            certificates.get('crane_lifting_certificate_no', ''),
            certificates.get('excavation_certificate_no', ''),
            certificates.get('box_up_certificate_no', ''),
            certificates.get('radiography_certificate_no', ''),
            certificates.get('diving_certificate_no', ''),
            certificates.get('scaffolding_certificate_no', ''),
            certificates.get('road_close_certificate_no', ''),
            certificates.get('nearby_high_voltage_certificate_no', '')
        ]
        dataset.append(column_values)
        return dataset

    def get_other_relevant_documents_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_safety_requirements_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_personal_protective_equipment_required_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_gas_measurement_results_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_approval_non_flamable_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_approval_flamable_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_communicate_with_requestor_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_gas_detection_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_work_permit_renewal_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset

    def get_close_work_permit_fields_dataset(self, permit_logid, snapshot, dataset, sa_session):
        dataset = self.get_dataset_field_values(permit_logid, snapshot, dataset, sa_session)
        return dataset





Plugin = ColdWorkDataSet
