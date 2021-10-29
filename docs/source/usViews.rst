Comentarios
============

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import UserStory
from userstory.forms import CreateUserStoryForm, UpdateUserStoryForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from tipoUserStory.models import *
from userstory.models import *


"""
Funcion eliminar UserStory
"""
def eliminar4(request,pk_proyecto,us_id):
    payload = {'project.pk': pk_proyecto, 'us_id': us_id}
    Us = UserStory.objects.get(id=payload['us_id'])
    Us.delete()
    return redirect("index")

@method_decorator(login_required, name='dispatch')
class UserStoryListView(LoginRequiredMixin, ListView):
"""
Vista de la lista de UserStory
"""
    queryset = UserStory.objects.all()

    def get(self,request,*args,**kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto,object_list=self.object_list,permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super(UserStoryListView,self).get_context_data(**kwargs)
        context['title'] = 'User Stories'
        return context


@method_decorator(login_required, name='dispatch')
class CreateUserStoryView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
"""
Vista para la creacion de un User Story
"""

    def get_object(self, queryset=None):
"""
metodo que retorna el objeto actual
"""
:param queryset:
"""
:return: el objeto actual
"""
        obj = UserStory()
        return obj

    def get(self,request,*args,**kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        for tipo in context['tipos_us']:
            if tipo.pk not in context['flujos'].keys():
                context['flujos'][tipo.pk] = tipo.flujos.all
        context['title'] = "Crear User Story"
        return context


@method_decorator(login_required, name='dispatch')
class UpdateUserStoryView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Vista para la modificacion de un User Story
"""
    template_name = 'userstory/userstory.html'
    model = UserStory
    form_class = UpdateUserStoryForm
    success_url = '../../'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        for tipo in context['tipos_us']:
            if tipo.pk not in context['flujos'].keys():
                context['flujos'][tipo.pk] = tipo.flujos.all
        context['title'] = "Modificar User Story"
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][str(context['project'])] = (2, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/')
        context['direccion']['User Stories'] = (3, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/userstories/')
        context['direccion']['Modificar: ' + self.object.nombre] = (4, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/userstories/modificar/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
"""
metodo que retorna el objeto actual
"""
:param queryset:
"""
:return: el objeto actual
"""
        return UserStory.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class VerUserStoryDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
"""
Clase de la vista para ver User Stories, sin opcion de modificar
"""

    def get(self, request, *args, **kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['title'] = "Ver User Story"
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][str(context['project'])] = (2, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/')
        context['direccion']['Sprints'] = (3, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/userstories/')
        context['direccion']['Ver: ' + self.object.nombre] = (4, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/userstories/ver/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
"""
retorna el objecto actual
"""
:param queryset:
"""
:return: el objeto actual
"""
        return UserStory.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProductBacklogListView(LoginRequiredMixin, ListView):
"""
Vista del Product Backlog
"""
    def get(self, request, *args, **kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, project=proyecto, ol=ol))


    def get_context_data(self, *, object_list=None, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super(ProductBacklogListView,self).get_context_data(**kwargs)
        context['title'] = "Product Backlog"
        for us in self.object_list:
            return context

@method_decorator(login_required, name='dispatch')
class ProductBacklogPDF(View):
"""
    clase de la vista para creacion de reporte Product Backlog
"""
    def get(self, request, *args, **kwargs):
"""
        metodo de respuesta a la consulta GET
        :param request: consulta GET
        :param args: argumentos
        :param kwargs: diccionario de datos
        :return: respuesta a la consulta GET
"""
        self.encabezado()
        self.titulo()
        self.descripcion()
        self.crearTabla()
        buffer.close()
        response.write(pdf)
        return response

    def encabezado(self):
"""
        agrega el encabezado al reporte :return: None
"""
        self.story.append(tabla)
        d.add(Line(0, 0, 480, 0))
        self.story.append(d)
        self.story.append(Spacer(1, 0.3 * inch))

    def titulo(self):
"""
        agrega el titulo al reporte :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def descripcion(self):
"""
        agrega la cabecera del reporte :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.3 * inch))

    def crearTabla(self):
"""
        agrega la tabla del reporte :return: None
"""
        for us in us_query:
            if us.estado != 0 and us.sprints_asignados:
                l1.append(us)
            elif (us.estado == 1 or us.estado == 0):
                l2.append(us)
            else:
                l3.append(us)
        l1.sort(key=lambda x: x.priorizacion, reverse=True)
        l2.sort(key=lambda x: x.priorizacion, reverse=True)
        l3.sort(key=lambda x: x.priorizacion, reverse=True)
        for us in l1:
            user_stories.append(us)
        for us in l2:
            user_stories.append(us)
        for us in l3:
            user_stories.append(us)
        for x in user_stories:
            aux = [nro,x.nombre, estados[x.estado] if not (x.estado != 0 and x.sprints_asignados) else "No Terminado", \
                locale.format("%0.2f", x.priorizacion, grouping=True)]
            data.append(aux)
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

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

@login_required
def ver_archivo(request,archivo_id):
"""
Vista utilizada para la visualizacion de archivos
"""
:param request:
"""
:param archivo_id: id del archivo a ser visualizado
"""
:return: el archivo adjunto
"""
    respuesta = HttpResponse(content=archivo_a_devolver)
    respuesta['Content-Type'] = 'application/octet-stream'
    respuesta['Content-Disposition'] = 'attachment; filename="%s"' % archivo.archivo.name
    return respuesta