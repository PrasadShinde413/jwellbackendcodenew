from rest_framework import serializers
from .models import BhishiAttachment, BhishiPayment, Customer, PurchaseInvoice,SupplierAttachment

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get("email") == "":
            validated_data["email"] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("email") == "":
            validated_data["email"] = None
        return super().update(instance, validated_data)


#################################################################################################################

from rest_framework import serializers
from .models import Metal, Carat

class MetalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metal
        fields = '__all__'
#################################################################################################################


class CaratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carat
        fields = '__all__'


from rest_framework import serializers
from .models import Jewelry

class JewelrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Jewelry
        fields = '__all__'


#################################################################################################################

# from datetime import datetime, date
# from rest_framework import serializers
# from .models import SaleItem

# class SaleItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SaleItem
#         fields = "__all__"

#     def to_internal_value(self, data):
#         data = data.copy()
#         sale_date = data.get('date')
#         if sale_date:
#             try:
#                 # Handle ISO and plain date strings
#                 if 'T' in sale_date:
#                     parsed_date = datetime.fromisoformat(sale_date.replace('Z', '')).date()
#                 else:
#                     parsed_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
#                 data['date'] = parsed_date
#             except Exception:
#                 pass
#         return super().to_internal_value(data)
    
######################################################################################################

# from datetime import datetime, date
# from rest_framework import serializers
# from .models import SaleItem, Customer # Import Customer model

# class SaleItemSerializer(serializers.ModelSerializer):
#     # Add a read-only field to display the customer's name
#     customer_name = serializers.CharField(source='customer.name', read_only=True)

#     class Meta:
#         model = SaleItem
#         fields = "__all__" # Keeps all model fields and adds customer_name

#     def to_internal_value(self, data):
#         data = data.copy()
#         sale_date = data.get('date')
#         if sale_date:
#             try:
#                 # Handle ISO and plain date strings
#                 if 'T' in sale_date:
#                     parsed_date = datetime.fromisoformat(sale_date.replace('Z', '')).date()
#                 else:
#                     parsed_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
#                 data['date'] = parsed_date
#             except (ValueError, TypeError):
#                 # If date parsing fails, let DRF handle validation or pass
#                 pass 
#         return super().to_internal_value(data)
    
from datetime import datetime
from rest_framework import serializers
from django.db.models import Sum

from .models import SaleItem, Customer
from .models import URDAdjustment, URDDetail


class SaleItemSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    sale_date = serializers.DateField(source='date', required=False)  # Alias for date field
    making_per_gram = serializers.DecimalField(source='making_charge', max_digits=10, decimal_places=2, required=False)  # Alias for making_charge

    # 🔽 NEW FIELDS
    urd_adjustment_amount = serializers.SerializerMethodField()
    urd_final_amount = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = [
            'id', 'saleitem_id', 'date', 'sale_date', 'salesperson', 'qr_barcode_id', 'huid_number', 'metal', 'item_name', 'purity', 'pieces',
            'gross_weight', 'less_weight', 'net_weight', 'rate_per_gram', 'making_type', 'making_charge', 'making_per_gram',
            'stone_charges', 'hallmark_charges', 'hm_tax_percent', 'gst_percent', 'comments', 'customer',
            'base_metal_cost', 'making_cost', 'total_tax', 'total_amount', 'bill_type', 'created_at',
            'customer_name', 'urd_adjustment_amount', 'urd_final_amount'
        ]

        # ✅ IMPORTANT FIX - Exclude calculated fields from input validation
        extra_kwargs = {
            # Required fields (keep validation)
            "metal": {"required": True},
            "item_name": {"required": True},
            "gross_weight": {"required": True},
            "rate_per_gram": {"required": True},
            "making_type": {"required": True},
            "customer": {"required": True},

            # Date field
            "date": {"required": False},
            "sale_date": {"required": False},

            # Making charge aliases
            "making_charge": {"required": False},
            "making_per_gram": {"required": False},
            "saleitem_id": {"required": False},

            # Calculated fields - make them read-only
            "net_weight": {"read_only": True},
            "base_metal_cost": {"read_only": True},
            "making_cost": {"read_only": True},
            "total_tax": {"read_only": True},
            "total_amount": {"read_only": True},

            # Read-only fields
            "customer_name": {"read_only": True},
            "urd_adjustment_amount": {"read_only": True},
            "urd_final_amount": {"read_only": True},
        }

    # -------------------------
    # URD Adjustment Amount
    # -------------------------
    def get_urd_adjustment_amount(self, obj):
        try:
            return obj.urd_adjustment.adjust_amount
        except URDAdjustment.DoesNotExist:
            return 0

    # -------------------------
    # URD Final Amount (SUM)
    # -------------------------
    def get_urd_final_amount(self, obj):
        total = URDDetail.objects.filter(
            sale_item=obj
        ).aggregate(total=Sum("final_amount"))["total"]

        return total or 0

    # -------------------------
    # DATE PARSING (unchanged)
    # -------------------------
    def to_internal_value(self, data):
        data = data.copy()
        sale_date = data.get('date')
        if sale_date:
            try:
                if 'T' in sale_date:
                    parsed_date = datetime.fromisoformat(
                        sale_date.replace('Z', '')
                    ).date()
                else:
                    parsed_date = datetime.strptime(
                        sale_date, "%Y-%m-%d"
                    ).date()
                data['date'] = parsed_date
            except (ValueError, TypeError):
                pass
        return super().to_internal_value(data)


##############################################################################################################

from rest_framework import serializers
from .models import SaleItem


class SaleItemInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = [
            "id", "saleitem_id", "date", "salesperson", "qr_barcode_id", "huid_number",
            "metal", "item_name", "purity", "pieces", "gross_weight", "less_weight",
            "net_weight", "rate_per_gram", "making_type", "making_charge",
            "stone_charges", "hallmark_charges", "hm_tax_percent", "gst_percent",
            "comments", "base_metal_cost", "making_cost", "total_tax",
            "total_amount", "created_at", "bill_type",
        ]

