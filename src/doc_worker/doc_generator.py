import os
from pprint import pprint
from docxtpl import DocxTemplate
from num2words import num2words
from src.db.models import Photosession, Contract


def serialize_contract_dict(contract: Contract) -> dict:
    """Создает словарь из объекта Contract для шаблонизации документа."""
    contract_dict = {
        'name': contract.name,
        'date': contract.date
    }
    return contract_dict


async def serialize_photosession_dict(photosession: Photosession) -> dict:
    """Создает словарь с данными фотосессии для шаблонизации документа."""
    print('++++' * 30)
    photosession_dict = {
        'photographer_fullname': photosession.contract.photographer.full_name,
        'photographer_address': photosession.contract.photographer.address,
        'photographer_opf_full': photosession.contract.photographer.opf_full,
        'photographer_opf_short': photosession.contract.photographer.opf_short,
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
        'agency_address': photosession.contract.agency.address,
        'agency_bank_address': photosession.contract.agency.bank_accaunt.address,
        'agency_corr': photosession.contract.agency.bank_accaunt.correspondent_account,
        'agency_bank_acc': photosession.contract.agency.paymant_account,
        'manager_full_name': photosession.contract.agency.manager.full_name,
        'manager_short': f'{photosession.contract.agency.manager.last_name} {photosession.contract.agency.manager.initials}',
        'contract_name': photosession.contract.name,
        'contract_date': photosession.contract.date,
        'bill_num': photosession.order_number,
        'upper_bill_number': photosession.upper_order_number,
        'bill_date': photosession.date,
        'service_name': photosession.service.name,
        'price': photosession.price,
        'price_litteral': photosession.price_litteral,
        'photosession_address': photosession.location,
        'photosession_url': photosession.url,
        'photosession_date': photosession.date
    }
    pprint(photosession_dict)
    return photosession_dict


def render_docx(photosession: Photosession) -> str:
    """Создает документ Word на основе шаблона для фотосессии."""
    doc_tamplate = f'{photosession.contract.agency.name}.docx'
    docx_tamplate_path = os.path.join('templates', doc_tamplate)

    docx = DocxTemplate(docx_tamplate_path)

    return docx
