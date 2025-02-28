import os
from pprint import pprint
from docxtpl import DocxTemplate
from num2words import num2words
from src.db.models import Photosession, Contract

#TODO add function to create dict from Contract
def serialize_contract_dict(contract: Contract) -> dict:
    contract_dict = {

    }
    return contract_dict



async def serialize_photosession_dict(photosession: Photosession) -> dict:
    print('++++' * 30)
    pprint(photosession.contract.photographer.__dict__)
    photosession_dict = {
        'photographer_fullname': photosession.contract.photographer.full_name,
        'photographer_adress': photosession.contract.photographer.adress,
        # 'photographer_opf_full': photosession.contract.photographer.opf_full,
        'photographer_kpp': photosession.contract.photographer.kpp,
        'photographer_ogrnip': photosession.contract.photographer.ogrnip,
        'photographer_inn': photosession.contract.photographer.inn,
        'photographer_bank_acc': photosession.contract.photographer.paymant_account,
        'photographer_bik': photosession.contract.photographer.bank_accaunt.bic,
        'photographer_bank_name': photosession.contract.photographer.bank_accaunt.name,
        'photographer_bank_corr': photosession.contract.photographer.bank_accaunt.correspondent_account,
        'agency_opf': photosession.contract.agency.opf_full,
        'agency_name': photosession.contract.agency.name,
        'agency_inn': photosession.contract.agency.inn,
        'agency_kpp': photosession.contract.agency.kpp,
        'agency_ogrn': photosession.contract.agency.ogrn,
        'agency_adress': photosession.contract.agency.address,
        'agency_bank_adress': photosession.contract.agency.bank_accaunt.address,
        'agency_corr': photosession.contract.agency.bank_accaunt.correspondent_account,
        'agency_bank_acc': photosession.contract.agency.paymant_account,
        'manager_full_name': photosession.contract.agency.manager.initials,
        # 'manager_short': photosession.contract.agency.manager.short_initials,
        'contract_name': photosession.contract.name,
        'contract_date': photosession.contract.date,
        # 'upper_bill_number': photosession.contract.upper_bill_number,
        # 'bill_date': photosession.contract.bill_date,
        # 'bill_num': photosession.contract.bill_num,
        'service_name': photosession.service.name,
        'photosession_price': photosession.price,
        'photosession_price_litteral': num2words(photosession.price, lang="ru"),
        'photosession_adress': photosession.location,
        'photosession_url': photosession.url,
        'cur_date': photosession.date
    }
    pprint(photosession_dict)
    return photosession_dict


def render_docx(photosession: Photosession) -> str:
    doc_tamplate = f'{photosession.contract.agency.name}.docx'
    docx_tamplate_path = os.path.join('templates', doc_tamplate)

    docx = DocxTemplate(docx_tamplate_path)

    return docx
