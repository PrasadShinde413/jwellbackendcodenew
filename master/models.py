from django.db import models
from django.utils import timezone # Import timezone
from datetime import date # Import the date class from datetime module
import qrcode

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True,blank=True, null=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    adhar_no = models.CharField(max_length=20, blank=True, null=True)
    gst_in = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    upload_document = models.FileField(upload_to='customer_docs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Metal(models.Model):
    id = models.AutoField(primary_key=True)
    metal_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.metal_name


class Carat(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value} Carat"



# from django.db import models
# import qrcode
# from io import BytesIO
# from django.core.files import File
# from datetime import datetime

# class Jewelry(models.Model):
#     id = models.AutoField(primary_key=True)
#     date = models.DateField(default=datetime.now)
#     bname = models.CharField(max_length=100, blank=True, null=True)
#     bill_no = models.CharField(max_length=100, blank=True, null=True)
#     metal_type = models.CharField(max_length=100)
#     item_name = models.CharField(max_length=100)
#     purity = models.DecimalField(max_digits=5, decimal_places=2)
#     huid_number = models.CharField(max_length=100, blank=True, null=True)
#     pieces = models.IntegerField(default=1)
#     gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
#     less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
#     wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     wastage_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
#     rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
#     making_charge_type = models.CharField(max_length=50, choices=[("Per Gram", "Per Gram"), ("Fixed", "Fixed")])
#     making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     per_gram_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     stone_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     hallmark_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3)
#     comments = models.TextField(blank=True, null=True)
#     qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
#     qr_url = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.item_name} ({self.metal_type})"

#     def save(self, *args, **kwargs):
#         # Generate QR Code
#         qr_content = f"Jewelry ID: {self.id}, Metal: {self.metal_type}, Purity: {self.purity}, Gross Weight: {self.gross_weight}"
#         qr_img = qrcode.make(qr_content)
#         buffer = BytesIO()
#         qr_img.save(buffer, format="PNG")
#         filename = f"jewelry_{self.id}.png"
#         self.qr_code.save(filename, File(buffer), save=False)
#         self.qr_url = f"/media/qr_codes/{filename}"  # Update as per your media URL
#         super().save(*args, **kwargs)

from django.db import models
# import qrcode
from io import BytesIO
from django.core.files import File
from datetime import datetime
from django.conf import settings
import os


from django.db import models
# import qrcode
from io import BytesIO
from django.core.files import File
from datetime import datetime
from django.conf import settings

class Jewelry(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.now)
    bname = models.CharField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    metal_type = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    purity = models.CharField(max_length=20,blank=True, null=True)
    huid_number = models.CharField(max_length=100, blank=True, null=True)
    pieces = models.IntegerField(default=1)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    wastage_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    making_charge_type = models.CharField(
        max_length=50,
        choices=[("Per Gram", "Per Gram"), ("Fixed", "Fixed")]
    )
    making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    per_gram_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stone_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hallmark_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3)
    comments = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_url = models.URLField(blank=True, null=True)
    final_weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} ({self.metal_type})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Generate QR code only for new records
        if is_new:
            # ✅ Step 1 — Build jewelry detail URL (you can change domain if needed)
            domain = getattr(settings, 'DOMAIN_URL', 'http://127.0.0.1:8000')
            qr_link = f"{domain}/api/jewelry/{self.id}/"

            # ✅ Step 2 — Create QR code with that link
            qr_img = qrcode.make(qr_link)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            filename = f"jewelry_{self.id}.png"

            # ✅ Step 3 — Save QR image and URL
            self.qr_code.save(filename, File(buffer), save=False)
            self.qr_url = f"/media/qr_codes/{filename}"

            # ✅ Step 4 — Update the instance
            super().save(update_fields=["qr_code", "qr_url"])



# from django.db import models
# import qrcode
# from io import BytesIO
# from django.core.files import File
# from datetime import datetime

