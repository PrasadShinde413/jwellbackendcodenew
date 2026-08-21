# sales_api/views.py
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SaleItemDetailRawSQL(APIView):
    def get(self, request, pk=None, format=None):
        query = """
            SELECT
                msi.id AS sale_item_master_id,
                msi.customer_id,
                c.name AS customer_name,
                c.address AS customer_address,
                c.contact_no AS customer_contact_no,
                sid.start_date,
                sid.end_date,
                sid.id,
                sid.no_of_months,
                sid.status,
                sid.total_amount,
                sid.paid_amount,
                sid.balance_amount
            FROM
                master_saleitem AS msi
            JOIN
                master_customer AS c ON msi.customer_id = c.customer_id
            JOIN
                master_itempayment AS sid ON msi.id = sid.sale_item_id
        """
        params = []

        if pk:
            query += " WHERE msi.id = %s"
            params.append(pk)
        
        # You can add ORDER BY here if needed, e.g., ORDER BY msi.id DESC

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            # Fetch all rows from the query result
            rows = cursor.fetchall()
            
            # Get column names from the cursor description
            columns = [col[0] for col in cursor.description]
            
            # Manually map rows to dictionaries for a clean JSON output
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))

        if not results and pk:
            return Response({"detail": "Sale item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(results, status=status.HTTP_200_OK)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import JobWork
from .serializers import MasterJobworkSerializer, TransactionHistorySerializer

class KaragirReportAPIView(generics.ListAPIView):
    """
    GET API — Fetch Karagir (Craftsman) Jobwork Report
    """
    queryset = JobWork.objects.all().order_by('-date')
    serializer_class = MasterJobworkSerializer
    permission_classes = [AllowAny]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from master.models import PurchaseInvoice  # adjust app name if different


class SupplierBalanceReportAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            invoices = PurchaseInvoice.objects.all().order_by('-date')

            data = []
            for inv in invoices:
                data.append({
                    "id": inv.id,
                    "supplier_name": inv.supplier_name,
                    "date": inv.date,
                    "address": inv.address,
                    "email": inv.email,
                    "contact_number": inv.contact_number,
                    "bill_no": inv.bill_no,
                    "advance": str(inv.advance),
                    "net_payable": str(inv.net_payable),
                    "paid": str(inv.paid),
                    "balance": str(inv.balance),
                })

            return Response({"supplier_balance_report": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from master.models import SaleItem, Customer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class SalesReportAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        sales = SaleItem.objects.all().order_by('-date')
        data = []

        for sale in sales:
            customer = Customer.objects.filter(customer_id=sale.customer_id).first()
            if customer:
                data.append({
                    "id": sale.id,
                    "date": sale.date,
                    "qr_barcode_id": sale.qr_barcode_id,
                    "huid_number": sale.huid_number,
                    "metal": sale.metal,
                    "item_name": sale.item_name,
                    "net_weight": sale.net_weight,
                    "making_charge": sale.making_charge,
                    "stone_charges": sale.stone_charges,
                    "hallmark_charges": sale.hallmark_charges,
                    "total_tax": sale.total_tax,
                    "base_metal_cost": sale.base_metal_cost,
                    "total_amount": sale.total_amount,
                    "comments": sale.comments,
                    # ✅ Customer details flattened
                    "customer_id": customer.customer_id,
                    "customer_name": customer.name,
                    "customer_contact_no": customer.contact_no,
                    "customer_email": customer.email,
                    "customer_address": customer.address,
                })

        return Response(data)



from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection


class TransactionHistoryAPIView(generics.ListAPIView):
    """
    GET /api/transaction-history/?item_payment_id=<id>
    → Returns customer details once and only 'paid' installment records
    """

    def get(self, request, *args, **kwargs):
        item_payment_id = request.query_params.get("item_payment_id")

        if not item_payment_id:
            return Response(
                {"error": "Please provide 'item_payment_id' as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        query = f"""
        SELECT
            mie.id AS installment_id,
            mie.installment_date,
            mie.amount,
            mie.installment_type,
            mie.count,
            mie.payment_status,
            mie.status,

            sid.id AS item_payment_id,
            sid.comments AS comments,
            sid.total_amount,
            sid.paid_amount,
            sid.balance_amount,
            sid.start_date AS purchase_date,
            sid.end_date AS due_date,
            sid.no_of_months,

            msi.id AS sale_item_id,
            msi.item_name,
            msi.customer_id,

            c.name AS customer_name,
            c.address AS customer_address,
            c.contact_no AS customer_contact_no

        FROM
            master_installmententry AS mie
        JOIN
            master_itempayment AS sid ON mie.item_payment_id = sid.id
        JOIN
            master_saleitem AS msi ON (sid.sale_item_id = msi.id OR sid.sale_item_id = msi.saleitem_id)
        JOIN
            master_customer AS c ON msi.customer_id = c.customer_id
        WHERE
            mie.item_payment_id = %s
            AND mie.payment_status = 'paid'
        ORDER BY
            mie.installment_date ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [item_payment_id])
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not rows:
            return Response(
                {"message": "No paid transactions found for this item_payment_id."},
                status=status.HTTP_404_NOT_FOUND
            )

        first = rows[0]
        installments = []

        for r in rows:
            installments.append({
                "installment_id": r["installment_id"],
                "installment_date": r["installment_date"],
                "amount": float(r["amount"]),
                "installment_type": r["installment_type"],
                "count": r["count"],
                "payment_status": r["payment_status"],
                "status": r["status"],
                "comments": r["comments"],
                "item_name": r["item_name"],
                "balance_amount": float(r["balance_amount"]),
            })

        response_data = {
            "customer_id": first["customer_id"],
            "customer_name": first["customer_name"],
            "customer_address": first["customer_address"],
            "customer_contact_no": first["customer_contact_no"],
            "purchase_date": str(first["purchase_date"]),
            "due_date": str(first["due_date"]),
            "total_amount": float(first["total_amount"]),
            "paid_amount": float(first["paid_amount"]),
            "balance_amount": float(first["balance_amount"]),
            "no_of_months": first["no_of_months"],
            "installments": installments
        }

        return Response(response_data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncQuarter
from datetime import datetime
from .models import ItemPayment  # your model

class GSTReportAPIView(APIView):
    """
    GET API — Returns GST report monthwise and quarterwise
    Aggregates CGST from master_itempayment table based on created_at
    """
    def get(self, request):
        try:
            # --- MONTHWISE REPORT ---
            monthwise_data = (
                ItemPayment.objects
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_cgst=Sum('cgst'))
                .order_by('month')
            )

            monthwise_report = [
                {
                    "month": data["month"].strftime("%B %Y"),  # e.g., "January 2025"
                    "total_cgst": float(data["total_cgst"] or 0)
                }
                for data in monthwise_data
            ]

            # --- QUARTERWISE REPORT ---
            quarterwise_data = (
                ItemPayment.objects
                .annotate(quarter=TruncQuarter('created_at'))
                .values('quarter')
                .annotate(total_cgst=Sum('cgst'))
                .order_by('quarter')
            )

            quarterwise_report = [
                {
                    "quarter": f"Q{((data['quarter'].month - 1)//3) + 1} {data['quarter'].year}",
                    "total_cgst": float(data["total_cgst"] or 0)
                }
                for data in quarterwise_data
            ]

            # --- OVERALL SUMMARY ---
            total_cgst = ItemPayment.objects.aggregate(total=Sum('cgst'))['total'] or 0
            start_date = ItemPayment.objects.order_by('created_at').first()
            end_date = ItemPayment.objects.order_by('-created_at').first()

            summary = {
                "from_date": start_date.created_at.strftime("%d-%m-%Y") if start_date else None,
                "to_date": end_date.created_at.strftime("%d-%m-%Y") if end_date else None,
                "total_cgst_collected": float(total_cgst)
            }

            return Response(
                {
                    "summary": summary,
                    "monthwise_report": monthwise_report,
                    "quarterwise_report": quarterwise_report
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###############################################################################################################################

from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection


class AllTransactionHistoryAPIView(generics.ListAPIView):
    """
    GET /api/all-transaction-history/
    → Returns all 'paid' installment records grouped by item_payment_id with customer details.
    """

    def get(self, request, *args, **kwargs):
        query = """
        SELECT
            mie.id AS installment_id,
            mie.installment_date,
            mie.amount,
            mie.installment_type,
            mie.count,
            mie.payment_status,
            mie.status,

            sid.id AS item_payment_id,
            sid.comments AS comments,
            sid.total_amount,
            sid.paid_amount,
            sid.balance_amount,
            sid.start_date AS purchase_date,
            sid.end_date AS due_date,
            sid.no_of_months,

            msi.id AS sale_item_id,
            msi.item_name,
            msi.customer_id,

            c.name AS customer_name,
            c.address AS customer_address,
            c.contact_no AS customer_contact_no

        FROM
            master_installmententry AS mie
        JOIN
            master_itempayment AS sid ON mie.item_payment_id = sid.id
        JOIN
            master_saleitem AS msi ON (sid.sale_item_id = msi.id OR sid.sale_item_id = msi.saleitem_id)
        JOIN
            master_customer AS c ON msi.customer_id = c.customer_id
        WHERE
            mie.payment_status = 'paid'
        ORDER BY
            mie.item_payment_id, mie.installment_date ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not rows:
            return Response(
                {"message": "No paid transactions found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Group data by item_payment_id
        grouped_data = {}
        for r in rows:
            item_payment_id = r["item_payment_id"]

            if item_payment_id not in grouped_data:
                grouped_data[item_payment_id] = {
                    "item_payment_id": item_payment_id,
                    "customer_id": r["customer_id"],
                    "customer_name": r["customer_name"],
                    "customer_address": r["customer_address"],
                    "customer_contact_no": r["customer_contact_no"],
                    "purchase_date": str(r["purchase_date"]),
                    "due_date": str(r["due_date"]),
                    "total_amount": float(r["total_amount"]),
                    "paid_amount": float(r["paid_amount"]),
                    "balance_amount": float(r["balance_amount"]),
                    "no_of_months": r["no_of_months"],
                    "item_name": r["item_name"],
                    "installments": []
                }

            grouped_data[item_payment_id]["installments"].append({
                "installment_id": r["installment_id"],
                "installment_date": r["installment_date"],
                "amount": float(r["amount"]),
                "installment_type": r["installment_type"],
                "count": r["count"],
                "payment_status": r["payment_status"],
                "status": r["status"],
                "comments": r["comments"],
            })

        return Response(list(grouped_data.values()), status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WhatsAppSendAPIView(APIView):

    def post(self, request):
        phone = request.data.get("phone")
        message = request.data.get("message", "")
        attachment = request.FILES.get("attachment")  # optional file

        if not phone:
            return Response({"error": "Phone number is required"}, status=400)

        # Add Sender Name
        sender_name = "Shree Gajanan Jewellers"
        full_message = f"{message}\n\nRegards,\n{sender_name}"

        # Encode message
        encoded_message = full_message.replace(" ", "%20").replace("\n", "%0A")

        # WhatsApp message URL
        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

        response_data = {
            "whatsapp_link": whatsapp_url,
            "sender": sender_name
        }

        # If a file is uploaded, save it and send URL
        if attachment:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"whatsapp/{attachment.name}", attachment)
            file_url = request.build_absolute_uri(default_storage.url(file_path))
            response_data["attachment_url"] = file_url

        return Response(response_data, status=status.HTTP_200_OK)
