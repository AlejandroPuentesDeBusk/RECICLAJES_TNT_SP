from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
import json

from django.utils import timezone


from mainapp.models import Material, Transaction, Transaction_Details, Day_Report



Users = get_user_model()




@login_required
def cv(request):

    today = timezone.now


    materials = Material.objects.all()

    #paginador
    materials_p = Paginator(materials, 8)
    page_numb = request.GET.get('page')
    show_page = materials_p.get_page(page_numb)




    return render(request, 'compra_venta/com_ven.html', {'show_page': show_page,
                                                        'today':today})




@login_required
def realizar_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            
            materials = data.get('materials', [])
            tipo_operacion = data.get('tipoOperacion')
            tipo_cargo = data.get('tipoCargo')
            discount = data.get('discount', 0)
            extra_charge = data.get('extra_charge', 0)
            total = data.get('total', 0)
            description = data.get('description', '')

        
            if not materials or not tipo_operacion or not tipo_cargo:
                return JsonResponse({'success': False, 'message': 'Datos incompletos.'})

       
            transaction = Transaction.objects.create(
                User=request.user,
                Total=total,
                Discount=discount,
                Transaction_Type=tipo_operacion.upper(),  
                Description=description,
                Status='COMPLETED'  
            )

           
            for item in materials:
                material_id = item.get('materialId')
                quantity = item.get('quantity', 0)
                price = item.get('price', 0)

              
                try:
                    material = Material.objects.get(id=material_id)
                except Material.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'El material con ID {material_id} no existe.'})

                subtotal = float(quantity) * float(price)

               
                Transaction_Details.objects.create(
                    Material=material,
                    Transaction=transaction,
                    Price=price,
                    Subtotal=subtotal,
                    Quantity=quantity
                )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        raise Http404