# class Jewelry(models.Model):
#     id = models.AutoField(primary_key=True)
#     date = models.DateField(default=datetime.now)
#     bname = models.CharField(max_length=100, blank=True, null=True)
#     bill_no = models.CharField(max_length=100, blank=True, null=True)
#     metal_type = models.CharField(max_length=100)
#     item_name = models.CharField(max_length=100)
#     purity = models.DecimalField(max_digits=5, decimal_places=2)
#     huid_number = models.CharField(max_length=100, blank=True, null=True)
#     pieces = models.IntegerField(default=1)
#     gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
#     less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
#     wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     wastage_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
#     rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
#     making_charge_type = models.CharField(
#         max_length=50,
#         choices=[("Per Gram", "Per Gram"), ("Fixed", "Fixed")]
#     )
#     making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     per_gram_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     stone_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     hallmark_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3)
#     comments = models.TextField(blank=True, null=True)
#     qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
#     qr_url = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.item_name} ({self.metal_type})"

#     def save(self, *args, **kwargs):
#         # 1️⃣ First save normally (create entry in DB)
#         is_new = self.pk is None
#         super().save(*args, **kwargs)

#         # 2️⃣ Then generate QR code only for new records
#         if is_new:
#             qr_content = (
#                 f"Jewelry ID: {self.id}\n"
#                 f"Metal: {self.metal_type}\n"
#                 f"Purity: {self.purity}\n"
#                 f"Gross Weight: {self.gross_weight}"
#             )
#             qr_img = qrcode.make(qr_content)
#             buffer = BytesIO()
#             qr_img.save(buffer, format="PNG")
#             filename = f"jewelry_{self.id}.png"

#             # Save image inside /media/qr_codes/
#             self.qr_code.save(filename, File(buffer), save=False)
#             self.qr_url = f"/media/qr_codes/{filename}"

#             # Save again — this time only updates, not inserts
#             super().save(update_fields=["qr_code", "qr_url"])


from django.db import models
from master.models import Customer
from datetime import date

class SaleItem(models.Model):

    
    BILL_TYPE_CHOICES = [
        ('GST', 'GST'),
        ('Estimate', 'Estimate'),
    ]
    id = models.AutoField(primary_key=True)
    saleitem_id = models.IntegerField(blank=True, null=True, db_index=True)
    date = models.DateField(default=date.today)  # ✅ FIXED: Use date.today, not datetime.now
    salesperson = models.CharField(max_length=100, blank=True, null=True)
    qr_barcode_id = models.CharField(max_length=100, blank=True, null=True)
    huid_number = models.CharField(max_length=100, blank=True, null=True)
    metal = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    purity = models.CharField(max_length=20,blank=True, null=True)
    pieces = models.IntegerField(default=1)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    making_type = models.CharField(max_length=50, choices=[("Per Gram", "Per Gram"), ("Fixed", "Fixed")])
    making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stone_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hallmark_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hm_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3)
    comments = models.TextField(blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sale_items")

    base_metal_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    making_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    bill_type = models.CharField(
        max_length=20,
        choices=BILL_TYPE_CHOICES,
        default='GST'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} ({self.bill_type}) - {self.customer.name}"

    def save(self, *args, **kwargs):
        try:
            self.net_weight = self.gross_weight - self.less_weight
            self.base_metal_cost = self.net_weight * self.rate_per_gram
            self.making_cost = (
                self.net_weight * self.making_charge
                if self.making_type == "Per Gram"
                else self.making_charge
            )
            subtotal = (
                self.base_metal_cost
                + self.making_cost
                + self.stone_charges
                + self.hallmark_charges
            )
            total_tax_percent = self.hm_tax_percent + self.gst_percent
            self.total_tax = subtotal * total_tax_percent / 100
            self.total_amount = subtotal + self.total_tax
        except Exception as e:
            print("Calculation Error:", e)

        super().save(*args, **kwargs)


# models.py
from django.db import models
from django.utils import timezone
from master.models import Customer  # assuming customer model already exists


# class Order(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     salesperson_name = models.CharField(max_length=100)
#     order_date = models.DateTimeField(default=timezone.now)
#     order_comments = models.TextField(blank=True, null=True)

#     urd_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
#     urd_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     urd_purity = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,blank=True, null=True)
#     discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
#     discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

#     item_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
#     making_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
#     tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
#     grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
#     balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.order_id}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson_name = models.CharField(max_length=100)
    order_date = models.DateTimeField(default=timezone.now)
    order_comments = models.TextField(blank=True, null=True)

    # -------- URD DETAILS --------
    urd_item_name = models.CharField(max_length=100, blank=True, null=True)
    urd_metal_name = models.CharField(max_length=50, blank=True, null=True)
    urd_pieces = models.IntegerField(blank=True, null=True)

    urd_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    urd_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    urd_purity = models.CharField(max_length=20, blank=True, null=True)

    # -------- DISCOUNT --------
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # -------- TOTALS --------
    item_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    making_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    attachment = models.FileField(upload_to='order_attachments/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id}"


class OrderAttachment(models.Model):
    order = models.ForeignKey(Order, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='order_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Order {self.order.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    qr_barcode = models.CharField(max_length=100)
    huid_number = models.CharField(max_length=100)
    metal_type = models.CharField(max_length=100,blank=True, null=True)

    item_name = models.CharField(max_length=100,blank=True, null=True)
    purity = models.CharField(max_length=20,blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3)
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    making_charge = models.DecimalField(max_digits=10, decimal_places=2)
    stone_charge = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50, blank=True, null=True)
    length = models.CharField(max_length=50, blank=True, null=True)
    advance_gold_weight = models.CharField(max_length=50, blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    hallmark_charge = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2)
    hm_tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(blank=True, null=True)
    

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.item_name}"


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=50)  # Cash, Card, UPI, etc.
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from master.models import Customer, Metal  # You already have Metal model

