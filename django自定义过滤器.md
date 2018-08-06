# django自定义过滤器

在内置的方法满足不了我们的需求的时候，就需要自己定义属于自己的方法了，自定义方法分别分为filter和simple_tag

## 步骤

1. settings中的INSTALLED_APPS,注册app

2. 在app中创建templatetags目录,目录名必须为templatetags

3. 创建一个自定义的custom_tags.py

   ```python
   from django import template
   from django.utils.safestring import mark_safe

   # register的名字是固定的,不可改变
   register = template.Library()

   # 过滤器
   @register.filter
   def test_filter(value, param):
       return value + param

   @register.filter
   def test_filter2(value, param1,param2):
       return value + param1 + param2
       
   # 标签
   @register.simple_tag
   def multi_tag(value, p2, p3, p1):
       return value * p2 * p3 * p1

   @register.simple_tag  # 标签
   def my_input(id, arg):
       result = "<input type='text' id='%s' class='%s' />" % (id, arg,)
       return mark_safe(result)

   ```

4. 在使用自定义simple_tag和filter的html文件中导入之前创建的 custom_tags.py

5. 在引用模板中导入：{% load custom_tags %}

6. 在模板中使用 

   ```python
   {#  使用filter方式调用自定义方法  #}
   <!-- 将当做参数传递给test_filter1函数进行处理    处理方式 test_filter2(test_filter1) -->
   <p>{{ test_filter1|test_filter2}}</p>
   !-- 将test_filter当做参数传递给test_filter2函数进行处理,接受2个参数  处理方式
       <p>{{ test_filter1|test_filter2:"xxx" }}</p>
   {#  使用simple_tag方式调用自定义方法  #}
   <!-- 将k1当做参数传递给multi_tag函数进行处理,接收多个参数  处理方式 multi_tag("处理的值", "参数1" "参数2" "参数3") -->
   <p>{% multi_tag "处理的值" "参数1" "参数2" "参数3" %}</p>
   ```

## 