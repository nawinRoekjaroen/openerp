from osv import osv, fields
from tools import config

class custom_market(osv.osv):
	_name="custom.market"

	def _purchase_amount(self, cr, uid, ids, field_name, arg, context):
                res = {}
                cur_obj = self.pool.get('res.currency')
                for puch in self.browse(cr, uid, ids):
                        res[puch.id] = {
                                'amount_total2':0.0,
                                }
                        val = 0.0
                        cur = puch.pricelist_id.currency_id
#                        import pdb; pdb.set_trace()
                        for chase in puch.purchase_id:
                                val += chase.price_total_purchase
                        res[puch.id]['amount_total2'] = cur_obj.round(cr, uid, cur, val)
                return res
	def _sale_amount(self, cr, uid, ids, field_name, arg, context):
		res={}
		cur_obj=self.pool.get('res.currency')
		for sale in self.browse(cr, uid, ids):
			res[sale.id] = {
				'amount_total':0.0,
				}
			val=0.0
			cur=sale.pricelist_id.currency_id
			for sale_line in sale.sales_id:
				val+=sale_line.price_total_sale
			res[sale.id]['amount_total']=cur_obj.round(cr, uid, cur, val)
		return res

	def _compute_total(self, cr, uid, ids, field_name, arg, context):
                res = {}
                cur_obj = self.pool.get('res.currency')
                for total in self.browse(cr, uid, ids):
                        res[total.id] = total.amount_total2 - total.amount_total
                        #cur = total.pricelist_id.currency_id
                        #res[total.id] = cur_obj.round(cr, uid, cur, res[total.id])
                return res
	
	def _get_purchase_order(self, cr, uid, ids, context={}):
                result={}
                for line in self.pool.get('purchase.order').browse(cr, uid, ids, context=context):
                        result[line.purchase_id_line.id] = True
                return result.keys()
	def _get_sale_order(self, cr, uid, ids, context={}):
                result={}
                for line in self.pool.get('sale.order').browse(cr, uid, ids, context=context):
                        result[line.sales_id_line.id] = True
                return result.keys()

	_columns={
		'name':fields.many2one('res.partner', 'Partner', required=True, select=True),
		'product_id':fields.many2one('product.product','Product', required=True, select=True),
		'sales_id':fields.one2many('sale.order', 'sales_id_line', 'Ref Sales'),
		'purchase_id':fields.one2many('purchase.order','purchase_id_line','Ref Purchase'),
		'date':fields.date('Date'),
		'pricelist_id':fields.many2one('product.pricelist','Pricelist'),
		'sum_total':fields.function(_compute_total, method=True, digids=(16,2), string='Benefit'),
		'amount_total2':fields.function(_purchase_amount, method=True, digids=(16, 2), string='Sale Total',
			store = {
				'custom.market':(lambda self, cr, uid, ids, c={}: ids, ['purchase_id'],10),
				'purchase.order':(_get_purchase_order, ['price_unit_purchase','product_uom_purchase'],10),
		 },
		multi='sums'),
		'amount_total':fields.function(_sale_amount, method=True, digids=(16, 2), string='Purchase Total',
			store = {
				'custom.market':(lambda self, cr, uid, ids, c={}: ids, ['sales_id'], 10),
				'sale.order':(_get_sale_order, ['price_unit', 'product_uom'], 10),
		},
		multi='sums'),
	}
	
	_defualts={}

	def button_demo(self, cr, uid, ids, context={}):
		return True
	def button_demo2(self, cr, uid, ids, context={}):
                return True
custom_market()
class purchase_order(osv.osv):
	_name="purchase.order"

	def _compute_amount_purchase(self, cr, uid, ids, field_name, arg, context):
                res = {}
                cur_obj = self.pool.get('res.currency')
                for purchase in self.browse(cr, uid, ids):
                        res[purchase.id] = purchase.price_unit_purchase * purchase.product_uom_purchase
                        cur = purchase.purchase_id_line.pricelist_id.currency_id
                        res[purchase.id] = cur_obj.round(cr, uid, cur, res[purchase.id])
                return res
	
	_columns={
		'stat':fields.selection([('',''),('sale','sale Order'),('purchase','Purchase Order')],'State',readonly=True),
		'purchase_id_line':fields.many2one('custom.market','Ref PCH ln'),
		'price_unit_purchase':fields.float('Price Per Unit', digids=(16,2)),
		'product_uom_purchase':fields.float('Quanlity (UoM)', digids=(16,2)),
		'price_total_purchase':fields.function(_compute_amount_purchase, method=True, string='Price Purchase', digids=(2, int(config['price_accuracy']))),
		}
	
	_defaults={
		'stat':lambda *a: 'sale',
		'price_unit_purchase':lambda *a: 0.0,
                'product_uom_purchase':lambda *a: 0.0,
		}
purchase_order()

class sale_order(osv.osv):
	_name="sale.order"
	
	def _compute_amount_sale(self, cr, uid, ids, field_name, arg, context):
		res={}
		cur_obj=self.pool.get('res.currency')
		for sale in self.browse(cr, uid, ids):
			res[sale.id] = sale.price_unit * sale.product_uom
			cur = sale.sales_id_line.pricelist_id.currency_id
			#import pdb; pdb.set_trace()
			res[sale.id]=cur_obj.round(cr, uid, cur, res[sale.id])
		return res

	_columns={
		'sales_id_line':fields.many2one('custom.market','Ref Sales'),
		'price_unit':fields.float('Price Per Unit', digids=(16,2)),
		'product_uom':fields.float('Quanlity (UoM)', digids=(16,2)),
		'price_total_sale':fields.function(_compute_amount_sale, method=True, string='Price Sale', digids=(2, int(config['price_accuracy']))),
		'state':fields.selection([('',''),('sale','sale Order'),('purchase','Purchase Order')],'State',readonly=True),
		}
	_defaults={
		'state':lambda *a:'purchase',
		'price_unit':lambda *a: 0.0,
		'product_uom':lambda *a: 0.0,
		}
sale_order()