class DiamondBilling(models.Model):
    BILLING_MODES = [
        ('Estimate', 'Estimate'),
        ('GST Invoice', 'GST Invoice'),
    ]

    billing_id = models.AutoField(primary_key=True)
    mode = models.CharField(max_length=20, choices=BILLING_MODES, default='Estimate')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="diamond_billings")
    billing_date = models.DateTimeField(auto_now_add=True)

    # totals and calculation
    diamond_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metal_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    round_adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_mode = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    comments = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing #{self.billing_id} - {self.customer.name}"


# class DiamondDetail(models.Model):
#     billing = models.ForeignKey(DiamondBilling, on_delete=models.CASCADE, related_name="diamond_items")
#     qr_cert = models.CharField(max_length=100, blank=True, null=True)
#     hsn = models.CharField(max_length=100, blank=True, null=True)
#     item = models.CharField(max_length=100)
#     weight = models.DecimalField(max_digits=10, decimal_places=3)
#     carat = models.DecimalField(max_digits=10, decimal_places=3)
#     cuts = models.CharField(max_length=100, blank=True, null=True)
#     color = models.CharField(max_length=100, blank=True, null=True)
#     quantity = models.IntegerField(default=1)
#     rate = models.DecimalField(max_digits=10, decimal_places=2)
#     amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

#     def save(self, *args, **kwargs):
#         self.amount = self.quantity * self.rate
#         super().save(*args, **kwargs)

class DiamondDetail(models.Model):
    billing = models.ForeignKey(DiamondBilling, on_delete=models.CASCADE, related_name="diamond_items")
    qr_cert = models.CharField(max_length=100, blank=True, null=True)
    hsn = models.CharField(max_length=100, blank=True, null=True)
    item = models.CharField(max_length=100)

    # NEW FIELDS
    shape = models.CharField(max_length=50, blank=True, null=True)
    clarity = models.CharField(max_length=50, blank=True, null=True)
    polish = models.CharField(max_length=50, blank=True, null=True)
    symmetry = models.CharField(max_length=50, blank=True, null=True)
    fluorescence = models.CharField(max_length=50, blank=True, null=True)

    weight = models.DecimalField(max_digits=10, decimal_places=3)
    carat = models.DecimalField(max_digits=10, decimal_places=3)
    cuts = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)

    quantity = models.IntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate
        super().save(*args, **kwargs)