#################################################################################################################

# # serializers.py
# from rest_framework import serializers
# from .models import Order, OrderItem, Payment


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = "__all__"
#         read_only_fields = ["order", "total_price"]


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"
#         read_only_fields = ["order"]


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     payments = PaymentSerializer(many=True, required=False)

#     class Meta:
#         model = Order
#         fields = "__all__"

#     def create(self, validated_data):
#         items_data = validated_data.pop("items")
#         payments_data = validated_data.pop("payments", [])

#         order = Order.objects.create(**validated_data)

#         total_item_amount = 0
#         total_tax = 0
#         total_making = 0

#         for item_data in items_data:
#             net_weight = item_data["net_weight"]
#             rate = item_data["rate_per_gram"]
#             making = item_data["making_charge"]
#             stone = item_data["stone_charge"]
#             hallmark = item_data["hallmark_charge"]
#             gst = item_data["gst_percent"]
#             hm = item_data["hm_tax_percent"]

#             subtotal = (net_weight * rate) + making + stone + hallmark
#             tax = subtotal * ((gst + hm) / 100)
#             total = subtotal + tax

#             total_item_amount += subtotal
#             total_tax += tax
#             total_making += making

#             OrderItem.objects.create(order=order, total_price=total, **item_data)

#         # Handle payments
#         total_payments = 0
#         for payment_data in payments_data:
#             total_payments += payment_data["amount"]
#             Payment.objects.create(order=order, **payment_data)

#         # Apply discount and URD
#         discount_amt = (total_item_amount * validated_data.get("discount_percent", 0)) / 100
#         urd_value = validated_data.get("urd_weight", 0) * validated_data.get("urd_rate", 0)

#         grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
#         balance_due = grand_total - total_payments

#         order.item_total = total_item_amount
#         order.making_total = total_making
#         order.tax_total = total_tax
#         order.discount_amount = discount_amt
#         order.grand_total = grand_total
#         order.balance_due = balance_due
#         order.save()

#         return order
    
from rest_framework import serializers
from .models import Order, OrderItem, Payment, OrderAttachment


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["order", "total_price"]  # Don't allow updating these fields


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["order"]  # Don't allow updating the order field here

##############################################################################################################################
from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem, Payment


class OrderAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderAttachment
        fields = ['id', 'order', 'file', 'file_url', 'uploaded_at']
        read_only_fields = ['id', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    payments = PaymentSerializer(many=True, required=False)
    attachment = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)
    attachments = OrderAttachmentSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        # When using multipart/form-data, nested fields like 'items' and 'payments' 
        # are often sent as JSON strings. We need to parse them.
        if hasattr(data, 'copy'):
            data = data.copy()
        
        import json
        for field in ['items', 'payments', 'item']: # Added 'item' just in case as some views use it
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except (ValueError, TypeError):
                    pass

        # Handle cases where 'attachment' might be a string (e.g., empty string or existing file path)
        # FileField expects a file object; passing a string causes "The submitted data was not a file" error.
        if 'attachment' in data and isinstance(data['attachment'], (str, type(None))):
            data.pop('attachment', None)

        return super().to_internal_value(data)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        payments_data = validated_data.pop("payments", [])

        # Create the order
        order = Order.objects.create(**validated_data)

        total_item_amount = Decimal(0)
        total_tax = Decimal(0)
        total_making = Decimal(0)

        # Process items and create them
        for item_data in items_data:
            net_weight = item_data["net_weight"]
            rate = item_data["rate_per_gram"]
            making = item_data["making_charge"]
            stone = item_data["stone_charge"]
            hallmark = item_data["hallmark_charge"]
            gst = item_data["gst_percent"]
            hm = item_data["hm_tax_percent"]

            subtotal = (net_weight * rate) + (making * net_weight) + stone + hallmark
            tax = subtotal * ((gst + hm) / 100)
            total = subtotal + tax

            total_item_amount += subtotal
            total_tax += tax
            total_making += making

            # Create each item
            OrderItem.objects.create(order=order, total_price=total, **item_data)

        # Handle payments if provided
        total_payments = 0
        for payment_data in payments_data:
            total_payments += payment_data["amount"]
            Payment.objects.create(order=order, **payment_data)

        # Apply discount and URD adjustments
        discount_amt = validated_data.get("discount_amount", 0)
        urd_value = validated_data.get("urd_weight", 0) * validated_data.get("urd_rate", 0)

        # Calculate grand total and balance due
        grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
        balance_due = grand_total - total_payments

        # Update the order totals and save
        order.item_total = total_item_amount
        order.making_total = total_making
        order.tax_total = total_tax
        order.discount_amount = discount_amt
        order.grand_total = grand_total
        order.balance_due = balance_due
        order.save()

        return order

    # def update(self, instance, validated_data):
    #     # First, update the Order fields
    #     items_data = validated_data.pop('items', [])
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     # Update existing OrderItems, or create new ones if necessary
    #     for item_data in items_data:
    #         item_id = item_data.get('id', None)
            
    #         if item_id:
    #             try:
    #                 # Look for existing OrderItem by id
    #                 order_item = OrderItem.objects.get(id=item_id, order=instance)

    #                 # Update the fields of the existing OrderItem
    #                 for attr, value in item_data.items():
    #                     if attr != 'total_price':  # Avoid updating total_price directly
    #                         setattr(order_item, attr, value)

    #                 # Recalculate total_price for the existing OrderItem
    #                 order_item.total_price = (
    #                     (order_item.net_weight * order_item.rate_per_gram) +
    #                     order_item.making_charge +
    #                     order_item.stone_charge +
    #                     order_item.hallmark_charge +
    #                     ((order_item.net_weight * order_item.rate_per_gram) * (order_item.gst_percent + order_item.hm_tax_percent) / Decimal(100))
    #                 )
    #                 order_item.save()  # Save the updated OrderItem

    #             except OrderItem.DoesNotExist:
    #                 pass  # If the item doesn't exist, ignore it (no new record should be created here)

    #         # We no longer need an "else" block that creates a new OrderItem. This is the fix.
    #         # The block below should only be used when item_id is not provided, but in the case of updates, this should not be triggered.

    #     # Recalculate the totals after updating the items
    #     total_item_amount = Decimal(0)
    #     total_tax = Decimal(0)
    #     total_making = Decimal(0)

    #     for item in instance.items.all():  # Loop through related OrderItems
    #         subtotal = (item.net_weight * item.rate_per_gram) + item.making_charge + item.stone_charge + item.hallmark_charge
    #         tax = subtotal * ((item.gst_percent + item.hm_tax_percent) / Decimal(100))
    #         total_item_amount += subtotal
    #         total_tax += tax
    #         total_making += item.making_charge

    #     # Get total payments
    #     total_payments = 0
    #     for payment in instance.payments.all():
    #         total_payments += payment.amount

    #     # Apply discount and URD adjustments
    #     discount_amt = (total_item_amount * instance.discount_percent) / Decimal(100)
    #     urd_value = instance.urd_weight * instance.urd_rate

    #     # Final grand total calculation
    #     grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
    #     balance_due = grand_total - total_payments

    #     # Save the final calculated totals
    #     instance.item_total = total_item_amount
    #     instance.making_total = total_making
    #     instance.tax_total = total_tax
    #     instance.discount_amount = discount_amt
    #     instance.grand_total = grand_total
    #     instance.balance_due = balance_due
    #     instance.save()

    #     return instance


    def update(self, instance, validated_data):

        items_data = validated_data.pop("items", [])
        payments_data = validated_data.pop("payments", [])

        # Update Order fields INCLUDING urd_purity
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # --------------------------------
        # UPDATE ORDER ITEMS
        # --------------------------------
        for item_data in items_data:
            item_id = item_data.get("id", None)

            if not item_id:
                continue

            try:
                order_item = OrderItem.objects.get(id=item_id, order=instance)
            except OrderItem.DoesNotExist:
                continue

            # Update fields
            for attr, value in item_data.items():
                if attr != "total_price":
                    setattr(order_item, attr, value)

            # Recalculate total price
            subtotal = (
                (order_item.net_weight * order_item.rate_per_gram)
                + order_item.making_charge
                + order_item.stone_charge
                + order_item.hallmark_charge
            )

            tax = subtotal * (order_item.gst_percent + order_item.hm_tax_percent) / Decimal(100)

            order_item.total_price = subtotal + tax
            order_item.save()

        # --------------------------------
        # RECALCULATE TOTALS
        # --------------------------------
        total_item_amount = Decimal(0)
        total_tax = Decimal(0)
        total_making = Decimal(0)

        for item in instance.items.all():
            subtotal = (
                (item.net_weight * item.rate_per_gram)
                + item.making_charge
                + item.stone_charge
                + item.hallmark_charge
            )
            tax = subtotal * (item.gst_percent + item.hm_tax_percent) / Decimal(100)

            total_item_amount += subtotal
            total_tax += tax
            total_making += item.making_charge

        # --------------------------------
        # PAYMENTS TOTAL
        # --------------------------------
        total_payments = sum(p.amount for p in instance.payments.all())

        # --------------------------------
        # DISCOUNT, URD CALCULATIONS
        # --------------------------------
        discount_amt = instance.discount_amount or Decimal(0)

        # NOW INCLUDE NEW FIELD urd_purity
        urd_value = instance.urd_weight * instance.urd_rate

        # --------------------------------
        # FINAL CALCULATIONS
        # --------------------------------
        grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
        balance_due = grand_total - total_payments

        instance.item_total = total_item_amount
        instance.making_total = total_making
        instance.tax_total = total_tax
        instance.discount_amount = discount_amt
        instance.grand_total = grand_total
        instance.balance_due = balance_due

        instance.save()

        return instance

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     payments = PaymentSerializer(many=True, required=False)  # Make payments optional for the update

#     class Meta:
#         model = Order
#         fields = "__all__"

#     def create(self, validated_data):
#         # Extract items and payments from validated data
#         items_data = validated_data.pop("items")
#         payments_data = validated_data.pop("payments", [])

#         # Create the order
#         order = Order.objects.create(**validated_data)

#         total_item_amount = 0
#         total_tax = 0
#         total_making = 0

#         # Process items and create them
#         for item_data in items_data:
#             net_weight = item_data["net_weight"]
#             rate = item_data["rate_per_gram"]
#             making = item_data["making_charge"]
#             stone = item_data["stone_charge"]
#             hallmark = item_data["hallmark_charge"]
#             gst = item_data["gst_percent"]
#             hm = item_data["hm_tax_percent"]

#             subtotal = (net_weight * rate) + making + stone + hallmark
#             tax = subtotal * ((gst + hm) / 100)
#             total = subtotal + tax

#             total_item_amount += subtotal
#             total_tax += tax
#             total_making += making

#             # Create each item
#             OrderItem.objects.create(order=order, total_price=total, **item_data)

#         # Handle payments if provided
#         total_payments = 0
#         for payment_data in payments_data:
#             total_payments += payment_data["amount"]
#             Payment.objects.create(order=order, **payment_data)

#         # Apply discount and URD adjustments
#         discount_amt = (total_item_amount * validated_data.get("discount_percent", 0)) / 100
#         urd_value = validated_data.get("urd_weight", 0) * validated_data.get("urd_rate", 0)

