import pytest

from viadot.sources import Epicor
from viadot.config import local_config
from viadot.exceptions import DataRangeError


@pytest.fixture(scope="session")
def epicor():
    epicor = Epicor(
        base_url=local_config.get("Epicor").get("test_url"),
        config_key="Epicor",
        filters_xml="""
    <OrderQuery>
        <QueryFields>
            <CompanyNumber>001</CompanyNumber>
            <BegInvoiceDate>2022-05-16</BegInvoiceDate>
            <EndInvoiceDate>2022-05-16</EndInvoiceDate>
            <RecordCount>3</RecordCount>
        </QueryFields>
    </OrderQuery>""",
    )
    yield epicor


@pytest.fixture(scope="session")
def epicor_error():
    epicor_error = Epicor(
        base_url=local_config.get("Epicor").get("test_url"),
        config_key="Epicor",
        filters_xml="""
    <OrderQuery>
        <QueryFields>
            <CompanyNumber>001</CompanyNumber>
            <BegInvoiceDate></BegInvoiceDate>
            <EndInvoiceDate>2022-05-16</EndInvoiceDate>
            <RecordCount>3</RecordCount>
        </QueryFields>
    </OrderQuery>""",
    )
    yield epicor_error


def test_connection(epicor):
    assert epicor.get_xml_response().status_code == 200


def test_check_filter(epicor_error):
    with pytest.raises(DataRangeError):
        epicor_error.check_filter()