class DiamondMetalInfo(models.Model):
    billing = models.ForeignKey(DiamondBilling, on_delete=models.CASCADE, related_name="metal_items")
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="diamond_metal_info")
    purity = models.CharField(max_length=50,blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    making = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stone = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comments = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.amount = (self.weight * self.rate) + self.making + self.stone + self.hm
        super().save(*args, **kwargs)



from django.db import models
from django.contrib.auth.models import User
import uuid # For generating unique loan_number

# # --- Assuming these models already exist ---
# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20, unique=True)
#     email_address = models.EmailField(blank=True, null=True)
#     aadhar_number = models.CharField(max_length=16, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Metal(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.metal.name})"



from django.db import models
from datetime import date
import uuid 

class Loan(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='loans', blank=True, null=True)

    loan_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    loan_date = models.DateField(default=date.today, blank=True, null=True)
    status = models.CharField(max_length=50, default='Active', blank=True, null=True)

    item_name = models.CharField(max_length=255, blank=True, null=True)

    metal_used = models.ForeignKey('Metal', on_delete=models.CASCADE, related_name='loans_with_this_metal', blank=True, null=True)
    pieces = models.PositiveIntegerField(default=1, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=14, decimal_places=3, blank=True, null=True)
    less_stone_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, blank=True, null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, editable=False)
    purity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    value_per_gram = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, editable=False)

    hallmark_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, editable=False)
    adjusted_loan_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    interest = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    # New fields
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, editable=False)

    loan_return_period_unit = models.CharField(max_length=10, blank=True, null=True)
    period_value = models.PositiveIntegerField(blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.loan_number:
            self.loan_number = str(uuid.uuid4()).replace('-', '')[:20].upper()

        gross_weight = self.gross_weight if self.gross_weight is not None else 0
        less_stone_weight = self.less_stone_weight if self.less_stone_weight is not None else 0
        purity = self.purity if self.purity is not None else 0
        value_per_gram = self.value_per_gram if self.value_per_gram is not None else 0
        hallmark_charge = self.hallmark_charge if self.hallmark_charge is not None else 0
        tax = self.tax if self.tax is not None else 0
        adjusted_loan_amount = self.adjusted_loan_amount if self.adjusted_loan_amount is not None else 0

        self.net_weight = gross_weight - less_stone_weight
        self.current_value = self.net_weight * value_per_gram
        self.final_amount = self.current_value + hallmark_charge + tax

        # Calculate initial paid_amount and balance_amount only on creation (when id is None)
        # or if they haven't been set yet.
        # When creating a new loan, set paid_amount to 0 and balance_amount to adjusted_loan_amount
        if self._state.adding: # This checks if the object is being created for the first time
            self.paid_amount = 0.00
            self.balance_amount = adjusted_loan_amount
        else:
            # For updates, ensure balance_amount is always calculated based on current paid_amount
            # This allows future updates to paid_amount to automatically update balance.
            self.balance_amount = adjusted_loan_amount - (self.paid_amount if self.paid_amount is not None else 0)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.loan_number or 'N/A'} for {self.customer.name if self.customer else 'N/A'}"



from django.db import models
from django.utils import timezone
from decimal import Decimal

class LoanPayment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), # Added 'pending' as an initial status
        ('paid', 'Paid'),
        ('failed', 'Failed'), # Added 'failed' for robustness
    )

    id = models.AutoField(primary_key=True)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='payments')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2) # Increased max_digits to match Loan amounts
    payment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') # Default to pending initially

    payment_method = models.CharField(max_length=50, blank=True, null=True)
    loan_return_period_unit = models.CharField(max_length=20, blank=True, null=True)
    period_value = models.IntegerField(blank=True, null=True)
   
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True) # Increased max_digits

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Loan #{self.loan.loan_number or self.loan.id} - {self.payment_amount} ({self.status})"




# models.py

class LoanAttachment(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='loan_attachments/')
    file_name = models.CharField(max_length=255, blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment for Loan {self.loan.loan_number}"


class LoanCompletionAttachment(models.Model):
    """Model to store attachments for loan completion"""
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='completion_attachments')
    file = models.FileField(upload_to='loan_completion_attachments/')
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(
        max_length=50,
        choices=[
            ('invoice', 'Invoice'),
            ('receipt', 'Receipt'),
            ('certificate', 'Certificate'),
            ('document', 'Document'),
            ('other', 'Other'),
        ],
        default='document'
    )
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Loan Completion Attachment'
        verbose_name_plural = 'Loan Completion Attachments'

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Completion Attachment for Loan {self.loan.loan_number} - {self.file_type}"

####################################################################################################################





# C:\Project\Jewellary M\master\models.py