#         # Calculate grand total and balance due
#         grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
#         balance_due = grand_total - total_payments

#         # Update the order totals and save
#         order.item_total = total_item_amount
#         order.making_total = total_making
#         order.tax_total = total_tax
#         order.discount_amount = discount_amt
#         order.grand_total = grand_total
#         order.balance_due = balance_due
#         order.save()

#         return order

#     def update(self, instance, validated_data):
#         # Update the Order fields first
#         items_data = validated_data.pop('items', [])
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         # Update the nested OrderItem objects (if they exist in the validated_data)
#         for item_data in items_data:
#             item_id = item_data.get('id', None)
#             if item_id:
#                 # Try to find an existing OrderItem and update it
#                 try:
#                     order_item = OrderItem.objects.get(id=item_id, order=instance)
#                     for attr, value in item_data.items():
#                         if attr != 'total_price':  # Don't allow total_price to be updated
#                             setattr(order_item, attr, value)
#                     order_item.save()
#                 except OrderItem.DoesNotExist:
#                     pass  # If the item doesn't exist, we do nothing (or you could handle creating new items)
#             else:
#                 # If there's no item_id, create a new OrderItem
#                 OrderItem.objects.create(order=instance, **item_data)

#         # Recalculate the totals after updating order items
#         total_item_amount = 0
#         total_tax = 0
#         total_making = 0
#         total_payments = 0

#         for item in instance.items.all():  # Loop over the related order items
#             subtotal = (item.net_weight * item.rate_per_gram) + item.making_charge + item.stone_charge + item.hallmark_charge
#             tax = subtotal * ((item.gst_percent + item.hm_tax_percent) / 100)
#             total = subtotal + tax
#             total_item_amount += subtotal
#             total_tax += tax
#             total_making += item.making_charge

#         # Get the payments total
#         for payment in instance.payments.all():
#             total_payments += payment.amount

#         # Apply discount and URD adjustments
#         discount_amt = (total_item_amount * instance.discount_percent) / 100
#         urd_value = instance.urd_weight * instance.urd_rate

#         # Calculate the final totals
#         grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
#         balance_due = grand_total - total_payments

#         # Update the order totals and save
#         instance.item_total = total_item_amount
#         instance.making_total = total_making
#         instance.tax_total = total_tax
#         instance.discount_amount = discount_amt
#         instance.grand_total = grand_total
#         instance.balance_due = balance_due
#         instance.save()

#         return instance
    

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order
from .serializers import OrderSerializer


class OrderListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

#################################################################################################################


# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Payment


class GetOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        # fields = ['id', 'product_name', 'quantity', 'price']
        fields = "__all__"


class GetPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # fields = ['id', 'payment_date', 'amount_paid', 'payment_method', 'status']
        fields = "__all__"


#################################################################################################################


class GetOrderSerializer(serializers.ModelSerializer):
    items = GetOrderItemSerializer(many=True, read_only=True)
    payments = GetPaymentSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Order
        fields = "__all__"
        extra_fields = ['customer_name']  # optional, for clarity

#################################################################################################################

from rest_framework import serializers
from .models import DiamondBilling, DiamondDetail, DiamondMetalInfo


class DiamondDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiamondDetail
        fields = "__all__"
        read_only_fields = ['amount', 'billing']


class DiamondMetalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiamondMetalInfo
        fields = "__all__"
        read_only_fields = ['amount', 'billing']


class DiamondBillingSerializer(serializers.ModelSerializer):
    diamond_items = DiamondDetailSerializer(many=True)
    metal_items = DiamondMetalInfoSerializer(many=True)

    class Meta:
        model = DiamondBilling
        fields = "__all__"

    def create(self, validated_data):
        diamond_data = validated_data.pop('diamond_items', [])
        metal_data = validated_data.pop('metal_items', [])

        billing = DiamondBilling.objects.create(**validated_data)

        for d in diamond_data:
            DiamondDetail.objects.create(billing=billing, **d)
        for m in metal_data:
            DiamondMetalInfo.objects.create(billing=billing, **m)

        # --- Auto calculation ---
        diamond_total = sum(item.amount for item in billing.diamond_items.all())
        metal_total = sum(item.amount for item in billing.metal_items.all())
        billing.diamond_subtotal = diamond_total
        billing.metal_subtotal = metal_total

        subtotal = diamond_total + metal_total
        billing.tax_amount = subtotal * (billing.tax_rate / 100)
        billing.net_amount = subtotal + billing.tax_amount + billing.round_adjustment
        billing.balance_amount = billing.net_amount - billing.paid_amount
        billing.save()

        return billing



###############################################################################################################

from rest_framework import serializers
from .models import Customer, Metal, Item, Loan

# --- Helper Serializers for Read-Only Embedded Data (No changes needed here) ---
class CustomerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number']

class MetalNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metal
        fields = ['id', 'name']

class ItemNestedSerializer(serializers.ModelSerializer):
    metal_name = serializers.CharField(source='metal.name', read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'metal', 'metal_name']
# --- End Helper Serializers ---


#####################################################################################################################


# from rest_framework import serializers
# from .models import Loan, Customer, Metal
# from decimal import Decimal, ROUND_HALF_UP

# class LoanCreateSerializer(serializers.ModelSerializer):
#     customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True, required=False, allow_null=True)
#     metal_used_id = serializers.PrimaryKeyRelatedField(queryset=Metal.objects.all(), source='metal_used', write_only=True, required=False, allow_null=True)

#     customer_name = serializers.CharField(source='customer.name', read_only=True, allow_null=True)
#     metal_used_name = serializers.CharField(source='metal_used.name', read_only=True, allow_null=True)
    
#     status_display = serializers.CharField(source='status', read_only=True, allow_null=True)

