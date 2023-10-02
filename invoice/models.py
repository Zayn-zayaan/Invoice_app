from django.db import models

# Create your models here.

class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.customer_name
    
class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_details')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    price = models.FloatField()
    
    def __str__(self):
        return self.invoice.customer_name 