from django.db import models
from django.urls import reverse
from django.conf import settings
import os
# import qrcode
from io import BytesIO
from django.core.files import File
# from PIL import Image
import json
from decimal import Decimal # Import Decimal for safe calculations

class OrderManagement(models.Model):
    STATUS_CHOICES = [
        ('Assign', 'Assign'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Closed', 'Closed'),
    ]

    order_no = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100,blank=True, null=True)
    item = models.CharField(max_length=150,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_no} - {self.customer_name}"




# import json
# import qrcode
# from io import BytesIO
# from decimal import Decimal
# from django.conf import settings
# from django.db import models
# from django.core.files import File
# from .models import OrderManagement  # Ensure correct import


# class JobWork(models.Model):
#     order = models.ForeignKey(OrderManagement, on_delete=models.CASCADE, related_name="job_works")
#     craftsman_name = models.CharField(max_length=100)
#     date = models.DateTimeField(auto_now_add=True)
#     order_no = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)
#     contact_no = models.CharField(max_length=15)

#     # Jewelry details
#     metal_type = models.CharField(max_length=50)
#     hsn = models.CharField(max_length=50, blank=True, null=True)
#     item = models.CharField(max_length=100)
#     purity = models.DecimalField(max_digits=6, decimal_places=2)
#     huid_number = models.CharField(max_length=50, blank=True, null=True)
#     weight_gross = models.DecimalField(max_digits=10, decimal_places=3)
#     weight_less = models.DecimalField(max_digits=10, decimal_places=3)
#     weight_net = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
#     wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     wastage_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
#     rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     making = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     comments = models.TextField(blank=True, null=True)

#     # Payment Info
#     metal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     balance_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

#     qr_code_image = models.ImageField(upload_to='qrcodes/jobwork/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         is_new = self._state.adding

#         # === Auto Calculations ===
#         gross_weight = Decimal(self.weight_gross or 0)
#         less_weight = Decimal(self.weight_less or 0)
#         self.weight_net = gross_weight - less_weight

#         self.wastage_weight = (
#             (self.weight_net * Decimal(self.wastage_percent or 0)) / Decimal(100)
#         )

#         self.balance_amount = Decimal(self.metal_amount or 0) - Decimal(self.paid_amount or 0)

#         super().save(*args, **kwargs)

#         # === QR Code Generation ===
#         if is_new or not self.qr_code_image:
#             self.generate_qr_code()
#             self.save(update_fields=['qr_code_image'])

#         # === Update order status ===
#         if self.order:
#             self.order.status = "Processing"
#             self.order.save()

#     def generate_qr_code(self):
#         """Generate a QR code that links directly to the JobWork GET API"""
#         try:
#             # Build full GET API URL (dynamic from settings)
#             base_url = getattr(settings, "DOMAIN_URL", "http://127.0.0.1:8000")
#             qr_url = f"{base_url}/api/job-works/{self.id}/"

#             qr = qrcode.QRCode(
#                 version=1,
#                 error_correction=qrcode.constants.ERROR_CORRECT_H,
#                 box_size=10,
#                 border=4,
#             )
#             qr.add_data(qr_url)
#             qr.make(fit=True)

#             img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

#             buffer = BytesIO()
#             img.save(buffer, format='PNG')
#             filename = f'jobwork_qr_{self.id}.png'
#             self.qr_code_image.save(filename, File(buffer), save=False)
#         except Exception as e:
#             print("QR generation failed:", e)

#     def __str__(self):
#         return f"{self.order_no} - {self.craftsman_name}"




import json
# import qrcode
from io import BytesIO
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.files import File