#     item_name = serializers.CharField(max_length=255, required=False, allow_null=True)
#     loan_return_period_unit = serializers.CharField(max_length=10, required=False, allow_null=True)
#     period_value = serializers.IntegerField(required=False, allow_null=True)

#     class Meta:
#         model = Loan
#         fields = [
#             'id', 'loan_number', 'loan_date', 'status', 'status_display',
#             'customer_id', 'customer_name',
#             'item_name',
#             'metal_used_id', 'metal_used_name',
#             'pieces', 'gross_weight', 'less_stone_weight', 'net_weight',
#             'purity', 'value_per_gram', 'current_value',
#             'hallmark_charge', 'tax', 'final_amount', 'adjusted_loan_amount',
#             'paid_amount', 'balance_amount', # Added new fields
#             'loan_return_period_unit', 'period_value',
#             'remarks', 'created_at', 'updated_at'
#         ]
#         read_only_fields = [
#             'id', 'loan_number', 'loan_date', 'status_display',
#             'net_weight', 'current_value', 'final_amount',
#             'balance_amount', # balance_amount is calculated in save, so it's read-only in serializer
#             'created_at', 'updated_at',
#             'customer_name', 'metal_used_name',
#         ]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         for field in ['gross_weight', 'less_stone_weight', 'net_weight', 'purity', 'value_per_gram',
#                       'current_value', 'hallmark_charge', 'tax', 'final_amount', 'adjusted_loan_amount',
#                       'paid_amount', 'balance_amount']: # Include new fields for formatting
#             if data.get(field) is not None:
#                 data[field] = str(Decimal(data[field]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
#         return data

class LoanCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True,
        required=False,
        allow_null=True
    )

    metal_used_id = serializers.PrimaryKeyRelatedField(
        queryset=Metal.objects.all(),
        source='metal_used',
        write_only=True,
        required=False,
        allow_null=True
    )

    customer_name = serializers.CharField(source='customer.name', read_only=True)
    metal_used_name = serializers.CharField(source='metal_used.name', read_only=True)

    status_display = serializers.CharField(source='status', read_only=True)

    item_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    loan_return_period_unit = serializers.CharField(max_length=10, required=False, allow_null=True)
    period_value = serializers.IntegerField(required=False, allow_null=True)

    # NEW FIELD
    interest = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = Loan
        fields = [
            'id', 'loan_number', 'loan_date', 'status', 'status_display',

            'customer_id', 'customer_name',
            'item_name',

            'metal_used_id', 'metal_used_name',

            # NEW FIELD
            'interest',

            'pieces', 'gross_weight', 'less_stone_weight', 'net_weight',
            'purity', 'value_per_gram', 'current_value',

            'hallmark_charge', 'tax', 'final_amount',
            'adjusted_loan_amount',

            'paid_amount', 'balance_amount',

            'loan_return_period_unit', 'period_value',
            'remarks',

            'created_at', 'updated_at'
        ]

        read_only_fields = [
            'id', 'loan_number', 'loan_date', 'status_display',
            'net_weight', 'current_value', 'final_amount',
            'balance_amount',
            'created_at', 'updated_at',
            'customer_name', 'metal_used_name',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field in [
            'interest',  # include here
            'gross_weight', 'less_stone_weight', 'net_weight',
            'purity', 'value_per_gram', 'current_value',
            'hallmark_charge', 'tax', 'final_amount',
            'adjusted_loan_amount',
            'paid_amount', 'balance_amount'
        ]:
            if data.get(field) is not None:
                data[field] = str(Decimal(data[field]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))

        return data    
        
# serializers.py

from .models import LoanAttachment, LoanCompletionAttachment

class LoanAttachmentSerializer(serializers.ModelSerializer):
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)

    class Meta:
        model = LoanAttachment
        fields = ['id', 'loan', 'loan_number', 'file', 'file_name', 'uploaded_at']
        read_only_fields = ['id', 'file_name', 'uploaded_at', 'loan_number']


