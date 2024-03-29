import traceback
from store_project_app.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Cast, Coalesce
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from .forms import *
import json
from .models import Categoria
from .models import Producto
from .models import Detalle_Venta

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class EstadisticasView(TemplateView):
    template_name = "estadisticas.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "productos_mas_vendidos":
                data = {
                    "name": "Producto",
                    "colorByPoint": True,
                    "data": self.productos_mas_vendidos(),
                }
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def productos_mas_vendidos(self):
        data = []
        ano = datetime.now().year
        mes = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = (
                    Detalle_Venta.objects.filter(
                        id_venta__fecha_venta__year=ano,
                        id_venta__fecha_venta__month=mes,
                        id_producto=p.id_producto,
                        id_venta__is_anulada=False,
                    )
                    .aggregate(resultado=Coalesce(Sum("cantidad"), 0))
                    .get("resultado")
                )
                data.append({"name": p.nombre, "y": float(total)})
        except Exception as e:
            track = traceback.format_exc()
            print(track)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Estadisticas"
        context["productos_mas_vendidos"] = self.productos_mas_vendidos()
        return context


class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "categoria/categorias.html"

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categoria"
        return context


class CategoriaCreateView(CreateView):

    model = Categoria
    form_class = nueva_categoria_form
    template_name = "categoria/categoria_form.html"
    success_url = reverse_lazy("{% url 'AgregarCategoria' %}")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear una Categoria"
        context["action"] = "add"
        return context


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = nueva_categoria_form
    template_name = "categoria/categoria_form.html"
    success_url = reverse_lazy("Categoria")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Categoría"
        context["action"] = "edit"
        return context


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = "categoria/eliminar_categoria.html"
    success_url = reverse_lazy("Categoria")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar una Categoria"
        return context


class ProductosListView(ListView):

    model = Producto
    template_name = "producto/productos.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Productos"
        return context


class ProductoCreateView(CreateView):

    model = Producto
    form_class = nuevo_producto_form
    template_name = "producto/producto_form.html"
    success_url = reverse_lazy("{% url 'AgregarProducto' %}")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Añadir un producto"
        context["action"] = "add"
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = nuevo_producto_form
    template_name = "producto/producto_form.html"
    success_url = reverse_lazy("Productos")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Producto"
        context["action"] = "edit"
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "producto/eliminar_producto.html"
    success_url = reverse_lazy("Productos")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar un Producto"
        return context


class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = nueva_venta_form
    template_name = "venta/venta_form.html"
    success_url = reverse_lazy("Index")
    permission_required = "store_project_app.change_categoria"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            producto = Producto.objects.filter(stock__gt=0)
            action = request.POST["action"]
            if action == "autocomplete":
                productos = Producto.objects.filter(
                    nombre__icontains=request.POST["term"], stock__gt=0
                )[0:10]
                for i in productos:
                    data = []
                    item = i.toJSON()
                    item["value"] = i.nombre
                    data.append(item)

            elif action == "add":
                ventas = json.loads(request.POST["ventas"])
                venta = Venta()
                venta.id_cliente = Cliente.objects.get(id_cliente=ventas["id_cliente"])
                # venta.id_empleado = Empleado.objects.get(
                #     id_empleado=ventas['id_empleado'])
                venta.fecha_venta = ventas["fecha_venta"]
                venta.forma_pago = Metodo_Pago.objects.get(
                    id_metodo_pago=ventas["forma_pago"]
                )
                venta.precio_total = float(ventas["precio_total"])
                venta.save()

                for i in ventas["productos"]:
                    detalle_venta = Detalle_Venta()
                    detalle_venta.id_venta = Venta.objects.get(id_venta=venta.id_venta)
                    detalle_venta.id_producto = Producto.objects.get(
                        id_producto=i["id_producto"]
                    )
                    detalle_venta.cantidad = int(i["cantidad"])
                    detalle_venta.subtotal = float(i["subtotal"])
                    detalle_venta.save()

                    detalle_venta.id_producto.stock -= detalle_venta.cantidad
                    detalle_venta.id_producto.save()
                data = {"id": venta.id_venta}
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
            track = traceback.format_exc()
            print(track)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear una Venta"
        context["entity"] = "Venta"
        context["list_url"] = self.success_url
        context["action"] = "add"
        return context


class VentaListView(ListView):

    model = Venta
    template_name = "venta/consultar_venta.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Venta.objects.filter(is_anulada=False):
                    data.append(i.toJSON())
            elif action == "searchdata_detalle":
                data = []
                for i in Detalle_Venta.objects.filter(id_venta=request.POST["id"]):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            track = traceback.format_exc()
            print(track)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Ventas"
        return context


class VentaFacturaPdfView(View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template("venta/factura.html")
            context = {
                "venta": Venta.objects.get(pk=self.kwargs["pk"]),
                "detalle": Detalle_Venta.objects.filter(id_venta=self.kwargs["pk"]),
                "comp": {
                    "name": "Cacharreria El Portal",
                    "ruc": "RUC",
                    "address": "Direccion",
                },
            }
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="reporte.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse("We had some errors <pre>" + html + "</pre>")
            return response
        except Exception as e:
            track = traceback.format_exc()
            print(track)
            return HttpResponseRedirect(reverse_lazy("ListaVenta"))


class ClienteListView(ListView):
    model = Cliente
    template_name = "cliente/clientes.html"

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        return context


class ClienteCreateView(CreateView):

    model = Cliente
    form_class = nuevo_cliente_form
    template_name = "cliente/cliente_form.html"
    success_url = reverse_lazy("{% url 'Clientes' %}")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Añadir un Cliente"
        context["action"] = "add"
        return context


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = nuevo_cliente_form
    template_name = "cliente/cliente_form.html"
    success_url = reverse_lazy("Clientes")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Cliente"
        context["action"] = "edit"
        return context


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "cliente/eliminar_cliente.html"
    success_url = reverse_lazy("Clientes")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar un Cliente"
        return context


class VentaUpdateView(UpdateView):

    model = Venta
    form_class = nueva_venta_form
    template_name = "venta/anular_venta.html"
    success_url = reverse_lazy("Clientes")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {}
        try:
            action = request.POST["action"]
            if action == "edit":
                form = self.get_form()
                data = form.save()
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Anular Venta"
        context["action"] = "edit"
        return context


class VentaAnuladaListView(ListView):

    model = Venta
    template_name = "venta/lista_ventas_anuladas.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Venta.objects.filter(is_anulada=True):
                    data.append(i.toJSON())
            elif action == "searchdata_detalle":
                data = []
                for i in Detalle_Venta.objects.filter(id_venta=request.POST["id"]):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            track = traceback.format_exc()
            print(track)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Ventas Anuladas"
        return context


class VentaPorCobrarListView(ListView):

    model = Venta
    template_name = "venta/ventas_por_cobrar.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Venta.objects.filter(
                    is_anulada=False, forma_pago__id_metodo_pago__contains=2
                ):
                    data.append(i.toJSON())
            elif action == "searchdata_detalle":
                data = []
                for i in Detalle_Venta.objects.filter(id_venta=request.POST["id"]):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Ventas"
        return context