class JobWork(models.Model):
    order = models.ForeignKey('OrderManagement', on_delete=models.CASCADE, related_name="job_works")
    craftsman_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    order_no = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)

    metal_type = models.CharField(max_length=50)
    hsn = models.CharField(max_length=50, blank=True, null=True)
    item = models.CharField(max_length=100)
    purity = models.CharField(max_length=20, blank=True, null=True)
    huid_number = models.CharField(max_length=50, blank=True, null=True)
    weight_gross = models.DecimalField(max_digits=10, decimal_places=3)
    weight_less = models.DecimalField(max_digits=10, decimal_places=3)
    weight_net = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    wastage_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    wastage_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    making = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    stone_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    hallmark_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    hm_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    gst_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    metal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    qr_code_image = models.ImageField(upload_to='qrcodes/jobwork/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        gross_weight = Decimal(self.weight_gross or 0)
        less_weight = Decimal(self.weight_less or 0)
        self.weight_net = gross_weight - less_weight

        self.wastage_weight = (self.weight_net * Decimal(self.wastage_percent or 0)) / Decimal(100)

        metal_amt = Decimal(self.metal_amount or 0)
        making_amt = Decimal(self.making or 0)
        stone_amt = Decimal(self.stone_charges or 0)
        hm_amt = Decimal(self.hm_charges or 0)
        hm_tx = Decimal(self.hallmark_tax or 0)
        gst_p = Decimal(self.gst_tax or 0)

        sub_total = metal_amt + making_amt + stone_amt + hm_amt + hm_tx
        gst_amount = (sub_total * gst_p) / Decimal(100)
        total_with_tax = sub_total + gst_amount
        
        self.balance_amount = total_with_tax - Decimal(self.paid_amount or 0)

        super().save(*args, **kwargs)

        if is_new or not self.qr_code_image:
            self.generate_qr_code()
            self.save(update_fields=['qr_code_image'])

        if self.order:
            self.order.status = "Processing"
            self.order.save()

    def generate_qr_code(self):
        try:
            base_url = getattr(settings, "DOMAIN_URL", "http://127.0.0.1:8000")
            qr_url = f"{base_url}/api/job-works/{self.id}/"

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f'jobwork_qr_{self.id}.png'
            self.qr_code_image.save(filename, File(buffer), save=False)
        except Exception as e:
            pass

    def __str__(self):
        return f"{self.order_no} - {self.craftsman_name}"
#####################################################################################################################
from django.db import models
from django.utils import timezone

class MetalRate(models.Model):
    metal_name = models.CharField(max_length=50)
    carat = models.CharField(max_length=50)
    rate_percentage = models.DecimalField(max_digits=6, decimal_places=2)
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('metal_name', 'carat', 'date')  # Prevent duplicates for same day

    def __str__(self):
        return f"{self.metal_name} - {self.carat}K - {self.date}"


from django.db import models
from django.utils import timezone

class PurchaseVoucher(models.Model):
    date = models.DateField(default=timezone.now)
    bill_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    metal = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_no} - {self.name}"


from django.db import models

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.supplier_name

######################################################################################################################

class PurchaseInvoice(models.Model):
    supplier_name = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bill_no = models.CharField(max_length=50)
    date = models.DateField()

    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gross_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    advance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    net_payable = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    paid = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    mode = models.CharField(max_length=50, null=True, blank=True)
    into_stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_no} - {self.supplier_name}"


class PurchaseItem(models.Model):
    invoice = models.ForeignKey(
        PurchaseInvoice,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )

    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )

    supplier_id = models.CharField(max_length=200, null=True, blank=True)
    supplier_name = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    hsn = models.CharField(max_length=50, null=True, blank=True)
    segment = models.CharField(max_length=100, null=True, blank=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    pieces = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    making = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    base = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    net = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    hm = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='purchase_documents/', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item or 'Item'} - {self.supplier_name or 'Unknown Supplier'}"


###################################################################################################




# models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class ItemPayment(models.Model):
    # Item details
    
    sale_item_id =  models.IntegerField(null=True, blank=True)
    item_name = models.CharField(max_length=100, null=True, blank=True)
    metal_type  = models.CharField(max_length=50, null=True, blank=True)
    purity = models.CharField(max_length=20, null=True, blank=True)
    final_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    urd_exchange_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Financial Summary
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hsn_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    grand_before_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Payment Details
    transaction_method = models.CharField(max_length=50, null=True, blank=True)
    transaction_number = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    # Installment Info
    installment_type = models.CharField(max_length=20, null=True, blank=True)  # daily, weekly, monthly, quarterly, yearly
    no_of_months = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(default=date.today, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default="active")  # active, completed, overdue

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate end_date based on installment type and months
        if self.start_date and self.no_of_months:
            self.end_date = self.start_date + timedelta(days=30 * self.no_of_months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name or 'Item'} - {self.transaction_method or 'N/A'}"




