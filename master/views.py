from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Bhishi, Customer,Notification,BhishiPayment, SupplierAttachment
from .serializers import BhishiCreateSerializer, BhishiGetUpdateSerializer, BhishiPaymentSerializer, CustomerBhishiDetailSerializer, CustomerDiamondBillingDetailSerializer, CustomerLoanDetailSerializer, CustomerOrderDetailSerializer, CustomerSaleItemDetailSerializer, CustomerSelfDetailSerializer, CustomerSerializer,SupplierAttachmentSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny


# CREATE & GET ALL CUSTOMERS
class CustomerListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        customers = Customer.objects.all().order_by('-created_at')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = CustomerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Customer created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()

            # Create a notification for customer creation
            Notification.objects.create(
                user=request.user if request.user.is_authenticated else None,  # optional: to assign notification to creator
                title="New Customer Added",
                message=f"Customer '{customer.name}' has been successfully created.",
                type="SUCCESS"
            )

            return Response({
                "message": "Customer created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

# GET, UPDATE, DELETE BY ID
class CustomerDetailAPIView(APIView):
    def get_object(self, customer_id):
        return get_object_or_404(Customer, customer_id=customer_id)

    def get(self, request, customer_id):
        customer = self.get_object(customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, customer_id):
        customer = self.get_object(customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id):
        customer = self.get_object(customer_id)
        customer.delete()
        return Response({"message": "Customer deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Metal, Carat
from .serializers import MetalSerializer, CaratSerializer


# ---------- METAL CRUD ----------
class MetalListCreateAPIView(APIView):
    def get(self, request):
        metals = Metal.objects.all().order_by('-created_at')
        serializer = MetalSerializer(metals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MetalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Metal created successfully!", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#################################################################################################################


class MetalDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Metal, id=id)

    def get(self, request, id):
        metal = self.get_object(id)
        serializer = MetalSerializer(metal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        metal = self.get_object(id)
        serializer = MetalSerializer(metal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Metal updated successfully!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        metal = self.get_object(id)
        metal.delete()
        return Response({"message": "Metal deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


# ---------- CARAT CRUD ----------
class CaratListCreateAPIView(APIView):
    def get(self, request):
        carats = Carat.objects.all().order_by('-created_at')
        serializer = CaratSerializer(carats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CaratSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Carat created successfully!", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#################################################################################################################


class CaratDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Carat, id=id)

    def get(self, request, id):
        carat = self.get_object(id)
        serializer = CaratSerializer(carat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        carat = self.get_object(id)
        serializer = CaratSerializer(carat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Carat updated successfully!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        carat = self.get_object(id)
        carat.delete()
        return Response({"message": "Carat deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Jewelry
from .serializers import JewelrySerializer
from django.db import transaction

class AddJewelryAPIView(APIView):
    def post(self, request):
        serializer = JewelrySerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    jewelry = serializer.save()
                    jewelry.save()  # Trigger QR generation
                    return Response({
                        "message": "Jewelry entry created successfully",
                        "data": JewelrySerializer(jewelry).data
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Jewelry
from .serializers import JewelrySerializer





class AddJewelryAPIView(APIView):
    def post(self, request):
        serializer = JewelrySerializer(data=request.data)
        if serializer.is_valid():
            jewelry = serializer.save()  # QR auto-generated in model
            return Response({
                "message": "Jewelry created successfully",
                "data": JewelrySerializer(jewelry).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

# ✅ LIST API
class JewelryListAPIView(APIView):
    def get(self, request):
        jewelries = Jewelry.objects.all().order_by('-created_at')
        serializer = JewelrySerializer(jewelries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ✅ RETRIEVE SINGLE ITEM
class JewelryDetailAPIView(APIView):
    def get(self, request, pk):
        jewelry = get_object_or_404(Jewelry, pk=pk)
        serializer = JewelrySerializer(jewelry)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################

# ✅ UPDATE API
class JewelryUpdateAPIView(APIView):
    def put(self, request, pk):
        jewelry = get_object_or_404(Jewelry, pk=pk)
        serializer = JewelrySerializer(jewelry, data=request.data, partial=True)
        if serializer.is_valid():
            updated_jewelry = serializer.save()
            updated_jewelry.save()  # regenerate QR if needed
            return Response({
                "message": "Jewelry updated successfully",
                "data": JewelrySerializer(updated_jewelry).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################


# ✅ DELETE API
class JewelryDeleteAPIView(APIView):
    def delete(self, request, pk):
        jewelry = get_object_or_404(Jewelry, pk=pk)
        jewelry.delete()
        return Response({"message": "Jewelry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#################################################################################################################


from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SaleItem
from .serializers import SaleItemSerializer

class SaleItemCreateAPIView(APIView):
    def post(self, request):

        # ✅ HANDLE ALL CASES
        if isinstance(request.data, list):
            items = request.data
            batch_id = None
        elif isinstance(request.data, dict) and "items" in request.data:
            items = request.data["items"]
            batch_id = request.data.get("saleitem_id")
        else:
            # single object → convert to list
            items = [request.data]
            batch_id = request.data.get("saleitem_id") if isinstance(request.data, dict) else None

        if batch_id is not None:
            try:
                batch_id = int(batch_id)
            except (TypeError, ValueError):
                return Response(
                    {"error": "saleitem_id must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if batch_id is None:
            last_batch = SaleItem.objects.aggregate(Max("saleitem_id"))["saleitem_id__max"] or 0
            batch_id = last_batch + 1

        for item in items:
            if isinstance(item, dict) and not item.get("saleitem_id"):
                item["saleitem_id"] = batch_id

        serializer = SaleItemSerializer(data=items, many=True)

        if serializer.is_valid():
            sale_items = serializer.save()

            return Response({
                "message": "Sale items created successfully",
                "count": len(sale_items),
                "saleitem_id": batch_id,
                "data": SaleItemSerializer(sale_items, many=True).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import SaleItem
from .serializers import SaleItemSerializer
from rest_framework.permissions import AllowAny  # You can replace with IsAuthenticated if needed


# ✅ 1. CREATE + LIST VIEW
class SaleItemListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Get list of all sale items, optionally filtered by salesperson or saleitem_id"""
        saleitem_id = request.query_params.get('saleitem_id')
        salesperson = request.query_params.get('salesperson')

        if saleitem_id:
            sale_items = SaleItem.objects.filter(saleitem_id=saleitem_id).order_by('-id')
        elif salesperson:
            sale_items = SaleItem.objects.filter(salesperson=salesperson).order_by('-id')
        else:
            sale_items = SaleItem.objects.all().order_by('-id')

        serializer = SaleItemSerializer(sale_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################

# ✅ 2. RETRIEVE, UPDATE, DELETE VIEW
class SaleItemDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        """Helper to get SaleItem or raise 404"""
        return get_object_or_404(SaleItem, pk=pk)

    def get(self, request, pk):
        """Retrieve single SaleItem"""
        sale_item = self.get_object(pk)
        serializer = SaleItemSerializer(sale_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update SaleItem"""
        sale_item = self.get_object(pk)
        serializer = SaleItemSerializer(sale_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sale Item updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete SaleItem"""
        sale_item = self.get_object(pk)
        sale_item.delete()
        return Response({"message": "Sale Item deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class SaleItemBulkUpdateAPIView(APIView):
    def put(self, request):

        # Handle all formats
        if isinstance(request.data, list):
            items = request.data
        elif isinstance(request.data, dict) and "items" in request.data:
            items = request.data["items"]
        else:
            return Response(
                {"error": "Invalid format. Expected list or items[]"},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_items = []
        errors = []

        for item in items:
            item_id = item.get("id")

            if not item_id:
                errors.append({"error": "ID is required", "data": item})
                continue

            try:
                instance = SaleItem.objects.get(id=item_id)
            except SaleItem.DoesNotExist:
                errors.append({"error": f"SaleItem {item_id} not found"})
                continue

            serializer = SaleItemSerializer(instance, data=item, partial=True)

            if serializer.is_valid():
                serializer.save()
                updated_items.append(serializer.data)
            else:
                errors.append(serializer.errors)

        return Response({
            "message": "Bulk update completed",
            "updated_count": len(updated_items),
            "updated_items": updated_items,
            "errors": errors
        }, status=status.HTTP_200_OK)

################################################################################################################################
# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import URDAdjustment
from .serializers import URDAllAdjustmentSerializer
from rest_framework.permissions import AllowAny

class URDAdjustmentCreateAPIView(generics.CreateAPIView):
    serializer_class = URDAllAdjustmentSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adjustment = serializer.save()
        return Response({
            "message": "URD Adjustment and related details saved successfully.",
            "data": URDAllAdjustmentSerializer(adjustment).data
        }, status=status.HTTP_201_CREATED)





######################################################################################################################################

# views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class OrderCreateAPIView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################################################################################
# from decimal import Decimal
# from django.db.models import Sum
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.exceptions import NotFound
# from .models import Order, OrderItem
# from .serializers import OrderSerializer

# class OrderUpdateAPIView(APIView):
#     def put(self, request, order_id):
#         try:
#             # Retrieve the existing Order by order_id
#             order = Order.objects.get(order_id=order_id)
#         except Order.DoesNotExist:
#             raise NotFound(detail="Order not found.")

#         # Deserialize the incoming data and update the order with partial=True to allow optional fields
#         serializer = OrderSerializer(order, data=request.data, partial=True)  # Use partial=True to allow partial updates
#         if serializer.is_valid():
#             # Save the updated order (this updates fields of the Order itself)
#             updated_order = serializer.save()

#             # Initialize totals
#             total_item_amount = Decimal(0)
#             total_tax = Decimal(0)
#             total_making = Decimal(0)

#             # Check if items are provided in the request
#             if not request.data.get("items"):
#                 return Response({"error": "No items provided to update."}, status=status.HTTP_400_BAD_REQUEST)

#             # Iterate over the items in the request data and update existing order items
#             for item_data in request.data.get("items", []):
#                 item_id = item_data.get('id', None)
#                 if item_id:
#                     try:
#                         # Fetch the existing OrderItem based on item_id and order_id
#                         order_item = OrderItem.objects.get(id=item_id, order=order)

#                         # Update the fields for this existing OrderItem
#                         order_item.qr_barcode = item_data.get('qr_barcode', order_item.qr_barcode)
#                         order_item.huid_number = item_data.get('huid_number', order_item.huid_number)
#                         order_item.metal_type = item_data.get('metal_type', order_item.metal_type)
#                         order_item.item_name = item_data.get('item_name', order_item.item_name)
#                         order_item.purity = Decimal(item_data.get('purity', order_item.purity))
#                         order_item.gross_weight = Decimal(item_data.get('gross_weight', order_item.gross_weight))
#                         order_item.less_weight = Decimal(item_data.get('less_weight', order_item.less_weight))
#                         order_item.net_weight = Decimal(item_data.get('net_weight', order_item.net_weight))
#                         order_item.rate_per_gram = Decimal(item_data.get('rate_per_gram', order_item.rate_per_gram))
#                         order_item.making_charge = Decimal(item_data.get('making_charge', order_item.making_charge))
#                         order_item.stone_charge = Decimal(item_data.get('stone_charge', order_item.stone_charge))
#                         order_item.hallmark_charge = Decimal(item_data.get('hallmark_charge', order_item.hallmark_charge))
#                         order_item.gst_percent = Decimal(item_data.get('gst_percent', order_item.gst_percent))
#                         order_item.hm_tax_percent = Decimal(item_data.get('hm_tax_percent', order_item.hm_tax_percent))
#                         order_item.comments = item_data.get('comments', order_item.comments)

#                         # Recalculate the total price for this item
#                         order_item.total_price = (
#                             (order_item.net_weight * order_item.rate_per_gram) +
#                             order_item.making_charge +
#                             order_item.stone_charge +
#                             order_item.hallmark_charge +
#                             ((order_item.net_weight * order_item.rate_per_gram) * (order_item.gst_percent + order_item.hm_tax_percent) / Decimal(100))
#                         )

#                         order_item.save()  # Save the updated OrderItem

#                     except OrderItem.DoesNotExist:
#                         return Response({"error": f"OrderItem with id {item_id} not found in this order."}, status=status.HTTP_400_BAD_REQUEST)

#             # Recalculate the totals for the Order
#             total_item_amount = sum(item.total_price for item in order.items.all())
#             total_tax = sum(item.total_price * (item.gst_percent / Decimal(100)) for item in order.items.all())
#             total_making = sum(item.making_charge for item in order.items.all())

#             # Handle any adjustments for discount, URD, etc.
#             discount_amt = (total_item_amount * Decimal(request.data.get("discount_percent", 0))) / Decimal(100)
#             urd_value = Decimal(request.data.get("urd_weight", 0)) * Decimal(request.data.get("urd_rate", 0))

#             # Recalculate grand total and balance due
#             grand_total = (total_item_amount + total_tax) - discount_amt - urd_value
#             balance_due = grand_total - updated_order.payments.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)

#             # Update the Order totals
#             updated_order.item_total = total_item_amount
#             updated_order.making_total = total_making
#             updated_order.tax_total = total_tax
#             updated_order.discount_amount = discount_amt
#             updated_order.grand_total = grand_total
#             updated_order.balance_due = balance_due
#             updated_order.save()

#             return Response({"message": "Order updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Order
from .serializers import OrderSerializer


class OrderUpdateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, order_id):

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            raise NotFound("Order not found")

        serializer = OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # update logic runs inside serializer
            return Response(
                {
                    "message": "Order updated successfully!",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import GetOrderSerializer


class OrderListAPIView(APIView):
    """GET all orders"""
    def get(self, request):
        # ✅ FIX: order_by('-order_id') instead of '-id'
        orders = Order.objects.all().order_by('-order_id')
        serializer = GetOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################

class OrderDetailAPIView(APIView):
    """GET order details with items & payments"""
    def get(self, request, order_id):
        # ✅ FIX: use order_id=order_id instead of pk=pk
        order = get_object_or_404(Order, order_id=order_id)
        serializer = GetOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DiamondBilling
from .serializers import DiamondBillingSerializer


class DiamondBillingCreateAPIView(APIView):
    def post(self, request):
        serializer = DiamondBillingSerializer(data=request.data)
        if serializer.is_valid():
            billing = serializer.save()
            return Response(DiamondBillingSerializer(billing).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

# views.py
# from django.db import connection
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny

# class TransactionListAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         b.billing_id AS transaction_id,
#                         b.billing_date,
#                         c.name AS customer_name,
#                         c.contact_no AS mobile,
#                         b.net_amount AS net,
#                         b.paid_amount AS paid,
#                         b.balance_amount AS balance
#                     FROM master_diamondbilling b
#                     INNER JOIN master_customer c 
#                         ON b.customer_id = c.customer_id
#                     ORDER BY b.billing_date DESC
#                 """)
#                 columns = [col[0] for col in cursor.description]
#                 data = [dict(zip(columns, row)) for row in cursor.fetchall()]

#             return Response(data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class TransactionListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        b.billing_id AS transaction_id,
                        b.billing_date,
                        c.name AS customer_name,
                        c.contact_no AS mobile,

                        -- 🔽 Newly added fields
                        b.diamond_subtotal,
                        b.metal_subtotal,

                        b.net_amount AS net,
                        b.paid_amount AS paid,
                        b.balance_amount AS balance
                    FROM master_diamondbilling b
                    INNER JOIN master_customer c 
                        ON b.customer_id = c.customer_id
                    ORDER BY b.billing_date DESC
                """)

                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return Response(
                {
                    "count": len(data),
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

#################################################################################################################


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import connection


# class BillingDetailAPIView(APIView):
#     def get(self, request, billing_id):
#         with connection.cursor() as cursor:
#             query = """
#                 SELECT 
#                     b.billing_id,
#                     b.billing_date,

#                     -- 🔽 Newly added fields
#                     b.diamond_subtotal,
#                     b.metal_subtotal,

#                     b.net_amount,
#                     b.paid_amount,
#                     b.balance_amount,

#                     c.name AS customer_name,
#                     c.contact_no AS customer_mobile,

#                     d.*,
#                     m.*
#                 FROM master_diamondbilling b
#                 LEFT JOIN master_diamonddetail d 
#                     ON b.billing_id = d.billing_id
#                 LEFT JOIN master_diamondmetalinfo m 
#                     ON b.billing_id = m.billing_id
#                 LEFT JOIN master_customer c 
#                     ON b.customer_id = c.customer_id
#                 WHERE b.billing_id = %s
#             """
#             cursor.execute(query, [billing_id])

#             columns = [col[0] for col in cursor.description]
#             results = [
#                 dict(zip(columns, row))
#                 for row in cursor.fetchall()
#             ]

#         if not results:
#             return Response(
#                 {"error": "Billing ID not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         return Response(
#             {
#                 "billing_id": billing_id,
#                 "data": results
#             },
#             status=status.HTTP_200_OK
#         )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class BillingDetailAPIView(APIView):
    def get(self, request, billing_id):
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    b.billing_id,
                    b.billing_date,

                    -- Billing amounts
                    b.diamond_subtotal,
                    b.metal_subtotal,
                    b.net_amount,
                    b.paid_amount,
                    b.balance_amount,

                    -- Customer info
                    c.name AS customer_name,
                    c.contact_no AS customer_mobile,

                    -- Diamond details
                    d.*,

                    -- Metal billing info
                    m.*,

                    -- 🔽 Metal master fields
                    mm.metal_name,
                    mm.type AS metal_type

                FROM master_diamondbilling b

                LEFT JOIN master_diamonddetail d 
                    ON b.billing_id = d.billing_id

                LEFT JOIN master_diamondmetalinfo m 
                    ON b.billing_id = m.billing_id

                -- 🔽 JOIN metal master table
                LEFT JOIN master_metal mm
                    ON m.metal_id = mm.id

                LEFT JOIN master_customer c 
                    ON b.customer_id = c.customer_id

                WHERE b.billing_id = %s
            """

            cursor.execute(query, [billing_id])

            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        if not results:
            return Response(
                {"error": "Billing ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "billing_id": billing_id,
                "data": results
            },
            status=status.HTTP_200_OK
        )


############################################################################################################
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Loan
from .serializers import LoanCreateSerializer

class LoanSerializer(LoanCreateSerializer): # General serializer for GET requests
    class Meta(LoanCreateSerializer.Meta):
        fields = [
            'id', 'loan_number', 'loan_date', 'status',
            'customer_name', 'item_type_name', 'metal_used_name',
            'pieces', # Added 'pieces'
            'gross_weight', 'less_stone_weight', 'net_weight', 'purity', 'value_per_gram',
            'current_value', 'hallmark_charge', 'tax', 'final_amount', 'adjusted_loan_amount',
            'remarks',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = fields # All fields are read-only for a general list/retrieve view

###############################################################################################################

# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .models import Loan
# from .serializers import LoanCreateSerializer

# class LoanCreateAPIView(generics.CreateAPIView):
#     queryset = Loan.objects.all()
#     serializer_class = LoanCreateSerializer
#     # permission_classes = [IsAuthenticated] # Uncomment if you need authentication

#     def perform_create(self, serializer):
#         serializer.save()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Loan
from .serializers import LoanCreateSerializer
from master.models import Notification  # Import Notification model
from django.contrib.auth.models import User  # If you want to assign notification to a user
from rest_framework.permissions import AllowAny

class LoanCreateAPIView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated if needed

    def perform_create(self, serializer):
        self.loan = serializer.save()  # Save loan and store it for later use

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Create notification after loan save
        loan = self.loan
        customer_name = loan.customer.name if hasattr(loan.customer, 'name') else "Customer"
        adjusted_loan_amount = loan.adjusted_loan_amount if hasattr(loan, 'adjusted_loan_amount') else 'N/A'

        Notification.objects.create(
            title="New Loan Created",
            message=f"Loan of amount ₹{adjusted_loan_amount} created for {customer_name}.",
            type="SUCCESS"
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# views.py

from rest_framework.parsers import MultiPartParser, FormParser
from .models import LoanAttachment
from .serializers import LoanAttachmentSerializer

class LoanAttachmentCreateAPIView(generics.CreateAPIView):
    queryset = LoanAttachment.objects.all()
    serializer_class = LoanAttachmentSerializer
    permission_classes = [AllowAny]

    parser_classes = [MultiPartParser, FormParser]  # IMPORTANT for file upload

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attachment = serializer.save()

        return Response(
            {
                "message": "Attachment uploaded successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class LoanAttachmentListAPIView(generics.ListAPIView):
    serializer_class = LoanAttachmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = LoanAttachment.objects.select_related('loan').all().order_by('-uploaded_at')

        loan_id = self.request.query_params.get('loan_id')

        if loan_id:
            queryset = queryset.filter(loan_id=loan_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {"message": "No attachments found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    
    

#################################################################################################################
# ✅ LOAN COMPLETION ATTACHMENT APIs
#################################################################################################################

from rest_framework.parsers import MultiPartParser, FormParser
from .models import LoanCompletionAttachment
from .serializers import LoanCompletionAttachmentSerializer


class LoanCompletionAttachmentUploadAPIView(APIView):
    """
    POST: Upload attachment for loan completion
    - Requires: loan, file, file_type, uploaded_by
    - Optional: description
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        try:
            loan_id = request.data.get('loan')
            file = request.FILES.get('file')
            file_type = request.data.get('file_type', 'document')
            description = request.data.get('description', '')
            uploaded_by = request.data.get('uploaded_by', 'Unknown')

            # Validate required fields
            if not loan_id:
                return Response(
                    {"error": "Loan ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not file:
                return Response(
                    {"error": "File is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if loan exists
            try:
                loan = Loan.objects.get(id=loan_id)
            except Loan.DoesNotExist:
                return Response(
                    {"error": f"Loan with ID {loan_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create attachment
            attachment = LoanCompletionAttachment.objects.create(
                loan=loan,
                file=file,
                file_type=file_type,
                description=description,
                uploaded_by=uploaded_by
            )

            serializer = LoanCompletionAttachmentSerializer(
                attachment,
                context={'request': request}
            )

            return Response(
                {
                    "message": "Attachment uploaded successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoanCompletionAttachmentListAPIView(APIView):
    """
    GET: Retrieve all loan completion attachments
    - Query params: loan_id (optional), file_type (optional)
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            loan_id = request.query_params.get('loan_id')
            file_type = request.query_params.get('file_type')

            # Base queryset
            queryset = LoanCompletionAttachment.objects.select_related('loan').all()

            # Filter by loan_id if provided
            if loan_id:
                try:
                    queryset = queryset.filter(loan_id=int(loan_id))
                except ValueError:
                    return Response(
                        {"error": "Invalid loan_id"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Filter by file_type if provided
            if file_type:
                queryset = queryset.filter(file_type=file_type)

            if not queryset.exists():
                return Response(
                    {
                        "message": "No attachments found",
                        "data": []
                    },
                    status=status.HTTP_200_OK
                )

            serializer = LoanCompletionAttachmentSerializer(
                queryset,
                many=True,
                context={'request': request}
            )

            return Response(
                {
                    "message": "Attachments retrieved successfully",
                    "count": queryset.count(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoanCompletionAttachmentDetailAPIView(APIView):
    """
    GET: Retrieve single loan completion attachment
    DELETE: Delete loan completion attachment
    """
    permission_classes = [AllowAny]

    def get(self, request, attachment_id, *args, **kwargs):
        try:
            attachment = LoanCompletionAttachment.objects.get(id=attachment_id)

            serializer = LoanCompletionAttachmentSerializer(
                attachment,
                context={'request': request}
            )

            return Response(
                {
                    "message": "Attachment retrieved successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except LoanCompletionAttachment.DoesNotExist:
            return Response(
                {"error": f"Attachment with ID {attachment_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, attachment_id, *args, **kwargs):
        try:
            attachment = LoanCompletionAttachment.objects.get(id=attachment_id)
            loan_id = attachment.loan.id

            # Delete file from storage
            if attachment.file:
                attachment.file.delete()

            attachment.delete()

            return Response(
                {
                    "message": "Attachment deleted successfully",
                    "deleted_id": attachment_id,
                    "loan_id": loan_id
                },
                status=status.HTTP_200_OK
            )

        except LoanCompletionAttachment.DoesNotExist:
            return Response(
                {"error": f"Attachment with ID {attachment_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoanCompletionAttachmentByLoanAPIView(APIView):
    """
    GET: Retrieve all attachments for a specific loan
    """
    permission_classes = [AllowAny]

    def get(self, request, loan_id, *args, **kwargs):
        try:
            # Check if loan exists
            try:
                loan = Loan.objects.get(id=loan_id)
            except Loan.DoesNotExist:
                return Response(
                    {"error": f"Loan with ID {loan_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get all attachments for the loan
            attachments = LoanCompletionAttachment.objects.filter(
                loan=loan
            ).order_by('-uploaded_at')

            if not attachments.exists():
                return Response(
                    {
                        "message": "No attachments found for this loan",
                        "loan_id": loan_id,
                        "data": []
                    },
                    status=status.HTTP_200_OK
                )

            serializer = LoanCompletionAttachmentSerializer(
                attachments,
                many=True,
                context={'request': request}
            )

            return Response(
                {
                    "message": "Attachments retrieved successfully",
                    "loan_id": loan_id,
                    "count": attachments.count(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

#################################################################################################################
#     queryset = Loan.objects.all()
#     serializer_class = LoanCreateSerializer
#     lookup_field = 'id'
#     permission_classes = [AllowAny]

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Loan
from .serializers import LoanCreateSerializer
from master.models import Notification


class LoanUpdateAPIView(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        self.loan = serializer.save()  # Save updated instance

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # allow partial update
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # OPTIONAL: Notification for update
        loan = self.loan
        customer_name = loan.customer.name if loan.customer else "Customer"

        Notification.objects.create(
            title="Loan Updated",
            message=f"Loan {loan.loan_number} updated for {customer_name}.",
            type="INFO"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
#######################################################################################################################

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Loan
from .serializers import LoanGetUpdateSerializer


class LoanListAPIView(generics.ListAPIView):
    serializer_class = LoanGetUpdateSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        If ?status=<value> is passed, filter by status.
        Otherwise, return all loans that are not soft-deleted.
        """
        status_param = self.request.query_params.get('status', None)

        # ✅ Filter only non-deleted loans
        queryset = Loan.objects.filter(is_deleted=False).order_by('-created_at')

        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Custom list method to show friendly messages.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            status_filter = request.query_params.get('status', 'all')
            return Response(
                {"message": f"No active loan records found for status: {status_filter}"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################


# ✅ GET SINGLE LOAN DETAILS
class LoanDetailAPIView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanGetUpdateSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]


#################################################################################################################


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .models import LoanPayment
# from .serializers import LoanPaymentSerializer,LoanPaymentGetSerializer # Ensure LoanPaymentGetSerializer is imported

# class LoanPaymentAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # Use select_related to prefetch the related Loan object
#         # This prevents N+1 query problems, making it more efficient
#         payments = LoanPayment.objects.select_related('loan').all().order_by('-payment_date')
#         serializer = LoanPaymentGetSerializer(payments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import LoanPayment
from .serializers import LoanPaymentGetSerializer

class LoanPaymentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Start with all payments, prefetching the related Loan object
        payments = LoanPayment.objects.select_related('loan').all()

        # Check for a 'id' query parameter (the LoanPayment id, not the loan_id)
        loan_payment_id = request.query_params.get('id')  # You can pass 'id' as the query parameter

        if loan_payment_id:
            try:
                # Filter payments by the provided loan_payment_id
                payments = payments.filter(id=int(loan_payment_id))  # Use LoanPayment's id field here
                if not payments:
                    return Response(
                        {"detail": f"No payments found for loan_payment_id {loan_payment_id}."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except ValueError:
                return Response(
                    {"detail": "Invalid id provided. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Order the results (if there are multiple payments)
        payments = payments.order_by('-payment_date', '-created_at')  # Order by payment_date and created_at for stability

        # Serialize the filtered payments
        serializer = LoanPaymentGetSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST — Make a loan payment (keeping this for context, ensure it uses LoanPaymentSerializer)
    def post(self, request):
        serializer = LoanPaymentSerializer(data=request.data)
        if serializer.is_valid():
            loan_payment = serializer.save()
            
            loan = loan_payment.loan
            response_message = "Payment recorded successfully."
            if loan.balance_amount <= 0:
                response_message += f" Loan {loan.loan_number} is now fully paid."
            
            return Response({"message": response_message, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # POST — Make a loan payment (Keeping this here for context, ensure it uses LoanPaymentSerializer)
    # def post(self, request):
    #     serializer = LoanPaymentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         loan_payment = serializer.save()
            
    #         loan = loan_payment.loan
    #         response_message = "Payment recorded successfully."
    #         if loan.balance_amount <= 0:
    #             response_message += f" Loan {loan.loan_number} is now fully paid."
            
    #         return Response({"message": response_message, "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
#################################################################################################################

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # Use IsAuthenticated as needed
from .models import LoanPayment # Import LoanPayment model
from .serializers import LoanPaymentSerializer

class LoanPaymentAddAPIView(generics.CreateAPIView):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer
    permission_classes = [AllowAny] # Use IsAuthenticated if users need to be logged in

    # The create method can be simplified as the logic is now in the serializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # The serializer's create method will handle saving the payment and updating the loan
        loan_payment = serializer.save() 
        
        # Access the updated loan directly from the payment object
        loan = loan_payment.loan 
        
        response_message = "Payment recorded successfully."
        if loan.balance_amount <= 0:
            response_message += f" Loan {loan.loan_number} is now fully paid."
            
        return Response(
            {"message": response_message, "data": serializer.data}, 
            status=status.HTTP_201_CREATED
        )

##########################################################################################################################


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import OrderManagement

#@method_decorator(csrf_exempt, name='dispatch')
class OrderManagementCreateView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))

            order_no = data.get('order_no')
            customer_name = data.get('customer_name')
            item = data.get('item')

            if not all([order_no, customer_name, item]):
                return JsonResponse({'error': 'All fields are required: order_no, customer_name, item'}, status=400)

            # Create new order with status = Pending by default
            order = OrderManagement.objects.create(
                order_no=order_no,
                customer_name=customer_name,
                item=item,
                status='Assign'
            )

            return JsonResponse({
                'message': 'Order created successfully',
                'order': {
                    'id': order.id,
                    'order_no': order.order_no,
                    'customer_name': order.customer_name,
                    'item': order.item,
                    'status': order.status,
                    'created_at': order.created_at
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


#############################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderManagement
from .serializers import OrderManagementSerializer

# ✅ GET API — Status-wise Order Listing
class OrderStatusListView(APIView):
    def get(self, request):
        status_param = request.query_params.get('status')
        if status_param:
            orders = OrderManagement.objects.filter(status=status_param)
        else:
            orders = OrderManagement.objects.all()
        
        serializer = OrderManagementSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#################################################################################################################

# ✅ PUT API — Change Order Status
class OrderStatusUpdateView(APIView):
    def put(self, request, pk):
        try:
            order = OrderManagement.objects.get(pk=pk)
        except OrderManagement.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_status = request.data.get("status")
        valid_status = dict(OrderManagement.STATUS_CHOICES).keys()

        if new_status not in valid_status:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        serializer = OrderManagementSerializer(order)
        return Response({
            "message": f"Order status updated to {new_status}",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


#########################################################################################################################

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from django.shortcuts import get_object_or_404
# from .models import JobWork  # your master_jobwork model


# class JobWorkDeleteAPIView(APIView):
#     permission_classes = [AllowAny]

#     def delete(self, request, id=None):
#         if not id:
#             return Response(
#                 {"status": False, "message": "id is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Fetch record
#         jobwork = get_object_or_404(JobWork, id=id)

#         # Delete record
#         jobwork.delete()

#         return Response(
#             {"status": True, "message": "Job Work deleted successfully"},
#             status=status.HTTP_200_OK
#         )


#################################################################################################################

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import JobWork, OrderManagement # Ensure OrderManagement is imported
# from .serializers import JobWorkSerializer

# class JobWorkCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Pass the request context to the serializer for generating absolute URLs
#         serializer = JobWorkSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save() # The QR code generation happens in the model's save method
#             return Response({
#                 "message": "Job Work Created Successfully. Order status updated to Processing.",
#                 "data": serializer.data # This will now include qr_code_image path and qr_code_url
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobWork, OrderManagement
from .serializers import JobWorkSerializer

class JobWorkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JobWorkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Job Work Created Successfully. Order status updated to Processing.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# You'll likely want List and Detail views for JobWork too:
class JobWorkListAPIView(generics.ListAPIView):
    queryset = JobWork.objects.all()
    serializer_class = JobWorkSerializer
    # permission_classes = [IsAuthenticated] # Example

class JobWorkDetailAPIView(generics.RetrieveAPIView):
    queryset = JobWork.objects.all()
    serializer_class = JobWorkSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated] # Example




from .models import OrderManagement


class OrderMarkCompletedAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order_id = request.data.get("order") or request.data.get("order_id")

        if not order_id:
            return Response(
                {"error": "order or order_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = OrderManagement.objects.get(id=order_id)
        except OrderManagement.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Optional safety check
        if order.status != "Processing":
            return Response(
                {
                    "error": f"Order status must be Processing to complete. Current status: {order.status}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "Completed"
        order.save(update_fields=["status"])

        return Response(
            {
                "message": "Order status updated to Completed successfully",
                "data": {
                    "order_id": order.id,
                    "order_no": order.order_no,
                    "customer_name": order.customer_name,
                    "status": order.status
                }
            },
            status=status.HTTP_200_OK
        )

#################################################################################################################

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import MetalRate
# from .serializers import MetalRateSerializer
# from django.utils import timezone

# class MetalRateCreateAPIView(APIView):
#     def post(self, request):
#         # Set date automatically to today's date
#         data = request.data.copy()
#         data['date'] = timezone.now().date()

#         serializer = MetalRateSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Today's metal rate added successfully.",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MetalRate
from .serializers import MetalRateSerializer
from django.utils import timezone
from django.utils import timezone

class MetalRateCreateAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['date'] = timezone.localdate()   # FIXED

        serializer = MetalRateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Today's metal rate added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

class MetalRateUpdateAPIView(APIView):
    """PUT API — Update existing metal rate by ID"""
    def put(self, request, pk):
        try:
            metal_rate = MetalRate.objects.get(pk=pk)
        except MetalRate.DoesNotExist:
            return Response(
                {"error": "Metal rate not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MetalRateSerializer(metal_rate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Metal rate updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import MetalRate
from .serializers import MetalRateSerializer

class MetalRateListAPIView(APIView):
    def get(self, request):
        date_param = request.query_params.get('date', None)

        if date_param:
            # Parse the date from query string
            parsed_date = parse_date(date_param)
            if not parsed_date:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                                status=status.HTTP_400_BAD_REQUEST)

            metals = MetalRate.objects.filter(date=parsed_date).order_by('metal_name')
            if not metals.exists():
                return Response({"message": f"No records found for {parsed_date}."},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = MetalRateSerializer(metals, many=True)
            return Response({
                "date": str(parsed_date),
                "total_records": metals.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # If no date is provided → show latest 20 date-wise entries
        metals = MetalRate.objects.all().order_by('-date')[:20]
        serializer = MetalRateSerializer(metals, many=True)
        return Response({
            "message": "Latest 20 metal rate records",
            "total_records": metals.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseVoucher
from .serializers import PurchaseVoucherSerializer

# ✅ POST API — Create a new purchase voucher
class PurchaseVoucherCreateAPIView(APIView):
    def post(self, request):
        serializer = PurchaseVoucherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Purchase voucher created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################

# ✅ GET List API — List all vouchers
class PurchaseVoucherListAPIView(APIView):
    def get(self, request):
        vouchers = PurchaseVoucher.objects.all().order_by('-created_at')
        serializer = PurchaseVoucherSerializer(vouchers, many=True)
        return Response({
            "total_records": vouchers.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#################################################################################################################

# ✅ GET Details API — Get details by ID
class PurchaseVoucherDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            voucher = PurchaseVoucher.objects.get(pk=pk)
        except PurchaseVoucher.DoesNotExist:
            return Response({"error": "Purchase voucher not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseVoucherSerializer(voucher)
        return Response(serializer.data, status=status.HTTP_200_OK)


#################################################################################################################



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from decimal import Decimal
from .models import PurchaseItem
from .serializers import PurchaseItemSerializer

class AddPurchaseItemAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        data = request.data.copy()

        # ✅ Calculate numeric fields safely
        weight = Decimal(data.get('weight', 0) or 0)
        rate = Decimal(data.get('rate', 0) or 0)
        making = Decimal(data.get('making', 0) or 0)
        tax_percentage = Decimal(data.get('tax_percentage', 0) or 0)

        base = weight * rate
        net = base + making
        tax_amount = (net * tax_percentage) / 100
        total_amount = net + tax_amount

        # ✅ Auto-fill calculated + default values
        data['base'] = base
        data['net'] = net
        data['tax_amount'] = tax_amount
        data['total_amount'] = total_amount
        data['status'] = data.get('status', 'P')  # Default Pending

        serializer = PurchaseItemSerializer(data=data)
        if serializer.is_valid():
            purchase_item = serializer.save()

            # ✅ Optional attachment
            if 'attachment' in request.FILES:
                purchase_item.attachment = request.FILES['attachment']
                purchase_item.save()

            return Response({
                "message": "Purchase item added successfully",
                "data": PurchaseItemSerializer(purchase_item).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#################################################################################################################


class UpdatePurchaseItemAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        try:
            purchase_item = PurchaseItem.objects.get(id=pk)
        except PurchaseItem.DoesNotExist:
            return Response({"error": "Purchase item not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        # Optional re-calculations if any field changes
        weight = Decimal(data.get('weight', purchase_item.weight or 0))
        rate = Decimal(data.get('rate', purchase_item.rate or 0))
        making = Decimal(data.get('making', purchase_item.making or 0))
        tax_percentage = Decimal(data.get('tax_percentage', purchase_item.tax_percentage or 0))

        base = weight * rate
        net = base + making
        tax_amount = (net * tax_percentage) / 100
        total_amount = net + tax_amount

        data['base'] = base
        data['net'] = net
        data['tax_amount'] = tax_amount
        data['total_amount'] = total_amount

        serializer = PurchaseItemSerializer(purchase_item, data=data, partial=True)
        if serializer.is_valid():
            updated_item = serializer.save()

            if 'attachment' in request.FILES:
                updated_item.attachment = request.FILES['attachment']
                updated_item.save()

            return Response({
                "message": "Purchase item updated successfully",
                "data": PurchaseItemSerializer(updated_item).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import PurchaseItem
from .serializers import PurchaseItemSerializer

# class PurchaseItemListAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         supplier_id = request.query_params.get('supplier_id')
#         status_filter = request.query_params.get('status')

#         # Start with all items
#         items = PurchaseItem.objects.all()

#         # If supplier_id is provided, filter by it
#         if supplier_id:
#             items = items.filter(supplier_id=supplier_id) # Corrected filter

#         # If status_filter is provided, filter by it
#         if status_filter:
#             items = items.filter(status=status_filter)

#         serializer = PurchaseItemSerializer(items, many=True)
#         return Response({
#             "count": items.count(),
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)


class PurchaseItemListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        supplier_id = request.query_params.get('supplier_id')
        status_filter = request.query_params.get('status')
        mode_filter = request.query_params.get('mode')   # NEW

        # Start with all purchase items
        items = PurchaseItem.objects.all()

        # Filter by supplier
        if supplier_id:
            items = items.filter(supplier_id=supplier_id)

        # Filter by status
        if status_filter:
            items = items.filter(status=status_filter)

        # ⭐ Filter by mode (via related PurchaseInvoice)
        if mode_filter:
            items = items.filter(invoice__mode__iexact=mode_filter)

        serializer = PurchaseItemSerializer(items, many=True)
        return Response({
            "count": items.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from decimal import Decimal
from .models import PurchaseInvoice, PurchaseItem
from .serializers import PurchaseInvoiceSerializer
from .utils import to_decimal  # helper function



##############################################################################################################

#Update 19 Nov


class AddPurchaseInvoiceAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        try:
            supplier_name = request.data.get("supplier_name")
            bill_no = request.data.get("bill_no")
            date = request.data.get("date")
            contact_number = request.data.get("contact_number")
            email = request.data.get("email")
            address = request.data.get("address")

            items = request.data.get("items", [])
            mode = request.data.get("mode")
            into_stock = request.data.get("into_stock", False)

            if not supplier_name:
                return Response({"error": "Supplier name is required"}, status=status.HTTP_400_BAD_REQUEST)

            subtotal = tax_total = gross_total = Decimal('0.00')

            # First create invoice (blank totals for now)
            invoice = PurchaseInvoice.objects.create(
                supplier_name=supplier_name,
                bill_no=bill_no,
                date=date,
                contact_number=contact_number,
                email=email,
                address=address,
                mode=mode,
                into_stock=into_stock
            )

            # Loop & create PurchaseItem (with invoice FK)
            for item in items:
                weight = to_decimal(item.get("weight"))
                rate = to_decimal(item.get("rate"))
                making = to_decimal(item.get("making"))
                tax_percentage = to_decimal(item.get("tax_percentage"))

                base = weight * rate
                net = base + making
                tax_amount = (net * tax_percentage) / 100
                total_amount = net + tax_amount

                subtotal += net
                tax_total += tax_amount
                gross_total += total_amount

                PurchaseItem.objects.create(
                    invoice=invoice,   # 👈 FOREIGN KEY ADDED
                    supplier_name=supplier_name,
                    hsn=item.get("hsn"),
                    segment=item.get("segment"),
                    item=item.get("item"),
                    pieces=item.get("pieces"),
                    weight=weight,
                    rate=rate,
                    making=making,
                    tax_percentage=tax_percentage,
                    base=base,
                    net=net,
                    tax_amount=tax_amount,
                    total_amount=total_amount,
                    hm=item.get("hm"),
                    comments=item.get("comments"),
                    status="A"
                )

            # Now calculate payments
            discount = to_decimal(request.data.get("discount"))
            advance = to_decimal(request.data.get("advance"))
            paid = to_decimal(request.data.get("paid"))

            net_payable = gross_total - discount - advance
            balance = net_payable - paid

            # Update invoice totals
            invoice.subtotal = subtotal
            invoice.tax_total = tax_total
            invoice.gross_total = gross_total
            invoice.discount = discount
            invoice.advance = advance
            invoice.net_payable = net_payable
            invoice.paid = paid
            invoice.balance = balance
            invoice.save()

            return Response({
                "message": "Invoice created successfully",
                "invoice": PurchaseInvoiceSerializer(invoice).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseInvoiceListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mode = request.query_params.get("mode")

        invoices = PurchaseInvoice.objects.all().order_by('-created_at')

        if mode:
            invoices = invoices.filter(mode=mode)

        serializer = PurchaseInvoiceSerializer(invoices, many=True)

        return Response({
            "count": invoices.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


######################################################################################################################

# views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from datetime import timedelta
# from django.utils import timezone
# from .models import ItemPayment, InstallmentEntry
# from .serializers import ItemPaymentSerializer

# class ItemPaymentCreateAPIView(APIView):
#     def post(self, request):
#         data = request.data.copy()

#         serializer = ItemPaymentSerializer(data=data)
#         if serializer.is_valid():
#             payment = serializer.save()

#             # --- Installment Logic ---
#             if payment.installment_type and payment.no_of_months and payment.start_date:
#                 total_amount = payment.balance_amount or payment.total_amount or 0
#                 per_installment = total_amount / payment.no_of_months
#                 date = payment.start_date

#                 for i in range(payment.no_of_months):
#                     if payment.installment_type == "daily":
#                         date += timedelta(days=1)
#                     elif payment.installment_type == "weekly":
#                         date += timedelta(weeks=1)
#                     elif payment.installment_type == "monthly":
#                         date += timedelta(days=30)
#                     elif payment.installment_type == "quarterly":
#                         date += timedelta(days=90)
#                     elif payment.installment_type == "yearly":
#                         date += timedelta(days=365)

#                     InstallmentEntry.objects.create(
#                         item_payment=payment,
#                         installment_date=date,
#                         amount=per_installment,
#                         installment_type=payment.installment_type,
#                         count=i + 1,
#                     )

#             response_data = ItemPaymentSerializer(payment).data
#             return Response({
#                 "message": "Item payment and installments created successfully.",
#                 "data": response_data
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from .models import ItemPayment, InstallmentEntry
from .serializers import ItemPaymentSerializer


class ItemPaymentCreateAPIView(APIView):
    def post(self, request):
        data = request.data.copy()

        serializer = ItemPaymentSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save ItemPayment first
        payment = serializer.save()

        # ---------------- INSTALLMENT LOGIC ----------------
        if (
            payment.installment_type
            and payment.no_of_months
            and payment.start_date
        ):
            # Use Decimal for financial safety
            total_amount = Decimal(
                payment.balance_amount or payment.total_amount or 0
            )
            months = int(payment.no_of_months)

            # Per-installment amount (rounded to 2 decimals)
            per_installment = (total_amount / Decimal(months)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            installment_date = payment.start_date
            total_created = Decimal("0.00")

            for i in range(months):
                # Increment date based on installment type
                if payment.installment_type == "daily":
                    installment_date += timedelta(days=1)
                elif payment.installment_type == "weekly":
                    installment_date += timedelta(weeks=1)
                elif payment.installment_type == "monthly":
                    installment_date += timedelta(days=30)
                elif payment.installment_type == "quarterly":
                    installment_date += timedelta(days=90)
                elif payment.installment_type == "yearly":
                    installment_date += timedelta(days=365)

                # Adjust LAST installment to avoid rounding mismatch
                if i == months - 1:
                    amount = total_amount - total_created
                else:
                    amount = per_installment
                    total_created += per_installment

                InstallmentEntry.objects.create(
                    item_payment=payment,
                    installment_date=installment_date,
                    amount=amount.quantize(Decimal("0.01")),
                    installment_type=payment.installment_type,
                    count=i + 1,
                )

        # ---------------- RESPONSE ----------------
        response_data = ItemPaymentSerializer(payment).data

        return Response(
            {
                "message": "Item payment and installments created successfully.",
                "data": response_data,
            },
            status=status.HTTP_201_CREATED,
        )

#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ItemPayment
from .serializers import ItemPaymentListSerializer,InstallmentEntrySerializer

class ItemPaymentListAPIView(APIView):
    """Get all item payments with installment info"""
    def get(self, request):
        payments = ItemPayment.objects.all().order_by('-id')
        serializer = ItemPaymentListSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InstallmentDetailAPIView(APIView):
    """Get all installment entries for a specific master (ItemPayment)"""
    def get(self, request, master_id):
        installments = InstallmentEntry.objects.filter(item_payment_id=master_id).order_by('installment_date')
        if not installments.exists():
            return Response(
                {"message": "No installments found for this master."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InstallmentEntrySerializer(installments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstallmentEntryListAPIView(APIView):
    """Get all installment entries with optional payment_status filter"""
    def get(self, request):
        payment_status = request.query_params.get('payment_status')
        installments = InstallmentEntry.objects.all().order_by('-installment_date')
        if payment_status in ['paid', 'unpaid']:
            installments = installments.filter(payment_status=payment_status)
        serializer = InstallmentEntrySerializer(installments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#################################################################################################################

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class CustomerPaymentSummaryAPIView(APIView):
    permission_classes = [AllowAny]

    """
    GET API — Customer payment summary with schema number and pay_status filter.
    Optional Query Param:
        - payment_status = paid | unpaid | all (default: all)
    """

    def get(self, request):
        # 🔹 Read filter from query params (default = all)
        filter_status = request.GET.get("payment_status", "all").lower()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    mip.id,
                    c.customer_id AS customer_id,
                    c.name AS customer_name,
                    c.contact_no AS mobile,
                    mip.id AS item_payment_id,
                    mip.total_amount AS total_amount,
                    mip.balance_amount AS balance_amount,
                    mip.status AS status,
                    mip.no_of_months AS no_of_months,
                    mip.start_date AS start_date,
                    mip.end_date AS end_date
                FROM master_itempayment mip
                LEFT JOIN master_saleitem msi ON (mip.sale_item_id = msi.id OR mip.sale_item_id = msi.saleitem_id)
                LEFT JOIN master_customer c ON msi.customer_id = c.customer_id
                GROUP BY mip.id, c.customer_id, c.name, c.contact_no, mip.id, 
                         mip.total_amount, mip.balance_amount, mip.status, 
                         mip.no_of_months, mip.start_date, mip.end_date
                ORDER BY mip.created_at DESC
            """)
            rows = cursor.fetchall()

        columns = [
            "id","customer_id", "name", "mobile", "item_payment_id",
            "amount", "balance_amount", "status",
            "no_of month", "start_date", "end_date"
        ]
        data = [dict(zip(columns, row)) for row in rows]

        if not data:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)

        filtered_data = []

        # 🧮 Add Schema No & Payment Status
        for record in data:
            record["schema_no"] = f"SCH-{record['id']}"

            item_payment_id = record["item_payment_id"]

            # Fetch payment statuses for this item_payment
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT payment_status 
                    FROM master_installmententry 
                    WHERE item_payment_id = %s
                """, [item_payment_id])
                statuses = [row[0] for row in cursor.fetchall()]

            if not statuses:
                pay_status = "unpaid"  # Default if no installment found
            elif any(status.lower() == "unpaid" for status in statuses):
                pay_status = "unpaid"
            else:
                pay_status = "paid"

            record["pay_status"] = pay_status
            record.pop("item_payment_id", None)

            # 🔹 Apply filter condition
            if filter_status == "all" or pay_status == filter_status:
                filtered_data.append(record)

        if not filtered_data:
            return Response({"message": f"No records found for payment_status='{filter_status}'"}, status=status.HTTP_404_NOT_FOUND)

        return Response(filtered_data, status=status.HTTP_200_OK)
#################################################################################################################


from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class InstallmentListByPaymentAPIView(APIView):
    permission_classes = [AllowAny]

    """
    GET API — List all installments for a given item_payment_id 
    with customer info and total calculations (total, paid, unpaid).
    """

    def get(self, request, item_payment_id):
        with connection.cursor() as cursor:
            # ✅ Fetch all installments with related customer details
            cursor.execute("""
                SELECT 
                    mie.id AS installment_id,
                    mie.installment_date,
                    mie.amount,
                    mie.installment_type,
                    mie.count AS installment_no,
                    mie.payment_status,
                    mie.status,
                    mip.start_date,
                    mip.no_of_months,
                    c.name AS customer_name,
                    c.contact_no AS contact_no,
                    msi.salesperson AS salesperson_name
                FROM master_installmententry mie
                JOIN master_itempayment mip ON mie.item_payment_id = mip.id
                JOIN master_saleitem msi ON mip.sale_item_id = msi.id
                JOIN master_customer c ON msi.customer_id = c.customer_id
                WHERE mie.item_payment_id = %s
                ORDER BY mie.installment_date ASC
            """, [item_payment_id])
            
            rows = cursor.fetchall()

        if not rows:
            return Response(
                {"message": "No installments found for this item_payment_id."},
                status=status.HTTP_404_NOT_FOUND
            )

        columns = [
            "installment_id", "installment_date", "amount", "installment_type",
            "installment_no", "payment_status", "status",
            "start_date", "no_of_months", "customer_name", "contact_no","salesperson_name"
        ]
        data = [dict(zip(columns, row)) for row in rows]

        # ✅ Calculate totals
        total_amount = sum(row["amount"] for row in data)
        total_paid_amount = sum(row["amount"] for row in data if row["payment_status"].lower() == "paid")
        total_unpaid_amount = sum(row["amount"] for row in data if row["payment_status"].lower() == "unpaid")

        # ✅ Prepare final response
        return Response({
            "item_payment_id": item_payment_id,
            "customer_name": data[0]["customer_name"],
            "salesperson_name": data[0]["salesperson_name"],
            "contact_no": data[0]["contact_no"],
            "start_date": data[0]["start_date"],
            "no_of_months": data[0]["no_of_months"],
            "totals": {
                "total_amount": total_amount,
                "total_paid_amount": total_paid_amount,
                "total_unpaid_amount": total_unpaid_amount
            },
            "installments": data
        }, status=status.HTTP_200_OK)


###################################################################################################

# views.py

from rest_framework.parsers import MultiPartParser, FormParser
from .models import InstallmentAttachment
from .serializers import InstallmentAttachmentSerializer

class InstallmentAttachmentCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    """
    POST API — Upload attachment for installment
    """

    def post(self, request):
        serializer = InstallmentAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Attachment uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # views.py

class InstallmentAttachmentListAPIView(APIView):
    permission_classes = [AllowAny]

    """
    GET API — Get all attachments for a specific installment
    """

    def get(self, request, installment_id):
        attachments = InstallmentAttachment.objects.filter(installment_id=installment_id)

        if not attachments.exists():
            return Response(
                {"message": "No attachments found for this installment"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InstallmentAttachmentSerializer(attachments, many=True)

        return Response({
            "installment_id": installment_id,
            "attachments": serializer.data
        }, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from .models import InstallmentEntry
from master.models import ItemPayment  # ✅ import your item payment model


class UpdateInstallmentStatusAPIView(APIView):
    permission_classes = [AllowAny]

    """
    PUT API — Update payment_status (e.g., unpaid → paid)
    for multiple installment IDs and update related ItemPayment balances.
    """

    def put(self, request):
        ids = request.data.get("ids", [])
        payment_status = request.data.get("payment_status", None)

        # ✅ Validate input
        if not ids or not isinstance(ids, list):
            return Response(
                {"error": "Please provide a list of 'ids'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if payment_status not in ["paid", "unpaid"]:
            return Response(
                {"error": "Invalid 'payment_status'. Must be 'paid' or 'unpaid'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Fetch installment entries
        installments = InstallmentEntry.objects.filter(id__in=ids)

        if not installments.exists():
            return Response(
                {"message": "No records found for provided IDs."},
                status=status.HTTP_404_NOT_FOUND
            )

        updated_ids = []
        with transaction.atomic():
            for installment in installments:
                # Only process if changing from unpaid → paid
                if installment.payment_status != payment_status:
                    # Update the installment status
                    installment.payment_status = payment_status
                    installment.save()

                    # ✅ Update related ItemPayment balance
                    if payment_status == "paid":
                        item_payment = ItemPayment.objects.filter(id=installment.item_payment_id).first()
                        if item_payment:
                            # Subtract from balance, add to paid
                            item_payment.paid_amount = (item_payment.paid_amount or 0) + installment.amount
                            item_payment.balance_amount = (item_payment.balance_amount or 0) - installment.amount
                            item_payment.save()

                    updated_ids.append(installment.id)

        return Response(
            {
                "message": f"Successfully updated {len(updated_ids)} installment(s).",
                "updated_status": payment_status,
                "updated_ids": updated_ids
            },
            status=status.HTTP_200_OK
        )


##################################################################################################################
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny
from .models import LoanPayment
from master.models import Loan  # 👈 make sure to import your Loan model correctly


class LoanPaymentCreateAPIView(APIView):
    permission_classes = [AllowAny]

    """
    POST API — Make a new loan payment.
    Fields: loan_id, amount, payment_method, loan_return_period_unit, period_value
    If payment marked as 'paid', it updates the loan status to 'complete'.
    """

    def post(self, request):
        loan_id = request.data.get("loan_id")
        amount = request.data.get("amount")
        payment_method = request.data.get("payment_method")
        loan_return_period_unit = request.data.get("loan_return_period_unit")
        period_value = request.data.get("period_value")
        payment_status = request.data.get("payment_status", "paid")  # default to paid

        # ✅ Validation
        if not loan_id or not amount:
            return Response(
                {"error": "loan_id and amount are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Create payment entry
            payment = LoanPayment.objects.create(
                loan_id=loan_id,
                payment_amount=amount,
                amount=amount,
                payment_method=payment_method,
                loan_return_period_unit=loan_return_period_unit,
                period_value=period_value,
                payment_date=timezone.now(),
                status=payment_status
            )

            # ✅ If paid — update master_loan status to 'complete'
            if payment_status.lower() == "paid":
                Loan.objects.filter(id=loan_id).update(status="Complete")

            return Response(
                {
                    "message": "Loan payment recorded successfully.",
                    "data": {
                        "id": payment.id,
                        "loan_id": payment.loan_id,
                        "amount": float(payment.payment_amount),
                        "payment_method": payment.payment_method,
                        "loan_return_period_unit": payment.loan_return_period_unit,
                        "period_value": payment.period_value,
                        "payment_date": payment.payment_date,
                        "status": payment.status,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Loan.DoesNotExist:
            return Response(
                {"error": f"Loan with ID {loan_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CraftsmanAttachment
from .serializers import CraftsmanAttachmentSerializer

class CraftsmanAttachmentUploadAPIView(APIView):
    permission_classes = [AllowAny]

    """
    POST API — Upload one or multiple attachments for a craftsman (jobwork_id).
    """

    def post(self, request):
        jobwork_id = request.data.get("jobwork_id")
        files = request.FILES.getlist("files")

        if not jobwork_id:
            return Response({"error": "jobwork_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not files:
            return Response({"error": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        attachments = []
        for file in files:
            attachment = CraftsmanAttachment.objects.create(jobwork_id=jobwork_id, file=file)
            attachments.append(attachment)

        serializer = CraftsmanAttachmentSerializer(attachments, many=True)
        return Response(
            {"message": "Attachments uploaded successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    
#################################################################################################################


class CraftsmanAttachmentListAPIView(APIView):
    permission_classes = [AllowAny]

    """
    GET API — Get all attachments for a given jobwork_id.
    """

    def get(self, request, jobwork_id):
        attachments = CraftsmanAttachment.objects.filter(jobwork_id=jobwork_id).order_by("-uploaded_at")
        serializer = CraftsmanAttachmentSerializer(attachments, many=True)
        return Response(
            {"jobwork_id": jobwork_id, "attachments": serializer.data},
            status=status.HTTP_200_OK
        )

#################################################################################################################


class SupplierAttachmentUploadAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        purchase_invoice_id = request.data.get("id")
        files = request.FILES.getlist("files")

        if not purchase_invoice_id:
            return Response({"error": "purchase_invoice_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not files:
            return Response({"error": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        attachments = []
        for file in files:
            attachment = SupplierAttachment.objects.create(purchase_invoice_id=purchase_invoice_id, file=file)
            attachments.append(attachment)

        serializer = SupplierAttachmentSerializer(attachments, many=True)
        return Response(
            {"message": "Attachments uploaded successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

class SupplierAttachmentListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, purchase_invoice_id):
        attachments = SupplierAttachment.objects.filter(purchase_invoice_id=purchase_invoice_id).order_by("-uploaded_at")
        serializer = SupplierAttachmentSerializer(attachments, many=True)
        return Response(
            {"id": purchase_invoice_id, "attachments": serializer.data},
            status=status.HTTP_200_OK
        )
########################################################################################################
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from master.models import JobWork  # assuming your table is master_jobwork

class JobWorkDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    """
    DELETE API — Deletes a JobWork record by ID
    """

    def delete(self, request, jobwork_id):
        try:
            jobwork = JobWork.objects.get(id=jobwork_id)
            jobwork.delete()
            return Response(
                {"message": f"JobWork record with ID {jobwork_id} deleted successfully."},
                status=status.HTTP_200_OK
            )
        except JobWork.DoesNotExist:
            return Response(
                {"error": f"No JobWork record found with ID {jobwork_id}."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from master.models import Loan


class LoanSoftDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    """
    PUT API — Soft delete a Loan record (set is_deleted=True)
    """

    def put(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id, is_deleted=False)
            loan.is_deleted = True
            loan.save(update_fields=["is_deleted"])
            
            return Response(
                {"message": f"Loan ID {loan_id} has been soft deleted successfully."},
                status=status.HTTP_200_OK
            )

        except Loan.DoesNotExist:
            return Response(
                {"error": f"Loan ID {loan_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


########################################################################################################################
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import URDAdjustment
from .serializers import URDAdjustmentSerializer


class URDAdjustmentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sale_item_id = request.query_params.get('sale_item_id')

        if not sale_item_id:
            return Response(
                {"error": "sale_item_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Fetch URD Adjustment linked to sale_item_id
            urd_adjustment = (
                URDAdjustment.objects
                .prefetch_related('urd_details')
                .get(sale_item_id=sale_item_id)
            )
        except URDAdjustment.DoesNotExist:
            return Response(
                {"error": "No URD Adjustment found for this sale_item_id"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Serialize main and related urd_details
        serializer = URDAdjustmentSerializer(urd_adjustment)
        return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################################################

from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from master.models import SaleItem  # update import as per your app

class SalesSummaryAPIView(generics.GenericAPIView):
    """
    GET /api/sales-summary/
    Optional Query Params:
        - date (YYYY-MM-DD): show sale of specific date
        - start_date & end_date: show combined sale between two dates
    Returns:
        today's sale, yesterday's sale, difference & percentage change
    """

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        date = request.query_params.get("date")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # --- Case 1: Specific Date ---
        if date:
            sale_total = SaleItem.objects.filter(date=date).aggregate(total=Sum("total_amount"))["total"] or 0
            return Response({
                "selected_date": date,
                "sale_value": round(sale_total, 2)
            })

        # --- Case 2: Date Range ---
        if start_date and end_date:
            sale_total = SaleItem.objects.filter(date__range=[start_date, end_date]).aggregate(total=Sum("total_amount"))["total"] or 0
            return Response({
                "start_date": start_date,
                "end_date": end_date,
                "combined_sale_value": round(sale_total, 2)
            })

        # --- Case 3: Today + Yesterday Comparison ---
        today_total = SaleItem.objects.filter(date=today).aggregate(total=Sum("total_amount"))["total"] or 0
        yesterday_total = SaleItem.objects.filter(date=yesterday).aggregate(total=Sum("total_amount"))["total"] or 0

        difference = today_total - yesterday_total
        percent_change = 0
        if yesterday_total > 0:
            percent_change = (difference / yesterday_total) * 100

        trend = "Increased" if difference > 0 else "Decreased" if difference < 0 else "No Change"

        return Response({
            "today_date": today,
            "today_sale": round(today_total, 2),
            "yesterday_sale": round(yesterday_total, 2),
            "difference": round(difference, 2),
            "percent_change": round(percent_change, 2),
            "trend": trend
        })

###############################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class ItemPaymentHistoryAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.id,
                    p.transaction_number,
                    p.transaction_method,
                    c.name AS customer_name,
                    DATE(p.created_at) AS date,
                    s.item_name AS items,
                    s.pieces AS number_of_items,         -- ✅ Added number of items
                    s.bill_type AS mode,                 -- ✅ Added mode (bill type)
                    p.paid_amount,
                    p.balance_amount
                FROM master_itempayment p
                LEFT JOIN master_saleitem s ON s.id = p.sale_item_id
                LEFT JOIN master_customer c ON s.customer_id = c.customer_id
                LEFT JOIN master_installmententry i ON i.item_payment_id = p.id
                ORDER BY p.created_at DESC
            """
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(data, status=status.HTTP_200_OK)


######################################################################################################################


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import connection

# class MetalRateAPIView(APIView):
#     def get(self, request):
#         metal_name = request.query_params.get("metal_type")
#         carat = request.query_params.get("purity")

#         if not metal_name or not carat:
#             return Response(
#                 {"error": "Please provide both 'metal_name' and 'carat' parameters."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with connection.cursor() as cursor:
#             query = """
#                 SELECT rate_per_gram
#                 FROM master_metalrate
#                 WHERE metal_name = %s AND carat = %s
#                 ORDER BY id DESC
#                 LIMIT 1
#             """
#             cursor.execute(query, [metal_name, carat])
#             result = cursor.fetchone()

#         if not result:
#             return Response(
#                 {"error": "No rate found for the given metal and carat."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         return Response(
#             {"metal_name": metal_name, "carat": carat, "rate_per_gram": result[0]},
#             status=status.HTTP_200_OK
#         )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import MetalRate
from .serializers import MetalRateSerializer

class MetalRateAPIView(APIView):
    def get(self, request):
        metal_name = request.query_params.get("metal_type")
        carat = request.query_params.get("purity")
        query_date = request.query_params.get("date")

        if not metal_name or not carat:
            return Response(
                {"error": "Please provide both 'metal_type' and 'purity' parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not query_date:
            query_date = timezone.now().date()

        try:
            rate_entry = MetalRate.objects.get(
                metal_name__iexact=metal_name,
                carat=carat,
                date=query_date
            )
            serializer = MetalRateSerializer(rate_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MetalRate.DoesNotExist:
            latest_rate = MetalRate.objects.filter(
                metal_name__iexact=metal_name,
                carat=carat
            ).order_by('-date').first()

            if latest_rate:
                serializer = MetalRateSerializer(latest_rate)
                return Response({
                    "message": "Rate not found for requested date. Returning latest available rate.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response(
                {"error": "No rate found for the given metal and carat."},
                status=status.HTTP_404_NOT_FOUND
            )
#################################################################################################################
# In your views.py file (add this to your existing views)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # Or IsAuthenticated, IsAdminUser etc.
from .models import SaleItem # Assuming SaleItem model is imported

# You don't need a serializer for deleting a single object typically
# Unless you want to return specific data about the deleted item,
# but a simple success message is usually enough for DELETE.

class SaleItemDeleteAPIView(generics.DestroyAPIView):
    queryset = SaleItem.objects.all()
    lookup_field = 'id' # Specifies that the URL will use 'id' to identify the SaleItem
    permission_classes = [AllowAny] # Adjust permissions as needed

    def delete(self, request, *args, **kwargs):
        instance = self.get_object() # Gets the SaleItem instance based on the URL 'id'
        
        # At this point, Django's CASCADE behavior (from your models)
        # will automatically delete related UrDAdjustment and UrDDetails.
        
        self.perform_destroy(instance) # Performs the actual deletion

        return Response(
            {"message": f"SaleItem {kwargs['id']} and related records deleted successfully."},
            status=status.HTTP_204_NO_CONTENT # 204 No Content is standard for successful DELETE
        )

####################################################################################################################

# Bulk delete sale items
class BulkSaleItemDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ids = request.data.get('ids', [])
        salesperson = request.data.get('salesperson')
        
        if not ids:
            return Response({"error": "ids list is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = SaleItem.objects.filter(id__in=ids)
        if salesperson:
            queryset = queryset.filter(salesperson=salesperson)
        
        deleted_count, _ = queryset.delete()
        
        return Response({
            "message": f"Deleted {deleted_count} sale items successfully."
        }, status=status.HTTP_204_NO_CONTENT)

####################################################################################################################

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from .models import Order
from .serializers import DeleteOrderSerializer

class DeleteOrderAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = DeleteOrderSerializer
    
    def get_object(self):
        """Override to fetch the order by `order_id`."""
        order_id = self.kwargs['order_id']
        try:
            return Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found", code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """Custom delete to return a custom response message."""
        order = self.get_object()
        order.delete()  # This will delete the order and associated OrderItems automatically due to `on_delete=models.CASCADE`
        return Response(
            {"message": f"Order {order.order_id} and its items deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


#################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, LoanPayment
from rest_framework.permissions import AllowAny

class LoanDeleteAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust permissions as needed
    
    def delete(self, request, loan_id):
        try:
            # Retrieve the Loan object based on the provided loan_id
            loan = Loan.objects.get(id=loan_id)

            # Check if loan exists
            if loan:
                # Delete all LoanPayments associated with the Loan (cascade delete happens here)
                loan.payments.all().delete()
                # Delete the Loan itself
                loan.delete()

                return Response(
                    {"detail": f"Loan and its payments with loan_id {loan_id} have been deleted."},
                    status=status.HTTP_204_NO_CONTENT
                )
        except Loan.DoesNotExist:
            return Response(
                {"detail": f"Loan with loan_id {loan_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


##################################################################################################################


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import DiamondBilling
# from rest_framework.permissions import AllowAny

# class DiamondBillingDeleteAPIView(APIView):
#     permission_classes = [AllowAny]  # Adjust permissions as needed
    
#     def delete(self, request, billing_id):
#         try:
#             # Retrieve the DiamondBilling object based on the provided billing_id
#             billing = DiamondBilling.objects.get(id=billing_id)

#             # If billing exists, delete the associated DiamondDetails and DiamondMetalInfo (cascades)
#             billing.delete()

#             return Response(
#                 {"detail": f"Diamond Billing and its associated records with billing_id {billing_id} have been deleted."},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#         except DiamondBilling.DoesNotExist:
#             return Response(
#                 {"detail": f"Diamond Billing with billing_id {billing_id} does not exist."},
#                 status=status.HTTP_404_NOT_FOUND
#             )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import DiamondBilling


class DiamondBillingDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, billing_id):
        try:
            # Get billing using correct primary key name
            billing = DiamondBilling.objects.get(billing_id=billing_id)

            # This will automatically delete DiamondDetail + DiamondMetalInfo because of CASCADE
            billing.delete()

            return Response(
                {
                    "message": f"Diamond billing {billing_id} and all related items deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except DiamondBilling.DoesNotExist:
            return Response(
                {"error": f"No billing found with billing_id {billing_id}"},
                status=status.HTTP_404_NOT_FOUND
            )


#####################################################################################################################


from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Notification.objects.all().order_by('-created_at')


#########################################################################################################


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, LoanPayment
from .serializers import LoanPaymentdetailsSerializer

class LoanPaymentDetailsAPIView(APIView):
    def get(self, request):
        loan_id = request.query_params.get('loan_id')
        if not loan_id:
            return Response({"error": "loan_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch payments under this loan_id
        payments = LoanPayment.objects.filter(loan_id=loan_id)
        serialized_payments = LoanPaymentdetailsSerializer(payments, many=True).data

        # Prepare API response retrieving data directly from DB
        return Response({
            "loan_id": loan.id,
            "loan_number": loan.loan_number,
            "loan_date": loan.loan_date,
            "adjusted_loan_amount": loan.adjusted_loan_amount,
            "paid_amount": loan.paid_amount,           # Taken directly from DB
            "balance_amount": loan.balance_amount,     # Taken directly from DB
            "payments": serialized_payments
        }, status=status.HTTP_200_OK)


###############################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import PurchaseItem

class PurchaseItemDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            item = PurchaseItem.objects.get(pk=pk)
        except PurchaseItem.DoesNotExist:
            return Response(
                {"message": "Purchase item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response(
            {"message": "Purchase item deleted successfully"},
            status=status.HTTP_200_OK
        )


####################################################################################################################

from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PurchaseInvoice, PurchaseItem
from .serializers import PurchaseItemDetailSerializer


class PurchaseInvoiceDetailAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        invoice_id = request.query_params.get("invoice_id")

        if not invoice_id:
            return Response(
                {"status": False, "message": "invoice_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch invoice
        invoice = get_object_or_404(PurchaseInvoice, id=invoice_id)

        # Fetch related items (via FK)
        items = PurchaseItem.objects.filter(invoice=invoice)

        # Calculate CGST + SGST split
        tax_total = invoice.tax_total or 0
        cgst = tax_total / 2
        sgst = tax_total / 2

        response = {
            "status": True,
            "message": "Invoice details fetched successfully",

            # SUPPLIER DETAILS
            "supplier_details": {
                "supplier_name": invoice.supplier_name,
                "contact_number": invoice.contact_number,
                "email": invoice.email,
                "address": invoice.address,
            },

            # INVOICE DETAILS
            "invoice_details": {
                "invoice_id": invoice.id,
                "bill_no": invoice.bill_no,
                "date": invoice.date,
                "subtotal": invoice.subtotal,
                "tax_total": invoice.tax_total,
                "cgst": cgst,
                "sgst": sgst,
                "gross_total": invoice.gross_total,
                "discount": invoice.discount,
                "advance": invoice.advance,
                "net_payable": invoice.net_payable,
                "paid": invoice.paid,
                "balance": invoice.balance,
                "mode": invoice.mode,
                "into_stock": invoice.into_stock,
                "created_at": invoice.created_at,
            },

            # ALL PURCHASE ITEMS
            "items": PurchaseItemDetailSerializer(items, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)
    

################################################################################################################################

# from rest_framework import status, generics
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import SaleItem, Customer


# class SaleInvoiceDetailAPIView(generics.GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         sale_item_id = request.query_params.get("sale_id")

#         if not sale_item_id:
#             return Response(
#                 {"status": False, "message": "sale_id is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Fetch SaleItem
#         sale = get_object_or_404(SaleItem, id=sale_item_id)

#         # Fetch Customer USING customer_id (not id)
#         customer = get_object_or_404(Customer, customer_id=sale.customer_id)

#         # Calculate CGST + SGST
#         total_tax = sale.total_tax or 0
#         cgst = total_tax / 2
#         sgst = total_tax / 2

#         response = {
#             "status": True,
#             "message": "Sale invoice fetched successfully",

#             "customer_details": {
#                 "customer_id": customer.customer_id,
#                 "name": customer.name,
#                 "contact_no": customer.contact_no,
#                 "email": customer.email,
#                 "pan_number": customer.pan_number,
#                 "adhar_no": customer.adhar_no,
#                 "gst_in": customer.gst_in,
#                 "bank_name": customer.bank_name,
#                 "address": customer.address,
#                 "upload_document": customer.upload_document.url if customer.upload_document else None,
#                 "created_at": customer.created_at,
#             },

#             "sale_details": {
#                 "id": sale.id,
#                 "date": sale.date,
#                 "salesperson": sale.salesperson,
#                 "qr_barcode_id": sale.qr_barcode_id,
#                 "huid_number": sale.huid_number,
#                 "metal": sale.metal,
#                 "item_name": sale.item_name,
#                 "purity": sale.purity,
#                 "pieces": sale.pieces,
#                 "gross_weight": sale.gross_weight,
#                 "less_weight": sale.less_weight,
#                 "net_weight": sale.net_weight,
#                 "rate_per_gram": sale.rate_per_gram,
#                 "making_type": sale.making_type,
#                 "making_charge": sale.making_charge,
#                 "stone_charges": sale.stone_charges,
#                 "hallmark_charges": sale.hallmark_charges,
#                 "hm_tax_percent": sale.hm_tax_percent,
#                 "gst_percent": sale.gst_percent,
#                 "comments": sale.comments,

#                 "base_metal_cost": sale.base_metal_cost,
#                 "making_cost": sale.making_cost,
#                 "total_tax": sale.total_tax,
#                 "cgst": cgst,
#                 "sgst": sgst,
#                 "total_amount": sale.total_amount,

#                 "bill_type": sale.bill_type,
#                 "created_at": sale.created_at,
#             }
#         }

#         return Response(response, status=status.HTTP_200_OK)


# from rest_framework import status, generics
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

# from .models import SaleItem, Customer
# from master.models import URDAdjustment, URDDetail


# class SaleInvoiceDetailAPIView(generics.GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         sale_item_id = request.query_params.get("sale_id")

#         if not sale_item_id:
#             return Response(
#                 {"status": False, "message": "sale_id is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ---------- Fetch Sale Item ----------
#         sale = get_object_or_404(SaleItem, id=sale_item_id)

#         # ---------- Fetch Customer ----------
#         customer = get_object_or_404(Customer, customer_id=sale.customer_id)

#         # ---------- Tax Split ----------
#         total_tax = sale.total_tax or 0
#         cgst = total_tax / 2
#         sgst = total_tax / 2

#         # ---------- URD DATA ----------
#         urd_adjustment = (
#             URDAdjustment.objects
#             .filter(sale_item_id=sale.id)
#             .values_list("adjust_amount", flat=True)
#             .first()
#         )

#         urd_final_amount = (
#             URDDetail.objects
#             .filter(sale_item_id=sale.id)
#             .values_list("final_amount", flat=True)
#             .first()
#         )

#         # ---------- RESPONSE ----------
#         response = {
#             "status": True,
#             "message": "Sale invoice fetched successfully",

#             "customer_details": {
#                 "customer_id": customer.customer_id,
#                 "name": customer.name,
#                 "contact_no": customer.contact_no,
#                 "email": customer.email,
#                 "pan_number": customer.pan_number,
#                 "adhar_no": customer.adhar_no,
#                 "gst_in": customer.gst_in,
#                 "bank_name": customer.bank_name,
#                 "address": customer.address,
#                 "upload_document": customer.upload_document.url if customer.upload_document else None,
#                 "created_at": customer.created_at,
#             },

#             "sale_details": {
#                 "id": sale.id,
#                 "date": sale.date,
#                 "salesperson": sale.salesperson,
#                 "qr_barcode_id": sale.qr_barcode_id,
#                 "huid_number": sale.huid_number,
#                 "metal": sale.metal,
#                 "item_name": sale.item_name,
#                 "purity": sale.purity,
#                 "pieces": sale.pieces,
#                 "gross_weight": sale.gross_weight,
#                 "less_weight": sale.less_weight,
#                 "net_weight": sale.net_weight,
#                 "rate_per_gram": sale.rate_per_gram,
#                 "making_type": sale.making_type,
#                 "making_charge": sale.making_charge,
#                 "stone_charges": sale.stone_charges,
#                 "hallmark_charges": sale.hallmark_charges,
#                 "hm_tax_percent": sale.hm_tax_percent,
#                 "gst_percent": sale.gst_percent,
#                 "comments": sale.comments,

#                 "base_metal_cost": sale.base_metal_cost,
#                 "making_cost": sale.making_cost,
#                 "total_tax": sale.total_tax,
#                 "cgst": cgst,
#                 "sgst": sgst,
#                 "total_amount": sale.total_amount,

#                 "bill_type": sale.bill_type,
#                 "created_at": sale.created_at,
#             },

#             # ✅ NEW SECTION
#             "urd_details": {
#                 "adjust_amount": urd_adjustment or 0,
#                 "urd_final_amount": urd_final_amount or 0
#             }
#         }

#         return Response(response, status=status.HTTP_200_OK)


from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SaleItem, Customer, ItemPayment, InstallmentEntry
from master.models import URDAdjustment, URDDetail


class SaleInvoiceDetailAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        sale_item_id = request.query_params.get("sale_id")

        if not sale_item_id:
            return Response(
                {"status": False, "message": "sale_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------- Fetch Sale Item ----------
        sale = get_object_or_404(SaleItem, id=sale_item_id)

        # ---------- Fetch Customer ----------
        customer = get_object_or_404(Customer, customer_id=sale.customer_id)

        # ---------- Tax Split ----------
        total_tax = sale.total_tax or 0
        cgst = total_tax / 2
        sgst = total_tax / 2

        # ---------- URD DATA ----------
        urd_adjustment = (
            URDAdjustment.objects
            .filter(sale_item_id=sale.id)
            .values_list("adjust_amount", flat=True)
            .first()
        )

        urd_final_amount = (
            URDDetail.objects
            .filter(sale_item_id=sale.id)
            .values_list("final_amount", flat=True)
            .first()
        )

        # ---------- PAYMENT + INSTALLMENT DATA ----------
        payments_data = []

        item_payments = ItemPayment.objects.filter(sale_item_id=sale.id)

        for payment in item_payments:
            installments = InstallmentEntry.objects.filter(
                item_payment_id=payment.id
            ).values(
                "id",
                "installment_date",
                "amount",
                "installment_type",
                "count",
                "payment_status",
                "status"
            )

            payments_data.append({
                "item_payment_id": payment.id,
                "item_name": payment.item_name,
                "metal_type": payment.metal_type,
                "purity": payment.purity,
                "final_weight": payment.final_weight,
                "total_amount": payment.total_amount,
                "sub_total": payment.sub_total,
                "cgst": payment.cgst,
                "hsn_tax": payment.hsn_tax,
                "discount": payment.discount,
                "grand_before_pay": payment.grand_before_pay,
                "paid_amount": payment.paid_amount,
                "balance_amount": payment.balance_amount,
                "transaction_method": payment.transaction_method,
                "transaction_number": payment.transaction_number,
                "comments": payment.comments,
                "installment_type": payment.installment_type,
                "no_of_months": payment.no_of_months,
                "start_date": payment.start_date,
                "end_date": payment.end_date,
                "installment_amount": payment.installment_amount,
                "status": payment.status,
                "created_at": payment.created_at,

                "installments": list(installments)
            })

        # ---------- RESPONSE ----------
        response = {
            "status": True,
            "message": "Sale invoice fetched successfully",

            "customer_details": {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "contact_no": customer.contact_no,
                "email": customer.email,
                "pan_number": customer.pan_number,
                "adhar_no": customer.adhar_no,
                "gst_in": customer.gst_in,
                "bank_name": customer.bank_name,
                "address": customer.address,
                "upload_document": customer.upload_document.url if customer.upload_document else None,
                "created_at": customer.created_at,
            },

            "sale_details": {
                "id": sale.id,
                "date": sale.date,
                "salesperson": sale.salesperson,
                "qr_barcode_id": sale.qr_barcode_id,
                "huid_number": sale.huid_number,
                "metal": sale.metal,
                "item_name": sale.item_name,
                "purity": sale.purity,
                "pieces": sale.pieces,
                "gross_weight": sale.gross_weight,
                "less_weight": sale.less_weight,
                "net_weight": sale.net_weight,
                "rate_per_gram": sale.rate_per_gram,
                "making_type": sale.making_type,
                "making_charge": sale.making_charge,
                "stone_charges": sale.stone_charges,
                "hallmark_charges": sale.hallmark_charges,
                "hm_tax_percent": sale.hm_tax_percent,
                "gst_percent": sale.gst_percent,
                "comments": sale.comments,

                "base_metal_cost": sale.base_metal_cost,
                "making_cost": sale.making_cost,
                "total_tax": sale.total_tax,
                "cgst": cgst,
                "sgst": sgst,
                "total_amount": sale.total_amount,

                "bill_type": sale.bill_type,
                "created_at": sale.created_at,
            },

            "urd_details": {
                "adjust_amount": urd_adjustment or 0,
                "urd_final_amount": urd_final_amount or 0
            },

            # ✅ NEW SECTION
            "payment_details": payments_data
        }

        return Response(response, status=status.HTTP_200_OK)

##########################################################################################################

class SaleInvoiceBatchDetailAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        saleitem_id = request.query_params.get("saleitem_id")

        if not saleitem_id:
            return Response(
                {"status": False, "message": "saleitem_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            saleitem_id = int(saleitem_id)
        except (TypeError, ValueError):
            return Response(
                {"status": False, "message": "saleitem_id must be an integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        sale_items = SaleItem.objects.filter(saleitem_id=saleitem_id)
        if not sale_items.exists():
            return Response(
                {"status": False, "message": "No sale items found for this saleitem_id"},
                status=status.HTTP_404_NOT_FOUND
            )

        first_sale = sale_items.first()
        customer = get_object_or_404(Customer, customer_id=first_sale.customer_id)

        batch_items = []
        for sale in sale_items:
            total_tax = sale.total_tax or 0
            cgst = total_tax / 2
            sgst = total_tax / 2

            urd_adjustment = (
                URDAdjustment.objects
                .filter(sale_item_id=sale.saleitem_id)
                .values_list("adjust_amount", flat=True)
                .first()
            )

            urd_final_amount = (
                URDDetail.objects
                .filter(sale_item_id=sale.saleitem_id)
                .values_list("final_amount", flat=True)
                .first()
            )

            payments_data = []
            item_payments = ItemPayment.objects.filter(sale_item_id=sale.saleitem_id)

            for payment in item_payments:
                installments = InstallmentEntry.objects.filter(
                    item_payment_id=payment.id
                ).values(
                    "id",
                    "installment_date",
                    "amount",
                    "installment_type",
                    "count",
                    "payment_status",
                    "status"
                )

                payments_data.append({
                    "item_payment_id": payment.id,
                    "item_name": payment.item_name,
                    "metal_type": payment.metal_type,
                    "purity": payment.purity,
                    "final_weight": payment.final_weight,
                    "total_amount": payment.total_amount,
                    "sub_total": payment.sub_total,
                    "cgst": payment.cgst,
                    "hsn_tax": payment.hsn_tax,
                    "discount": payment.discount,
                    "grand_before_pay": payment.grand_before_pay,
                    "paid_amount": payment.paid_amount,
                    "balance_amount": payment.balance_amount,
                    "transaction_method": payment.transaction_method,
                    "transaction_number": payment.transaction_number,
                    "comments": payment.comments,
                    "installment_type": payment.installment_type,
                    "no_of_months": payment.no_of_months,
                    "start_date": payment.start_date,
                    "end_date": payment.end_date,
                    "installment_amount": payment.installment_amount,
                    "status": payment.status,
                    "created_at": payment.created_at,
                    "urd_exchange_amount": payment.urd_exchange_amount,
                    "installments": list(installments)
                })

            batch_items.append({
                "sale_id": sale.id,
                "sale_details": {
                    "id": sale.id,
                    "saleitem_id": sale.saleitem_id,
                    "date": sale.date,
                    "salesperson": sale.salesperson,
                    "qr_barcode_id": sale.qr_barcode_id,
                    "huid_number": sale.huid_number,
                    "metal": sale.metal,
                    "item_name": sale.item_name,
                    "purity": sale.purity,
                    "pieces": sale.pieces,
                    "gross_weight": sale.gross_weight,
                    "less_weight": sale.less_weight,
                    "net_weight": sale.net_weight,
                    "rate_per_gram": sale.rate_per_gram,
                    "making_type": sale.making_type,
                    "making_charge": sale.making_charge,
                    "stone_charges": sale.stone_charges,
                    "hallmark_charges": sale.hallmark_charges,
                    "hm_tax_percent": sale.hm_tax_percent,
                    "gst_percent": sale.gst_percent,
                    "comments": sale.comments,
                    "base_metal_cost": sale.base_metal_cost,
                    "making_cost": sale.making_cost,
                    "total_tax": sale.total_tax,
                    "cgst": cgst,
                    "sgst": sgst,
                    "total_amount": sale.total_amount,
                    "bill_type": sale.bill_type,
                    "created_at": sale.created_at,
                },
                "urd_details": {
                    "adjust_amount": urd_adjustment or 0,
                    "urd_final_amount": urd_final_amount or 0
                },
                "payment_details": payments_data
            })

        response = {
            "status": True,
            "message": "Sale invoice batch fetched successfully",
            "saleitem_id": saleitem_id,
            "customer_details": {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "contact_no": customer.contact_no,
                "email": customer.email,
                "pan_number": customer.pan_number,
                "adhar_no": customer.adhar_no,
                "gst_in": customer.gst_in,
                "bank_name": customer.bank_name,
                "address": customer.address,
                "upload_document": customer.upload_document.url if customer.upload_document else None,
                "created_at": customer.created_at,
            },
            "sale_items": batch_items,
            "sale_count": len(batch_items)
        }

        return Response(response, status=status.HTTP_200_OK)

########################################################################################################################



from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class TotalStockAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT metal_type, SUM(gross_weight) AS total_gross_weight
                FROM master_jewelry
                GROUP BY metal_type;
            """)
            result = cursor.fetchall()

        data = [
            {
                "metal_type": row[0],
                "total_gross_weight": float(row[1])
            }
            for row in result
        ]

        return Response({"status": True, "total_stock": data})



############################################################################################################

import requests
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class InventoryValueAPIView(APIView):

    def get_live_rate_per_gram(self, metal_code):
        """Fetch live metal price per gram (GoldAPI gives per ounce)"""
        API_KEY = "goldapi-1dtsmi7duqiu-io"

        headers = {
            "x-access-token": API_KEY,
            "Content-Type": "application/json"
        }

        url = f"https://www.goldapi.io/api/{metal_code}/INR"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            price_per_ounce = float(data.get("price", 0))

            # Convert ounce → gram
            price_per_gram = price_per_ounce / 31.1034768
            return price_per_gram

        return 0

    def get(self, request):

        # 1️⃣ Live metal rates PER GRAM
        gold_rate = self.get_live_rate_per_gram("XAU")
        silver_rate = self.get_live_rate_per_gram("XAG")
        platinum_rate = self.get_live_rate_per_gram("XPT")

        # 2️⃣ Fetch total gross_weight grouped by metal
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT metal_type, SUM(gross_weight)
                FROM master_jewelry
                GROUP BY metal_type
            """)
            rows = cursor.fetchall()

        stock_data = []
        total_inventory_value = 0

        # 3️⃣ Calculate total value per metal
        for metal_type, total_weight in rows:

            metal_type_upper = metal_type.upper().strip()

            if metal_type_upper == "GOLD":
                live_rate = gold_rate
            elif metal_type_upper == "SILVER":
                live_rate = silver_rate
            elif metal_type_upper == "PLATINUM":
                live_rate = platinum_rate
            else:
                live_rate = 0

            # NOTE: total_weight is already in GRAMS
            metal_value = float(total_weight) * live_rate
            total_inventory_value += metal_value

            stock_data.append({
                "metal_type": metal_type,
                "total_gross_weight_grams": float(total_weight),
                "live_rate_in_inr_per_gram": live_rate,
                "total_value_in_inr": metal_value
            })

        return Response({
            "status": True,
            "live_rates_per_gram": {
                "gold_inr_per_gram": gold_rate,
                "silver_inr_per_gram": silver_rate,
                "platinum_inr_per_gram": platinum_rate,
            },
            "inventory_stock": stock_data,
            "grand_total_inventory_value": total_inventory_value
        })


###############################################################################################################################

#New Bhishi Requirement
# views.py

from rest_framework.parsers import MultiPartParser, FormParser
from .models import BhishiAttachment, Bhishi
from .serializers import BhishiAttachmentSerializer

class BhishiAttachmentUploadAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        bhishi_id = request.data.get('bhishi')

        # Validate Bhishi
        if not Bhishi.objects.filter(id=bhishi_id).exists():
            return Response({"error": "Invalid Bhishi ID"}, status=400)

        serializer = BhishiAttachmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Attachment uploaded successfully",
                "data": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)
    
class BhishiAttachmentListAPI(APIView):

    def get(self, request):
        bhishi_id = request.query_params.get('bhishi_id')

        if not bhishi_id:
            return Response({"error": "bhishi_id is required"}, status=400)

        attachments = BhishiAttachment.objects.filter(bhishi_id=bhishi_id)

        serializer = BhishiAttachmentSerializer(attachments, many=True)

        return Response({
            "bhishi_id": bhishi_id,
            "attachments": serializer.data
        }, status=200)
    

class BhishiCreateAPI(APIView):
    def post(self, request):
        serializer = BhishiCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BhishiGetUpdateAPI(APIView):

    def get(self, request, pk):
        try:
            obj = Bhishi.objects.get(pk=pk)
        except Bhishi.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = BhishiGetUpdateSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            obj = Bhishi.objects.get(pk=pk)
        except Bhishi.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = BhishiGetUpdateSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# class BhishiPaymentAPI(APIView):

#     def post(self, request):
#         serializer = BhishiPaymentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class BhishiPaymentAPI(APIView):

    def post(self, request):
        try:
            bhishi = request.data.get("bhishi")
            payment_amount = request.data.get("payment_amount")
            payment_method = request.data.get("payment_method")
            payment_date = request.data.get("payment_date")

            # Validate Bhishi
            if not Bhishi.objects.filter(id=bhishi).exists():
                return Response(
                    {"status": False, "message": "Invalid Bhishi ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bhishi_obj = Bhishi.objects.get(id=bhishi)

            # Create payment
            payment = BhishiPayment.objects.create(
                bhishi=bhishi_obj,
                payment_amount=payment_amount,
                payment_method=payment_method,
                payment_date=payment_date
            )

            # Update Bhishi amounts
            bhishi_obj.paid_amount += Decimal(payment_amount)
            bhishi_obj.save()

            return Response(
                {
                    "status": True,
                    "message": "Bhishi payment recorded successfully",
                    "data": {
                        "payment_id": payment.id,
                        "bhishi": bhishi_obj.id,
                        "customer": bhishi_obj.customer.customer_id,
                        "payment_amount": float(payment.payment_amount),
                        "payment_method": payment.payment_method,
                        "payment_date": str(payment.payment_date),
                        "updated_balance": float(bhishi_obj.balance_amount)
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=400)

##################################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Bhishi
from .serializers import BhishiGetUpdateSerializer
from django.core.paginator import Paginator, EmptyPage

class BhishiListAPI(APIView):
    def get(self, request):
        qs = Bhishi.objects.filter(is_deleted=False)

        customer_id = request.query_params.get('customer_id')
        status = request.query_params.get('status')
        date_from = request.query_params.get('date_from')  # YYYY-MM-DD
        date_to = request.query_params.get('date_to')
        min_balance = request.query_params.get('min_balance')
        max_balance = request.query_params.get('max_balance')
        search = request.query_params.get('search')

        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        if status:
            qs = qs.filter(status__iexact=status)
        if date_from:
            qs = qs.filter(bhishi_date__gte=date_from)
        if date_to:
            qs = qs.filter(bhishi_date__lte=date_to)
        if min_balance:
            qs = qs.filter(balance_amount__gte=min_balance)
        if max_balance:
            qs = qs.filter(balance_amount__lte=max_balance)
        if search:
            qs = qs.filter(
                Q(bhishi_number__icontains=search) |
                Q(bhishi_type__icontains=search) |
                Q(customer__name__icontains=search)
            )

        # Sorting
        order_by = request.query_params.get('order_by', '-created_at')
        qs = qs.order_by(order_by)

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 25))
        paginator = Paginator(qs, page_size)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return Response({"results": [], "count": paginator.count})

        serializer = BhishiGetUpdateSerializer(page_obj.object_list, many=True)
        return Response({
            "results": serializer.data,
            "count": paginator.count,
            "page": page,
            "page_size": page_size,
            "num_pages": paginator.num_pages
        })


#################################################################################################################

from .models import BhishiPayment
from .serializers import BhishiPaymentSerializer

class BhishiPaymentHistoryAPI(APIView):
    def get(self, request):
        bhishi_id = request.query_params.get('bhishi_id')
        if not bhishi_id:
            return Response({"error": "bhishi_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        qs = BhishiPayment.objects.filter(bhishi_id=bhishi_id).order_by('-payment_date')

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(payment_date__gte=date_from)
        if date_to:
            qs = qs.filter(payment_date__lte=date_to)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 25))
        paginator = Paginator(qs, page_size)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return Response({"results": [], "count": paginator.count})

        serializer = BhishiPaymentSerializer(page_obj.object_list, many=True)
        return Response({
            "results": serializer.data,
            "count": paginator.count,
            "page": page,
            "page_size": page_size,
            "num_pages": paginator.num_pages
        })

###############################################################################################################

from django.db.models import Sum, Count, F
from decimal import Decimal

class BhishiDashboardAPI(APIView):
    def get(self, request):
        qs = Bhishi.objects.filter(is_deleted=False)

        total_bhishis = qs.count()
        total_collections = qs.aggregate(total_collected=Sum('paid_amount'))['total_collected'] or Decimal('0.00')
        total_pending_amount = qs.aggregate(total_pending=Sum('balance_amount'))['total_pending'] or Decimal('0.00')
        completed_count = qs.filter(status__iexact='Completed').count()
        active_count = qs.filter(status__iexact='Active').count()

        # Optionally group by month/year for recent activity
        # Add more metrics if needed

        return Response({
            "total_bhishis": total_bhishis,
            "total_collections": str(total_collections),
            "total_pending_amount": str(total_pending_amount),
            "completed_count": completed_count,
            "active_count": active_count
        })

##########################################################################################################################################

import io
from django.http import FileResponse, Http404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from datetime import datetime

class BhishiReportPDFView(APIView):
    def get(self, request, pk):
        bhishi = get_object_or_404(Bhishi, pk=pk, is_deleted=False)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Header
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, height - 50, f"Bhishi Report - {bhishi.bhishi_number}")
        p.setFont("Helvetica", 10)
        p.drawString(40, height - 70, f"Date: {bhishi.bhishi_date}")
        p.drawString(40, height - 85, f"Customer: {bhishi.customer.name if bhishi.customer else 'N/A'}")

        # Details
        y = height - 120
        p.drawString(40, y, f"Bhishi Type: {bhishi.bhishi_type or ''}")
        p.drawString(300, y, f"Total Amount: {bhishi.total_amount or 0}")
        y -= 20
        p.drawString(40, y, f"Per Installment: {bhishi.per_installment or 0}")
        p.drawString(300, y, f"Total Installments: {bhishi.total_installments or 0}")
        y -= 20
        p.drawString(40, y, f"Paid Amount: {bhishi.paid_amount or 0}")
        p.drawString(300, y, f"Balance Amount: {bhishi.balance_amount or 0}")
        y -= 30

        # Payments table header
        p.setFont("Helvetica-Bold", 10)
        p.drawString(40, y, "Payments:")
        y -= 15
        p.setFont("Helvetica", 9)
        p.drawString(40, y, "Date")
        p.drawString(150, y, "Amount")
        p.drawString(300, y, "Status")
        y -= 12

        payments = bhishi.payments.all().order_by('-payment_date')
        for pay in payments:
            if y < 60:
                p.showPage()
                y = height - 50
            p.drawString(40, y, str(pay.payment_date))
            p.drawString(150, y, str(pay.payment_amount))
            p.drawString(300, y, str(pay.status))
            y -= 15

        # Footer
        p.setFont("Helvetica-Oblique", 8)
        p.drawString(40, 30, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"bhishi_{bhishi.bhishi_number}.pdf")

###############################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Bhishi

class DeleteBhishiAPIView(APIView):

    def delete(self, request, bhishi_id):
        bhishi = get_object_or_404(Bhishi, id=bhishi_id)

        # Delete Bhishi (payments auto-deleted due to CASCADE)
        bhishi.delete()

        return Response(
            {"message": "Bhishi and all related payments deleted successfully"},
            status=status.HTTP_200_OK
        )

############################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Bhishi, BhishiPayment
from .serializers import BhishiPaymentDetailsSerializer


class BhishiPaymentDetailsAPIView(APIView):
    def get(self, request):
        bhishi_id = request.query_params.get('bhishi_id')
        if not bhishi_id:
            return Response({"error": "bhishi_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get main Bhishi record
        bhishi = get_object_or_404(Bhishi, id=bhishi_id)

        # Fetch all payments under this Bhishi
        payments = BhishiPayment.objects.filter(bhishi_id=bhishi_id)

        serialized_payments = BhishiPaymentDetailsSerializer(payments, many=True).data

        return Response({
            "bhishi_id": bhishi.id,
            "bhishi_number": bhishi.bhishi_number,      # if exists
            "bhishi_date": bhishi.bhishi_date,          # if exists
            "total_amount": bhishi.total_amount,
            "paid_amount": bhishi.paid_amount,          # Direct from DB
            "balance_amount": bhishi.balance_amount,    # Direct from DB
            "payments": serialized_payments
        }, status=status.HTTP_200_OK)

################################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import CraftsmanAttachment


class CraftsmanAttachmentDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, attachment_id):
        attachment = get_object_or_404(CraftsmanAttachment, id=attachment_id)

        # Delete file from storage first
        if attachment.file:
            attachment.file.delete(save=False)

        attachment.delete()

        return Response(
            {"message": "Craftsman attachment deleted successfully"},
            status=status.HTTP_200_OK
        )


###################################################################################################################

from .models import SupplierAttachment


class SupplierAttachmentDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, attachment_id):
        attachment = get_object_or_404(SupplierAttachment, id=attachment_id)

        # Delete file from storage
        if attachment.file:
            attachment.file.delete(save=False)

        attachment.delete()

        return Response(
            {"message": "Supplier attachment deleted successfully"},
            status=status.HTTP_200_OK
        )


######################################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import ItemPayment, Order, OrderAttachment
from .serializers import ItemPaymentDetailSerializer, OrderAttachmentSerializer


class ItemPaymentDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        item_payment_id = request.query_params.get("item_payment_id")

        if not item_payment_id:
            return Response(
                {"error": "item_payment_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item_payment = ItemPayment.objects.get(id=item_payment_id)
        except ItemPayment.DoesNotExist:
            return Response(
                {"error": "ItemPayment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemPaymentDetailSerializer(item_payment)

        return Response(
            {
                "message": "Item payment details fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

###################################################################################################


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import ItemPayment
from .serializers import ItemPaymentSerializer


class ItemPaymentGetAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        status_param = request.query_params.get("status")
        installment_type = request.query_params.get("installment_type")
        metal_type = request.query_params.get("metal_type")

        queryset = ItemPayment.objects.all().order_by("-created_at")

        # Optional filters
        if status_param:
            queryset = queryset.filter(status=status_param)

        if installment_type:
            queryset = queryset.filter(installment_type=installment_type)

        if metal_type:
            queryset = queryset.filter(metal_type=metal_type)

        serializer = ItemPaymentSerializer(queryset, many=True)

        return Response(
            {
                "message": "Item payment data fetched successfully",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

#####################################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class CustomerAllTransactionDetailAPIView(APIView):

    def get(self, request, customer_id):

        customer = get_object_or_404(Customer, customer_id=customer_id)

        bhishi_qs = Bhishi.objects.filter(customer_id=customer_id, is_deleted=False)
        diamond_qs = DiamondBilling.objects.filter(customer_id=customer_id)
        loan_qs = Loan.objects.filter(customer_id=customer_id, is_deleted=False)
        order_qs = Order.objects.filter(customer_id=customer_id)
        sale_item_qs = SaleItem.objects.filter(customer_id=customer_id)

        response_data = {
            "customer": CustomerSelfDetailSerializer(customer).data,
            "bhishi": CustomerBhishiDetailSerializer(bhishi_qs, many=True).data,
            "diamond_billing": CustomerDiamondBillingDetailSerializer(diamond_qs, many=True).data,
            "loans": CustomerLoanDetailSerializer(loan_qs, many=True).data,
            "orders": CustomerOrderDetailSerializer(order_qs, many=True).data,
            "sale_items": CustomerSaleItemDetailSerializer(sale_item_qs, many=True).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class OrderAttachmentUploadAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order_id = request.data.get("order_id")
        files = request.FILES.getlist("attachments") or request.FILES.getlist("attachment")
        single_file = request.FILES.get("attachment")

        if not order_id:
            return Response({"error": "order_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not files and single_file:
            files = [single_file]

        if not files:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        attachments = []
        for file in files:
            attachment = OrderAttachment.objects.create(order=order, file=file)
            attachments.append(attachment)

        serializer = OrderAttachmentSerializer(attachments, many=True, context={"request": request})

        return Response(
            {
                "message": "Order attachments uploaded successfully.",
                "order_id": order.order_id,
                "attachments": serializer.data
            },
            status=status.HTTP_200_OK
        )




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order
from .serializers import ItemPaymentSerializer, OrderAttachmentSerializer


class OrderAttachmentRetrieveAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order_id = request.GET.get("order_id")

        if not order_id:
            return Response(
                {"error": "order_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        attachments = order.attachments.all()
        serializer = OrderAttachmentSerializer(attachments, many=True, context={"request": request})

        return Response(
            {
                "order_id": order.order_id,
                "attachments": serializer.data,
                "salesperson_name": order.salesperson_name,
                "order_date": order.order_date,
                "grand_total": order.grand_total
            },
            status=status.HTTP_200_OK
        )
    