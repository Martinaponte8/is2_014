from django.views.generic import ListView, CreateView, UpdateView, DetailView
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.enums import TA_RIGHT
from .models import Cliente
from proyecto.models import Proyecto, TeamMember
from clientes.forms import CreateClientForm, UpdateClientForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from reportlab.pdfgen import canvas
import locale
from django.views.generic import View
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (Paragraph,
                                Table,
                                SimpleDocTemplate,
                                Spacer,
                                TableStyle,
                                Image, KeepTogether)
from userstory.models import UserStory
from is2_014 import settings

"""
Vistas necesarias para la administracion de Cliente
"""


@method_decorator(login_required, name='dispatch')
class ClientListView(LoginRequiredMixin, ListView):
    """
    Clase de la vista de lista de Clientes
    """
    template_name = 'clientes/list.html'
    model = Cliente
    queryset = Cliente.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object_list = Cliente.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Clientes"
        context['direccion'] = {}
        context['direccion']['Clientes'] = (1, '/clientes/')
        return context


@method_decorator(login_required, name='dispatch')
class CreateClientView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Clase de la vista de Creacion de Cliente
    """
    template_name = 'clientes/cliente.html'
    model = Cliente
    success_url = '../'
    form_class = CreateClientForm
    success_message = 'Se ha creado el cliente'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Cliente"
        context['direccion'] = {}
        context['direccion']['Clientes'] = (1, '/clientes/')
        context['direccion']['Crear Cliente'] = (2, '/clientes/create/')
        return context

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = None
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        permisos = request.user.get_nombres_permisos()
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos, form=form))


@method_decorator(login_required, name='dispatch')
class UpdateClientView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase de la vista de Modificacion de Cliente
    """
    template_name = 'clientes/cliente.html'
    model = Cliente
    form_class = UpdateClientForm
    success_url = './'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Cliente"
        context['direccion'] = {}
        context['direccion']['Clientes'] = (1, '/clientes/')
        context['direccion']['Modificar: ' + self.object.nombre] = (
        2, '/clientes/modificar/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser modificado
        :param queryset:
        :return: Retorna el cliente a ser modificado
        """
        return Cliente.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object = None
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        permisos = request.user.get_nombres_permisos()
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos, form=form))


@method_decorator(login_required, name='dispatch')
class VerClientDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    """
    Clase de la vista para ver clientes
    """
    model = Cliente
    template_name = 'clientes/ver_cliente.html'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Cliente"
        context['direccion'] = {}
        context['direccion']['Clientes'] = (1, '/clientes/')
        context['direccion']['Ver: ' + self.object.nombre] = (2, '/clientes/ver/' + str(self.object.pk) + '/')
        context['proyectos'] = Proyecto.objects.filter(cliente=self.get_object())
        context['cliente'] = self.object
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser visualizado
        :param queryset:
        :return: Retorna el cliente a ser visualizado
        """
        return Cliente.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProyectosClientePDF(View):
    """
    clase de la vista para creacion de reporte de Proyectos del cliente
    """

    def get(self, request, *args, **kwargs):
        """
        metodo de respuesta a la consulta GET
        :param request: consulta GET
        :param args: argumentos
        :param kwargs: diccionario de datos
        :return: respuesta a la consulta GET
        """
        self.cliente = Cliente.objects.get(pk=self.kwargs['pk'])
        response = HttpResponse(content_type='application/pdf')
        # se crea el pdf
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.doc = SimpleDocTemplate(buffer)
        self.doc.title = 'Reporte de Proyectos del Cliente: ' + str(self.cliente.nombre)
        self.story = []
        self.encabezado()
        self.titulo()
        self.descripcion()
        self.crearTabla()
        self.doc.build(self.story, onFirstPage=self.numeroPagina,
                       onLaterPages=self.numeroPagina)
        pdf = buffer.getvalue()
        # fin
        buffer.close()
        response.write(pdf)
        return response

    def encabezado(self):
        """
        agrega el encabezado al reporte
        :return: None
        """
        logo = settings.MEDIA_ROOT+"logo2.png"
        im = Image(logo, inch, inch)
        im.hAlign = 'LEFT'
        p = Paragraph("<i>Software Gestor de Proyectos<br/>Asunción-Paraguay<br/>Contacto: 0981-222333</i>", self.estiloPR())
        data_tabla = [[im, p]]
        tabla = Table(data_tabla)
        self.story.append(tabla)

        d = Drawing(480, 3)
        d.add(Line(0, 0, 480, 0))
        self.story.append(d)
        self.story.append(Spacer(1, 0.3 * inch))

    def titulo(self):
        """
        agrega el titulo al reporte
        :return: None
        """
        txt = "<b><u>Reporte de Proyectos de Cliente</u></b>"
        p = Paragraph('<font size=20>'+str(txt)+'</font>', self.estiloPC())
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def descripcion(self):
        """
        agrega la cabecera del reporte
        :return: None
        """
        txt = "<b>Cliente: </b>"+self.cliente.nombre+"<br/><b>Descripción: </b>" + self.cliente.descripcion+"<br/><b>Teléfono: </b>"+ self.cliente.telefono
        p = Paragraph('<font size=12>' + str(txt) + '</font>', self.estiloPL())
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def crearTabla(self):
        """
        agrega la tabla del reporte
        :return: None
        """
        proyectos = Proyecto.objects.filter(cliente=self.cliente.pk)
        nro = 1
        data = [["N°", "Proyectos", "Estado", "Usuarios Asignados" , "US Terminados", "US Asignados", "US Pendientes"]]
        for x in proyectos:
            # Hallar numero de US terminados y no finalizados
            us_total = UserStory.objects.filter(proyecto=x.pk)
            ut = us_total.filter(estado=0).count() ## US FINALIZADO
            ua = us_total.filter(estado=1).count()  ## US ASIGNADO
            up = us_total.filter(estado=2).count()  ## US PENDIENTE
            usuarios_asig = TeamMember.objects.filter(proyecto=x.pk).count() #Usuarios Asignados al Proyecto
            aux = [nro, x.nombre, x.estado, usuarios_asig, ut, ua, up]
            nro += 1
            data.append(aux)
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        # Altura variable dependiendo de la cantidad de datos
        t = Table(data)
        t.setStyle(style)
        self.story.append(t)

    def estiloPC(self):
        """
        :return: estilo del cuerpo del reporte
        """
        return ParagraphStyle(name="centrado", alignment=TA_CENTER)

    def estiloPL(self):
        """
        :return: estilo de la descripcion del reporte
        """
        return ParagraphStyle(name="izquierda", alignment=TA_LEFT)

    def estiloPR(self):
        """
        :return: estilo del encabezado
        """
        return ParagraphStyle(name="derecha", alignment=TA_RIGHT)

    def numeroPagina(self, canvas, doc):
        """
        agrega el numero de pagina al documento
        :param canvas:
        :param doc:documento pdf
        :return: None
        """
        num = canvas.getPageNumber()
        text = "Página %s" % num
        canvas.drawRightString(190 * mm, 20 * mm, text)
