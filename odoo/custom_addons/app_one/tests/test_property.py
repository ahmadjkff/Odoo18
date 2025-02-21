from odoo.tests import common
from odoo import fields

class TestProperty(common.TransactionCase):

    today = fields.Date.today()
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT10003',
            'name': 'Property 1001',
            'description': 'description',
            'postcode': '1234433',
            'date_availability': self.today,
            'bedrooms': 7,
            'expected_price': 3000,
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id,[{
            'ref': 'PRT10002',
            'name': 'Property 1001',
            'description': 'description',
            'postcode': '1234433',
            'date_availability': self.today,
            'bedrooms': 7,
            'expected_price': 3000,
        }])
