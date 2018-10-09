from django.db import models

# Create your models here.
from django.utils import timezone
from SH1802Django.settings import SEX_CHOICES, DB_FIELD_VALID_CHOICES, USER_CHOICES,  DINNER_CHOICES, PAY_CHOICES
from DjangoUeditor.models import UEditorField

'''
会员信息
'''
class  ArtsUser(models.Model):
	username = models.CharField(max_length=50, verbose_name="用户名")
	password = models.CharField(max_length=100, verbose_name="密码")
	email = models.EmailField(verbose_name="邮箱")
	createtime = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="添加时间")
	flag = models.IntegerField(default=0, verbose_name="会员控制字段", choices=USER_CHOICES)

	def __str__(self):
		return self.username

	class Meta:
		db_table = "arts_user"
		verbose_name = "会员信息"
		verbose_name_plural = verbose_name
		ordering = ["-createtime"]



'''
小说标签类
'''
class Tag(models.Model):
	t_name = models.CharField(max_length=20, verbose_name="文章标签")
	t_info = models.CharField(max_length=50, verbose_name="标签描述")
	t_createtime = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="创建时间")
	t_flag = models.IntegerField(default=0, verbose_name="控制字段", choices=DB_FIELD_VALID_CHOICES)

	def __str__(self):
		return self.t_name

	class  Meta:
		verbose_name = "标签"
		verbose_name_plural = verbose_name
		db_table = "tag"
		ordering = ["-t_createtime"]    #按照创建时间降序



'''
小说内容
Tag -- Art
1 ---- N
'''
class Art(models.Model):
	a_title = models.CharField(max_length=100, verbose_name="文章标题")
	a_info = models.CharField(max_length=200, verbose_name="文章描述")
	#a_content= models.TextField(verbose_name="文章内容")
	a_content = UEditorField(verbose_name="文章内容", width=1000, height=600,
							 imagePath="media/arts_ups/ueditor/",
							 filePath="media/arts_ups/ueditor/",
							 blank=True, toolbars="full", default='')
	a_img = models.ImageField(null=True, blank=True, upload_to="media/arts_ups/%Y/%m",
							  verbose_name="封面", max_length=150)
	a_createtime = models.DateTimeField(default=timezone.now, db_index=True,
								   verbose_name="添加时间")

	a_tag = models.ForeignKey(Tag, verbose_name="关联文章标签")
	a_price = models.IntegerField(default=0, verbose_name="单价")
	a_flag = models.IntegerField(default=0, verbose_name="控制字段", choices=DB_FIELD_VALID_CHOICES)
	operator = models.ForeignKey("auth.User", default=1, verbose_name="api操作者")


	def __str__(self):
		return self.a_title


	class Meta:
		verbose_name = "小说"
		verbose_name_plural = verbose_name
		db_table = "art"
		ordering = ["-a_createtime"]  # 按照创建时间降序


'''
小说的章节信息
'''
class Chapter(models.Model):
	art = models.ForeignKey(Art, verbose_name="小说")
	title = models.CharField(max_length=100, verbose_name="章节标题")
	content = models.TextField(verbose_name="小说章节内容")
	create_time = models.DateTimeField(default=timezone.now, db_index=True,
								   verbose_name="添加时间")

	class Meta:
		db_table = "art_chapter"
		verbose_name = "小说章节"
		verbose_name_plural = verbose_name



'''
订单数据模型
'''
class ProductOrder(models.Model):
	order_id = models.BigIntegerField(verbose_name="订单号", unique=True)
	pay_type = models.IntegerField(default=0, verbose_name="支付类型", choices=PAY_CHOICES)
	address = models.CharField(default='', max_length=200, verbose_name="订单配送地址")
	phone = models.BigIntegerField(default=0, verbose_name="联系方式")
	order_time = models.DateTimeField(default=timezone.now, db_index=True,
									  verbose_name="下单时间")

	def __str__(self):
		return self.order_id


	class Meta:
		db_table = "product_order"
		verbose_name = "用户订单"
		verbose_name_plural = verbose_name

'''
购物车条目
'''
class LineItem(models.Model):
	product = models.ForeignKey(Art, verbose_name="小说产品")
	user = models.ForeignKey(ArtsUser, verbose_name="购买用户")
	unit_price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="单价")
	quantity = models.IntegerField(default=0, verbose_name="购买数量")
	createtime = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
	flag = models.IntegerField(default=0, verbose_name="购买状态", choices=DINNER_CHOICES)

	def __str__(self):
		return self.product.a_title


	class Meta:
		db_table = "line_item"
		verbose_name = "购物车条目"
		verbose_name_plural = verbose_name


'''
商品条目和订单关联表
1   1
3   1
4   1
'''
class OrderItemRelation(models.Model):
	line_item = models.ForeignKey(LineItem, verbose_name="关联条目")
	product_order = models.ForeignKey(ProductOrder, verbose_name="关联订单")
	create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")


	class Meta:
		db_table = "order_item_relation"
		verbose_name = "商品条目和订单关联表"
		verbose_name_plural = verbose_name

'''
购物车
购物车是这些条目的容器。
购物车并不需要记录到数据库中，就好像超市并不关注顾客使用了哪些购物车而只关注他买了什么商品一样。
所以购物车不应该继承自models.Model，而仅仅应该是一个普通类
'''
import time, random
class Cart(object):

	@classmethod
	def add_product(Cls, product, user):
		the_item_products = LineItem.objects.filter(user=user.id, product=product.id)
		product_quality_dict = {}
		if len(the_item_products) > 0:
			the_product = the_item_products[0]
			this_quality = the_product.quantity + 1
			#print(f'quality:{this_quality}')
			the_item_products.update(quantity=this_quality)
		else:
			# order_id = "%s%s" % (int(time.time()), random.randint(10, 100))
			# product_order = ProductOrder(order_id=int(order_id))
			# product_order.save()
			l_item = LineItem(product=product,
                    user = user,
                    unit_price=product.a_price,
					#product_order_id = int(order_id),
                    quantity=1)
			l_item.save()

		return True


	@classmethod
	def get_products(Cls, user):
		product_list = LineItem.objects.filter(user=user.id)

		total_price = 0
		for prod_item in product_list:
			total_price += prod_item.product.a_price * prod_item.quantity
		return (total_price, product_list)