class InstallmentEntry(models.Model):
    item_payment = models.ForeignKey(ItemPayment, on_delete=models.CASCADE, related_name="installments")
    installment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_type = models.CharField(max_length=20)
    count = models.IntegerField()
    payment_status = models.CharField(max_length=20, default="unpaid")  # paid/unpaid
    status = models.CharField(max_length=20, default="active")  # active/completed/overdue

    def __str__(self):
        return f"{self.installment_date} - {self.amount}"


# models.py

class InstallmentAttachment(models.Model):
    installment = models.ForeignKey(
        InstallmentEntry,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file = models.FileField(upload_to="installment_attachments/")
    file_name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment for Installment {self.installment.id}"
    
    
from django.db import models
from master.models import JobWork  # assuming master_jobwork = JobWork

class CraftsmanAttachment(models.Model):
    jobwork = models.ForeignKey(JobWork, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="craftsman_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for JobWork ID {self.jobwork.id}"


#######################################################################################################################



from django.db import models
from django.utils import timezone

class URDAdjustment(models.Model):
    sale_item = models.OneToOneField(
        SaleItem, on_delete=models.CASCADE, related_name='urd_adjustment'
    )
    adjust_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    adjust_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    adjust_hm_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Adjustment for Sale Item #{self.sale_item.id}"


class URDDetail(models.Model):
    urd_adjustment = models.ForeignKey(
        URDAdjustment, on_delete=models.CASCADE, related_name='urd_details'
    )
    sale_item = models.ForeignKey(
        SaleItem, on_delete=models.CASCADE, related_name='urd_details'
    )
    metal = models.CharField(max_length=100, blank=True, null=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    pieces = models.PositiveIntegerField(default=0)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    comments = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='urd_files/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"URD for Sale Item #{self.sale_item.id} - {self.item or 'N/A'}"


###############################################################################################################


# notifications/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('ALERT', 'Alert'),
        ('WARNING', 'Warning'),
        ('SUCCESS', 'Success'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES, default='INFO')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.type})"


###############################################################################################################


from django.db import models
from datetime import date
import uuid
from decimal import Decimal
from django.utils import timezone


class Bhishi(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='bhishis', blank=True, null=True)

    bhishi_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bhishi_date = models.DateField(default=date.today, blank=True, null=True)
    status = models.CharField(max_length=50, default='Active', blank=True, null=True)

    bhishi_type = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    per_installment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_installments = models.PositiveIntegerField(blank=True, null=True)

    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, editable=False)

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.bhishi_number:
            self.bhishi_number = str(uuid.uuid4()).replace('-', '')[:20].upper()

        total_amount = self.total_amount if self.total_amount else Decimal('0.00')
        paid = self.paid_amount if self.paid_amount else Decimal('0.00')

        # If creating a new Bhishi
        if self._state.adding:
            self.paid_amount = Decimal('0.00')
            self.balance_amount = total_amount

        else:
            self.balance_amount = total_amount - paid

        # Status change
        if self.balance_amount <= 0:
            self.status = "Completed"
        else:
            self.status = "Active"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bhishi {self.bhishi_number or 'N/A'}"
    


class BhishiPayment(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    bhishi = models.ForeignKey(Bhishi, on_delete=models.CASCADE, related_name='payments')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bhishi Payment {self.payment_amount} ({self.status})'


######################################################################################################################


class BhishiInstallment(models.Model):
    bhishi = models.ForeignKey(Bhishi, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField(blank=True, null=True)
    payment_ref = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bhishi', 'installment_number')
        ordering = ['installment_number']

    def __str__(self):
        return f"{self.bhishi.bhishi_number} - Inst #{self.installment_number}"

######################################################################################################


from django.db import models
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Make sure to import MasterPurchaseInvoice from your models
from .models import PurchaseInvoice 

class SupplierAttachment(models.Model):
    purchase_invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="supplier_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Invoice ID {self.purchase_invoice_id}"

###############################################

# models.py

class BhishiAttachment(models.Model):
    bhishi = models.ForeignKey(Bhishi, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='bhishi_attachments/')
    file_name = models.CharField(max_length=255, blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name} - Bhishi {self.bhishi.id}"