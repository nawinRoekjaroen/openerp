from osv import fields, osv
from tools import config
import math
import time
import netsvc
from tools.translate import _
class market_shop(osv.osv):
	_name = "market.shop"
	
	_columns = {
		'name':fields.char('Market Name:',size=23,required=True),
		'address':fields.many2one('res.partner.address','Address:'),
		}
market_shop()
class market_stock(osv.osv):
	_name = "market.stock"
	
	_columns = {
		'pricelist_id':fields.many2one('product.pricelist', 'Pricelist'),
		'name':fields.many2one('market.shop','Name Market',required=True),
		'date_id':fields.date('Date'),
		'supply':fields.many2one('res.partner','Supplier'),
		}
	_defaults = {}
	def button_dummy2(self, cr, uid, ids, context={}):
		return True
market_stock()
class market_sale(osv.osv):
	_name = "market.sale"
	def _amount_sum(self, cr, uid, ids, field_name, arg, context):
		res={} 
		cur_obj = self.pool.get('res.currency')
		for line2 in self.browse(cr, uid, ids):
			res[line2.id] = line2.amount_total - line2.amount_total2
			cur = line2.pricelist_id.currency_id
			res[line2.id] = cur_obj.round(cr, uid, cur, res[line2.id])
		return res
	def _purchase_amount(self, cr, uid, ids, field_name, arg, context):
                res = {}
                cur_obj = self.pool.get('res.currency')
                for pur in self.browse(cr, uid, ids):
                        res[pur.id] = {
                                'amount_total2':0.0,
                                }
                        val = 0.0
                        cur = pur.pricelist_id.currency_id
#                       import pdb; pdb.set_trace()
                        for chase in pur.sale_id:
                                val += chase.price_total
                        res[pur.id]['amount_total2'] = cur_obj.round(cr, uid, cur, val)
                return res
        def _get_order_purchase(self, cr, uid, ids, context={}):
                result = {}
                for line in self.pool.get('market.purchase.sale.sale'):
                        result[line.purchase_order_id.id] = True
                return result.keys()

	
	def _amount_all(self, cr, uid, ids, field_name, arg, context):
		res = {}
		cur_obj = self.pool.get('res.currency')
		for order in self.browse(cr, uid, ids):
			res[order.id] = {
				'amount_untaxed': 0.0,
				'amount_total': 0.0,
				}
			val = val1 = 0.0
			cur = order.pricelist_id.currency_id
			for line in order.purchase_id:
				val1 += line.price_suptotal
			res[order.id]['amount_balance'] = cur_obj.round(cr, uid, cur, val)
			res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
#			import pdb;pdb.set_trace()
			res[order.id]['amount_total'] = res[order.id]['amount_untaxed']
		return res


	def _get_order(self, cr, uid, ids, context={}):
		result={}
		for line in self.pool.get('market.purchase.sale').browse(cr, uid, ids, context=context):
			result[line.order_id.id] = True
		return result.keys()

	_columns = {
		'pricelist_id':fields.many2one('product.pricelist', 'Pricelist'),
		'partner_id':fields.many2one('res.partner','Customer',required=True),
		'name':fields.many2one('market.shop', 'Name Market',required=True),
		'date':fields.date('Date'),
		'stat':fields.selection([('',''),('sale','Sale Oder'),('purchase','Purshase Order')], 'State', required=True),
		'purchase_id':fields.one2many('market.purchase.sale','order_id','Ref Purchase and Sale'),
		'sale_id':fields.one2many('market.purchase.sale.sale','purchase_id_order','Ref Purchase and Sale'),
		'price_balance':fields.function(_amount_sum, method=True, digids=(16, int(config['price_accuracy'])), string="Balance_total"),
		'amount_untaxed':fields.function(_amount_all, method=True, digids=(16,2), string= 'Untaxed Amount',
			store = {
				'market.sale': (lambda self, cr, uid, ids, c={}: ids, ['purchase_id'], 10),
				'market.purshase.sale':(_get_order, ['price_unit', 'discount', 'product_uom_qty'], 10),
			},
			multi='sums'),
		'amount_total':fields.function(_amount_all, method=True, digids=(16,2), string='Total Sales',
                        store = {
                                'market.sale': (lambda self, cr, uid, ids, c={}: ids, ['purchase_id'], 10),
                                'market.purshase.sale':(_get_order, ['price_unit', 'discount', 'product_uom_qty'], 10),
                        },
                        multi='sums'),
		'amount_total2':fields.function(_purchase_amount, method=True, digids=(16,2), string='Total Purchases',
                        store = {
                                'market.sale': (lambda self, cr, uid, ids, c={}: ids, ['sale_id'], 10),
                                'market.purshase.sale.sale':(_get_order_purchase, ['price_unit', 'discount', 'product_uom_qty'], 10),
                        },
                        multi='sums'),
                }
       	_defaults = {
		'stat':lambda *a:"''",
		'pricelist_id': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr, uid, context).id,
		}
	def button_dummy(self, cr, uid, ids, context={}):
		return True
	def button_dummy2(self, cr, uid, ids, context={}):
                return True
