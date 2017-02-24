from django.conf.urls import url

from task_admin.views import RenderPreviewView, CodeRenderView

urlpatterns = [
    url(r'^render$', RenderPreviewView.as_view(), name='render_preview'),
    url(r'^code_render$', CodeRenderView.as_view(), name='code_render'),

]
