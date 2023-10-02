from rest_framework import serializers
from . import models


class InvoiceDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    class Meta:
        model = models.InvoiceDetail
        fields = ['id', 'description', 'quantity', 'unit_price', 'price']


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(models.InvoiceDetail, many=True)
    class Meta:
        model = models.Invoice
        fields = ['id', 'customer_name', 'date', 'invoice_details']

    
    # overiding create method to create invoice details 
    # pass the whole list of invoiceDetail objects in the payload
    def create(self, validated_data):

        invoice_details = validated_data.pop("invoice_details")
        invoice = models.Invoice.objects.create(**validated_data)
        invoice_details_list = []

        for item in invoice_details:
            instance, created = models.InvoiceDetail.objects.get_or_create(invoice=invoice, **item)
            invoice_details_list += [instance]

        invoice.invoice_details.set(invoice_details_list)
        invoice.save()


        return invoice
    
    # overiding update method to update invoice details 
    # pass the whole list of invoiceDetail objects in the payload
    def update(self, instance, validated_data):
        invoice_details = validated_data.pop('invoice_details')

        for item in invoice_details:
            models.InvoiceDetail.objects.filter(id=item['id']).update(**item)

        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        return instance
    