market_sale()
class market_product(osv.osv):
	_name = "market.product"

	_columns = {
		'name':fields.char('Product Name',size=20),
		'code':fields.integer('Code',digid=(16,2)),
		'sequence':fields.integer('Amount',digid=(16,2)),
		'price_product':fields.float('Price Per Unit',required=True, digids=(16, 2)),
		
		}
	_defaults = {
		'sequence':lambda *a:0,
		}
market_product()

class market_purchase_sale(osv.osv):

	def _amount_line(self, cr, uid, ids, field_name, arg, context):
		res={}
		cur_obj = self.pool.get('res.currency')
		for line in self.browse(cr, uid, ids):
			res[line.id] = line.price_unit * line.product_uom_qty * (1-(line.discount or 0.0)/100)
                        #import pdb; pdb.set_trace()
			cur = line.order_id.pricelist_id.currency_id
			res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
		return res 
	_name = "market.purchase.sale"
	_columns = {
		'order_id':fields.many2one('market.sale', 'Oder Ref', required=True, select=True, readonly=True, ondelete='cascade'),
		'price_unit':fields.float('Unit Price', required=True, digids=(16, int(config['price_accuracy'])),),
		'product_uom_qty':fields.float('Quantity (UoM)',digids=(16,2), required=True,),
		'discount':fields.float('Discount (%)'),
		'product':fields.many2one('market.product', 'Product'),
		'price_suptotal':fields.function(_amount_line, method=True, string='Subtotal', digids=(16, int(config['price_accuracy']))),
		}
	_defaults = {
		'price_unit':lambda *a:0.0,
		'product_uom_qty':lambda *a:0.0,
		'discount':lambda *a:0.0,
		}
market_purchase_sale()

class market_purchase_sale_sale(osv.osv):

        def _amount_total(self, cr, uid, ids, field_name, arg, context):
                res={}
                cur_obj = self.pool.get('res.currency')
                for line in self.browse(cr, uid, ids):
                        res[line.id] = line.price_unit * line.product_uom_qty * (1-(line.discount or 0.0)/100)
                        #import pdb; pdb.set_trace()
                        cur = line.purchase_id_order.pricelist_id.currency_id
                        res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
                return res
        _name = "market.purchase.sale.sale"
        _columns = {
                'purchase_id_order':fields.many2one('market.sale', 'Purchase Ref', required=True, readonly=True, ondelete="cascade"),
                'price_unit':fields.float('Unit Price', required=True, digids=(16, int(config['price_accuracy'])),),
                'product_uom_qty':fields.float('Quantity (UoM)',digids=(16,2), required=True,),
                'discount':fields.float('Discount (%)'),
                'product':fields.many2one('market.product', 'Product'),
                'price_total':fields.function(_amount_total, method=True, string='Total', digids=(16, int(config['price_accuracy']))),
                }
        _defaults = {
                'price_unit':lambda *a:0.0,
                'product_uom_qty':lambda *a:0.0,
                'discount':lambda *a:0.0,
                }
market_purchase_sale_sale()
