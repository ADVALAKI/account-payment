# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
try:
    from openupgradelib.openupgrade_tools import table_exists
except ImportError:
    table_exists = None


def post_init_hook(cr, registry):
    """Loaded after installing the module.
    This module's DB modifications will be available.
    :param odoo.sql_db.Cursor cr:
        Database cursor.
    :param odoo.modules.registry.Registry registry:
        Database registry, using v7 api.
    """
    payment_ids = registry['account.payment'].search(
        cr, 1, [('payment_type', '!=', 'transfer')])
    # TODO improove this because it is too slow, perhups because of name
    # computation
    for payment in registry['account.payment'].browse(cr, 1, payment_ids):
        payment.payment_group_id.write({
            'document_number': payment.document_number,
            'receiptbook_id': payment.receiptbook_id.id,
        })