class LoanCompletionAttachmentSerializer(serializers.ModelSerializer):
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LoanCompletionAttachment
        fields = [
            'id', 'loan', 'loan_number', 'file', 'file_url', 'file_name', 
            'file_type', 'description', 'uploaded_by', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_name', 'uploaded_at', 'updated_at', 'loan_number', 'file_url']

    def get_file_url(self, obj):
        """Return the full URL of the file"""
        if obj.file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
##############################################################################################################



from rest_framework import serializers
from .models import Loan, Customer, Item, Metal
from decimal import Decimal, ROUND_HALF_UP

class LoanGetUpdateSerializer(serializers.ModelSerializer):
    # Input: foreign key IDs
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
   
    metal_used_id = serializers.PrimaryKeyRelatedField(queryset=Metal.objects.all(), source='metal_used', write_only=True, required=False, allow_null=True)


    # Output: display names and direct item_name
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    metal_used_name = serializers.CharField(source='metal_used.name', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'loan_number', 'loan_date', 'status',
            'customer_id', 'customer_name',
            'item_name', # Added item_name directly
            # 'item_type_id', 'item_type_name', # Removed as it's not in your current Loan model
            'metal_used_id', 'metal_used_name',
            'pieces',
            'gross_weight', 'less_stone_weight', 'net_weight',
            'purity', 'value_per_gram',
            'current_value', 'hallmark_charge', 'tax',
            'final_amount', 'adjusted_loan_amount','paid_amount','balance_amount',
            'loan_return_period_unit', 'period_value', # Added these fields
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'loan_number', 'loan_date', 'status',
            'net_weight', 'current_value', 'final_amount','paid_amount','balance_amount',
            'created_at', 'updated_at',
            'customer_name', 'metal_used_name' # item_name is not read-only as per your model
        ]

    def to_representation(self, instance):
        """Ensure decimal values have two digits after the decimal point."""
        data = super().to_representation(instance)
        for field in ['gross_weight', 'less_stone_weight', 'net_weight', 'purity', 'value_per_gram',
                      'current_value', 'hallmark_charge', 'tax', 'final_amount', 'adjusted_loan_amount']:
            if data.get(field) is not None:
                # Ensure it's a Decimal before quantizing, then convert to string
                data[field] = str(Decimal(data[field]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        return data
    

#################################################################################################################

from rest_framework import serializers
from .models import LoanPayment, Loan # Make sure Loan model is imported
from decimal import Decimal, ROUND_HALF_UP # For formatting decimals

class LoanPaymentGetSerializer(serializers.ModelSerializer):
    # Add loan_number for easier identification
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)

    # Fields from the related Loan model
    loan_item_name = serializers.SerializerMethodField()
    loan_paid_amount = serializers.SerializerMethodField()
    loan_balance_amount = serializers.SerializerMethodField()

    class Meta:
        model = LoanPayment
        fields = [
            'id', 'loan', 'loan_number', 'payment_amount', 'payment_date',
            'status', 'payment_method', 'loan_return_period_unit',
            'period_value', 'amount', 'created_at',
            'loan_item_name', 'loan_paid_amount', 'loan_balance_amount' # Include the new fields
        ]
        read_only_fields = fields # All fields are read-only for a GET serializer

    def get_loan_item_name(self, obj):
        # obj here is a LoanPayment instance
        return obj.loan.item_name if obj.loan and obj.loan.item_name else None

    def get_loan_paid_amount(self, obj):
        # Format the decimal to two places, similar to your other serializers
        if obj.loan and obj.loan.paid_amount is not None:
            return str(Decimal(obj.loan.paid_amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        return None

    def get_loan_balance_amount(self, obj):
        # Format the decimal to two places
        if obj.loan and obj.loan.balance_amount is not None:
            return str(Decimal(obj.loan.balance_amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        return None

    
############################################################################################################

from rest_framework import serializers
from .models import LoanPayment, Loan # Import Loan model
from decimal import Decimal, ROUND_HALF_UP

class LoanPaymentSerializer(serializers.ModelSerializer):
    # Add a read-only field for loan number for better response readability
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)

    class Meta:
        model = LoanPayment
        fields = [
            'id', 'loan', 'loan_number', 'payment_amount', 'payment_date',
            'status', 'payment_method', 'loan_return_period_unit',
            'period_value', 'created_at'
        ]
        read_only_fields = ['id', 'loan_number', 'created_at']

    def validate(self, data):
        loan = data.get('loan')
        payment_amount = data.get('payment_amount')

        if not loan:
            raise serializers.ValidationError("A loan must be specified for the payment.")
        if payment_amount is None or payment_amount <= 0:
            raise serializers.ValidationError("Payment amount must be a positive value.")

        # Ensure adjusted_loan_amount is not None before proceeding with balance check
        adjusted_loan_amount = loan.adjusted_loan_amount if loan.adjusted_loan_amount is not None else Decimal('0.00')
        balance_amount = loan.balance_amount if loan.balance_amount is not None else adjusted_loan_amount # Default to adjusted if balance is None

        if balance_amount <= 0:
            raise serializers.ValidationError(f"Loan {loan.loan_number} is already fully paid.")

        if payment_amount > balance_amount:
            # Allow overpayment or partial payment up to balance, depending on business logic
            # For this scenario, we'll suggest a partial payment.
            raise serializers.ValidationError(
                f"Payment amount {payment_amount} exceeds the remaining balance {balance_amount:.2f} for loan {loan.loan_number}. "
                "Please enter an amount less than or equal to the balance."
            )
            
        return data

    def create(self, validated_data):
        loan = validated_data['loan']
        payment_amount = validated_data['payment_amount']

        # Save the LoanPayment instance first
        loan_payment = LoanPayment.objects.create(**validated_data)
        loan_payment.status = 'paid' # Mark this specific payment as paid
        loan_payment.save()

        # Update the Loan's paid_amount and balance_amount
        # Ensure we handle None values for adjusted_loan_amount, paid_amount, balance_amount
        adjusted_loan_amount = loan.adjusted_loan_amount if loan.adjusted_loan_amount is not None else Decimal('0.00')
        
        # Ensure paid_amount and balance_amount are Decimal objects before arithmetic
        loan.paid_amount = (loan.paid_amount if loan.paid_amount is not None else Decimal('0.00')) + payment_amount
        loan.balance_amount = adjusted_loan_amount - loan.paid_amount
        
        # Handle cases where balance goes to zero or below due to floating point or exact payment
        if loan.balance_amount < 0:
            loan.balance_amount = Decimal('0.00')

        # Optionally, update loan status if fully paid
        if loan.balance_amount <= 0:
            loan.status = 'Paid' # Or 'Closed', 'Completed' based on your definitions
        elif loan.status == 'Paid': # If balance is > 0 but status was 'Paid' (e.g. via an admin edit)
            loan.status = 'Active' # Revert to active if it's no longer fully paid
            
        loan.save(update_fields=['paid_amount', 'balance_amount', 'status']) # Save only changed fields for efficiency

        return loan_payment

#####################################################################################################

from rest_framework import serializers
from .models import OrderManagement

class OrderManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderManagement
        fields = ['id', 'order_no', 'customer_name', 'item', 'status', 'created_at']


#################################################################################################################

# from rest_framework import serializers
# from .models import JobWork, OrderManagement # Ensure OrderManagement is imported if used here

# class JobWorkSerializer(serializers.ModelSerializer):
#     # Add a read-only field for the absolute URL of the QR code
#     qr_code_url = serializers.SerializerMethodField(read_only=True)

#     # If you want to show order details in the response
#     order_details = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = JobWork
#         fields = "__all__" # Includes qr_code_image
#         read_only_fields = ['qr_code_image', 'qr_code_url', 'date', 'created_at', 'weight_net', 'balance_amount', 'wastage_weight']

#     def get_qr_code_url(self, obj):
#         request = self.context.get('request')
#         if obj.qr_code_image and request:
#             return request.build_absolute_uri(obj.qr_code_image.url)
#         return None

#     def get_order_details(self, obj):
#         if obj.order:
#             # You might want a dedicated OrderManagementSerializer for full details
#             return {
#                 'id': obj.order.id,
#                 'order_no': obj.order.order_no,
#                 'customer_name': obj.order.customer_name,
#                 'status': obj.order.status
#                 # ... other order fields you want to expose
#             }
#         return None


from rest_framework import serializers
from .models import JobWork, OrderManagement

class JobWorkSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField(read_only=True)
    order_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobWork
        fields = "__all__"
        read_only_fields = [
            'qr_code_image', 
            'qr_code_url', 
            'date', 
            'created_at', 
            'weight_net', 
            'balance_amount', 
            'wastage_weight'
        ]

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code_image and request:
            return request.build_absolute_uri(obj.qr_code_image.url)
        return None

    def get_order_details(self, obj):
        if obj.order:
            return {
                'id': obj.order.id,
                'order_no': obj.order.order_no,
                'customer_name': obj.order.customer_name,
                'status': obj.order.status
            }
        return None
#################################################################################################################


from rest_framework import serializers
from .models import MetalRate

class MetalRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalRate
        fields = "__all__"


from rest_framework import serializers
from .models import PurchaseVoucher

class PurchaseVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseVoucher
        fields = '__all__'



##########################################################################################################


from rest_framework import serializers
from .models import PurchaseItem

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'
        extra_kwargs = {
            field.name: {'required': False, 'allow_null': True}
            for field in model._meta.fields if field.name != 'id'
        }


class PurchaseItemMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['id', 'item', 'weight', 'rate', 'making', 'tax_percentage', 'total_amount']


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    items = PurchaseItemMiniSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseInvoice
        fields = "__all__"


#################################################################################################



# # serializers.py
# from rest_framework import serializers
# from .models import ItemPayment, InstallmentEntry

# class InstallmentEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstallmentEntry
#         fields = "__all__"

# class ItemPaymentSerializer(serializers.ModelSerializer):
#     installments = InstallmentEntrySerializer(many=True, read_only=True)

#     class Meta:
#         model = ItemPayment
#         fields = "__all__"

from rest_framework import serializers
from .models import ItemPayment, InstallmentEntry


class InstallmentEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentEntry
        fields = "__all__"


class ItemPaymentSerializer(serializers.ModelSerializer):
    installments = InstallmentEntrySerializer(many=True, read_only=True)

    # 🔽 EXPLICITLY declare this
    sale_item_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ItemPayment
        fields = "__all__"


        


from rest_framework import serializers
from .models import PurchaseItem

class PurchaseItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = [
            "id", "item", "hsn", "segment", "pieces", "weight",
            "rate", "making", "tax_percentage", "tax_amount",
            "base", "net", "total_amount", "hm", "comments",
            "attachment", "status"
        ]

#################################################################################################################

from rest_framework import serializers
from .models import ItemPayment, InstallmentEntry

class ItemPaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPayment
        fields = [
            'id', 'item_name', 'metal_type', 'start_date', 'total_amount', 'balance_amount',
            'installment_type', 'no_of_months', 'status'
        ]

# serializers.py

from rest_framework import serializers
from .models import InstallmentAttachment

class InstallmentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentAttachment
        fields = ["id", "installment", "file", "file_name", "uploaded_at"]
        
class InstallmentEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentEntry
        fields = ['item_payment_id', 'installment_date', 'amount', 'installment_type', 'count', 'payment_status']

class ItemPaymentDetailSerializer(serializers.ModelSerializer):
    installments = InstallmentEntrySerializer(many=True, read_only=True)

    class Meta:
        model = ItemPayment
        fields = "__all__"

###############################################################################################################################

from rest_framework import serializers
from .models import JobWork

class MasterJobworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobWork
        fields = [
            'id', 'craftsman_name', 'date', 'order_no', 'address', 
            'contact_no', 'metal_amount', 'paid_amount', 
            'balance_amount', 'qr_code_image', 'order_id'
        ]

#################################################################################################################


from rest_framework import serializers

class TransactionHistorySerializer(serializers.Serializer):
    installment_date = serializers.DateField()
    transaction_method = serializers.CharField()
    item_name = serializers.CharField()
    comment = serializers.CharField(allow_null=True)
    total_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    customer_name = serializers.CharField()
    customer_address = serializers.CharField()
    customer_contact_no = serializers.CharField()


from rest_framework import serializers
from .models import CraftsmanAttachment

class CraftsmanAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CraftsmanAttachment
        fields = ["id", "jobwork", "file", "uploaded_at"]


###################################################################################################################

from rest_framework import serializers
from .models import URDDetail, URDAdjustment


class URDDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = URDDetail
        fields = [
            'id', 'metal', 'item', 'pieces',
            'gross_weight', 'less_weight', 'net_weight',
            'rate', 'final_amount', 'comments', 'file', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

#################################################################################################################

class URDAdjustmentSerializer(serializers.ModelSerializer):
    urd_details = URDDetailSerializer(many=True, write_only=True)

    class Meta:
        model = URDAdjustment
        fields = [
            'id', 'sale_item',
            'adjust_amount', 'adjust_tax', 'adjust_hm_charges',
            'urd_details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        urd_details_data = validated_data.pop('urd_details', [])
        adjustment = URDAdjustment.objects.create(**validated_data)

        # ✅ Correct linkage between URDAdjustment and URDDetail
        for detail_data in urd_details_data:
            URDDetail.objects.create(
                urd_adjustment=adjustment,   # ✅ Fix: Link to adjustment
                sale_item=adjustment.sale_item,
                **detail_data
            )

        return adjustment


############################################################################################################

# from rest_framework import serializers
# from .models import URDAdjustment, URDDetail

# class URDDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = URDDetail
#         fields = '__all__'


# class URDAdjustmentSerializer(serializers.ModelSerializer):
#     urd_details = URDDetailSerializer(many=True, read_only=True)

#     class Meta:
#         model = URDAdjustment
#         fields = '__all__'


from rest_framework import serializers
from .models import URDAdjustment, URDDetail


class URDDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = URDDetail
        exclude = ["created_at", "sale_item", "urd_adjustment"]


class URDAllAdjustmentSerializer(serializers.ModelSerializer):
    urd_details = URDDetailSerializer(many=True)

    class Meta:
        model = URDAdjustment
        fields = "__all__"

    def create(self, validated_data):
        urd_details_data = validated_data.pop("urd_details", [])

        adjustment = URDAdjustment.objects.create(**validated_data)

        for detail in urd_details_data:
            URDDetail.objects.create(
                urd_adjustment=adjustment,
                sale_item=adjustment.sale_item,
                **detail
            )

        return adjustment


#################################################################################################################


# serializers.py
from rest_framework import serializers
from .models import Order

class DeleteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'salesperson_name', 'order_date', 'order_comments']

#########################################################################################################################


# notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'type', 'is_read', 'created_at']

#############################################################################################################


# serializers.py

from rest_framework import serializers
from .models import LoanPayment, Loan

class LoanPaymentdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = ['id', 'payment_amount', 'payment_date', 'status', 'payment_method', 'created_at']


###################################################################################################################################


from rest_framework import serializers
from .models import Bhishi, Customer
from decimal import Decimal, ROUND_HALF_UP


class BhishiCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Bhishi
        fields = [
            'id', 'bhishi_number', 'bhishi_date', 'status',
            'customer_id', 'customer_name',
            'bhishi_type', 'total_amount', 'per_installment',
            'total_installments', 'paid_amount', 'balance_amount',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'bhishi_number', 'status',
            'paid_amount', 'balance_amount', 'created_at', 'updated_at'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['total_amount', 'per_installment', 'paid_amount', 'balance_amount']:
            if data.get(field) is not None:
                data[field] = str(Decimal(data[field]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        return data

class BhishiGetUpdateSerializer(serializers.ModelSerializer):

    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Bhishi
        fields = [
            'id', 'bhishi_number', 'bhishi_date', 'status',
            'customer_id', 'customer_name',
            'bhishi_type', 'total_amount', 'per_installment',
            'total_installments', 'paid_amount', 'balance_amount',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'bhishi_number', 'paid_amount', 'balance_amount',
            'created_at', 'updated_at'
        ]

class BhishiPaymentSerializer(serializers.ModelSerializer):

    bhishi_number = serializers.CharField(source='bhishi.bhishi_number', read_only=True)

    class Meta:
        model = BhishiPayment
        fields = [
            'id', 'bhishi', 'bhishi_number', 'payment_amount',
            'payment_date', 'status', 'payment_method', 'created_at'
        ]
        read_only_fields = ['id', 'bhishi_number', 'created_at']

    def validate(self, data):
        bhishi = data['bhishi']
        payment_amount = data['payment_amount']

        if payment_amount <= 0:
            raise serializers.ValidationError("Amount must be positive.")

        if bhishi.balance_amount <= 0:
            raise serializers.ValidationError("Bhishi already completed.")

        if payment_amount > bhishi.balance_amount:
            raise serializers.ValidationError("Payment exceeds balance.")

        return data

    def create(self, validated_data):

        bhishi = validated_data['bhishi']
        amount = validated_data['payment_amount']

        payment = BhishiPayment.objects.create(**validated_data)
        payment.status = "paid"
        payment.save()

        bhishi.paid_amount = (bhishi.paid_amount or 0) + amount
        bhishi.balance_amount = bhishi.total_amount - bhishi.paid_amount

        if bhishi.balance_amount <= 0:
            bhishi.status = "Completed"
            bhishi.balance_amount = 0

        bhishi.save()

        return payment


# serializers.py

class BhishiAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BhishiAttachment
        fields = ['id', 'bhishi', 'file', 'file_name', 'uploaded_at']
        read_only_fields = ['id', 'file_name', 'uploaded_at']
#######################################################################################################################


from rest_framework import serializers
from .models import BhishiPayment

class BhishiPaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhishiPayment
        fields = [
            'id',
            'payment_amount',
            'payment_date',
            'status',
            'payment_method',
            'created_at'
        ]


#######################################################################################

class SupplierAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierAttachment
        fields = ["id", "purchase_invoice", "file", "uploaded_at"]

##########################################################################################################
#################################################################################################################

from rest_framework import serializers

from master.models import Customer
from master.models import Bhishi
from master.models import DiamondBilling
from master.models import Loan
from master.models import Order
from master.models import SaleItem


class CustomerSelfDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]


class CustomerBhishiDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bhishi
        exclude = ["created_at", "updated_at", "status"]


class CustomerDiamondBillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiamondBilling
        exclude = ["created_at"]


class CustomerLoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ["created_at", "updated_at", "status"]


class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["created_at"]


class CustomerSaleItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        exclude = ["created_at"]


class CustomerCompleteDataSerializer(serializers.Serializer):
    customer = CustomerSelfDetailSerializer()
    bhishi = CustomerBhishiDetailSerializer(many=True)
    diamond_billing = CustomerDiamondBillingDetailSerializer(many=True)
    loans = CustomerLoanDetailSerializer(many=True)
    orders = CustomerOrderDetailSerializer(many=True)
    sale_items = CustomerSaleItemDetailSerializer(many=True)
