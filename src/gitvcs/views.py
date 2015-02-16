
from django.http.response import HttpResponse, Http404
from django.views.generic.base import TemplateView

from gitvcs import repository
from gitvcs.repository import local_repo    

def _get_branch(request, default_name='master'):
    branch_name = request.GET.get('branch')
    if not branch_name:
        if not local_repo().heads:
            raise Http404("There are no branches. The repository might be empty or the repository patrh isn't configured correctly.")
        
        if default_name in local_repo().heads:
            branch_name = default_name
        else:
            branch_name = local_repo().heads[0].name
    
    if branch_name in local_repo().heads:
        return local_repo().heads[branch_name]
    else:
        raise Http404("A branch named "+branch_name+" doesn't exists.")

class BrowseSourceView(TemplateView):

    template_name = "gitvcs/browse_source.html"
    
    def get_context_data(self, **kwargs):
        context = super(BrowseSourceView, self).get_context_data(**kwargs)
        
        branch = _get_branch(self.request)
        
        context['file_tree_data'] = repository.tree_as_json(branch.commit.tree, branch.name)
        context['branch_name'] = branch.name
        context['all_branches'] = repository.branches()
        
        return context

class FileContentsView(TemplateView):
    
    template_name = "gitvcs/file_contents.html"
    
    def get_context_data(self, **kwargs):
        context = super(FileContentsView, self).get_context_data(**kwargs)
        
        file_path = self.request.GET.get('path')
        if not file_path:
            raise Http404("No file specified.")
        
        branch = _get_branch(self.request)
        
        context['file_contents'] = branch.commit.tree[file_path].data_stream.read().decode('ascii')
        context['file_path'] = file_path
        context['branch_name'] = branch.name
        context['all_branches'] = repository.branches()
        
        return context

def diff(request):
    return HttpResponse('hi this is diff')


    