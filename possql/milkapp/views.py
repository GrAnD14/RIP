import psycopg2
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Service, Order
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

def service_list(request):
    product_to_search = request.GET.get('product')
    
    if product_to_search:
        services = Service.objects.filter(is_active=True, name__contains=product_to_search)
    else:
        services = Service.objects.filter(is_active=True)
    
    return render(request, 'service_list.html', {'services': services, 'product_to_search': product_to_search})

@require_POST
def deactivateService(request):
    service_id = request.POST.get('service_id')
    product_to_search = request.POST.get('product_to_search', '')

    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        port=settings.DATABASES['default']['PORT']
    )

    cursor = conn.cursor()

    try:
        # Используйте параметризованный запрос
        cursor.execute("UPDATE milkapp_service SET is_active=False WHERE id=%s", (service_id,))
        conn.commit()
    except Exception as e:
        # Обработайте возможные ошибки базы данных
        print(f"Error updating service: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def service_detail(request, id):
    product = Service.objects.get(id=id)
    return render(request, 'service_detail.html', {'product': product})

def orders(request):
    all_orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': all_orders})

def create_order(request):
    if request.method == 'POST':
        parent_name = request.POST['parent_name']
        service_id = request.POST['service_id']

        # Получаем объект Service или возвращаем 404, если не найден
        product = get_object_or_404(Service, id=service_id)

        # Создаем заказ с использованием связи многие ко многим
        order = Order(parent_name=parent_name)
        order.save()
        order.services.add(product)  # Добавляем связанную услугу к заказу

        return redirect(reverse('service_detail', args=[service_id]))

def new_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']

        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)

            new_service = Service(name=name, price=price, image=filename)
            new_service.save()

            return redirect(reverse('service_list'))

    return render(request, 'new_service.html')
