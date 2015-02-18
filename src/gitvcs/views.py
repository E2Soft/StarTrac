
from django.core.exceptions import SuspiciousOperation
from django.http.response import HttpResponse, Http404
from django.views.generic.base import TemplateView

from gitvcs import repository
from gitvcs.repository import local_repo


def _get_rev(branch_name=None, commit_sha=None, default_branch_name='master'):
    
    if not local_repo().branches:
        raise Http404("There are no branches. The repository might be empty or the repository patrh isn't configured correctly.")
    
    if branch_name and commit_sha:
        raise SuspiciousOperation("A branch and a commit can't be specified at the same time.") # bad request
    
    if not (branch_name or commit_sha):
        if default_branch_name is None:
            return None
        
        if default_branch_name in local_repo().branches:
            branch_name = default_branch_name
        else:
            branch_name = local_repo().branches[0].name
    
    if commit_sha:
        return (repository.commit(commit_sha), 'commit', commit_sha)
    
    if branch_name:
        return (local_repo().branches[branch_name].commit, 'branch', branch_name)

class BrowseSourceView(TemplateView):

    template_name = "gitvcs/browse_source.html"
    
    def get_context_data(self, **kwargs):
        context = super(BrowseSourceView, self).get_context_data(**kwargs)
        
        commit, rev_type, rev_name = _get_rev(self.request.GET.get('branch'), self.request.GET.get('commit'))

        context['file_tree_data'] = repository.tree_as_json(commit.tree, rev_type, rev_name)
        context['rev_name'] = rev_name
        context['rev_type'] = rev_type
        context['all_branches'] = repository.branches()
        
        return context

class FileContentsView(TemplateView):
    
    template_name = "gitvcs/file_contents.html"
    
    def get_context_data(self, **kwargs):
        context = super(FileContentsView, self).get_context_data(**kwargs)
        
        file_path = self.request.GET.get('path')
        if not file_path:
            raise Http404("No file specified.")
        
        commit, rev_type, rev_name = _get_rev(self.request.GET.get('branch'), self.request.GET.get('commit'))
        
        context['file_contents'] = commit.tree[file_path].data_stream.read().decode('ascii')
        context['file_path'] = file_path
        context['rev_name'] = rev_name
        context['rev_type'] = rev_type
        context['all_branches'] = repository.branches()
        
        return context

def diff(request):
    return HttpResponse('hi this is diff')

class CommitListView(TemplateView):
    
    template_name = "gitvcs/commit_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(CommitListView, self).get_context_data(**kwargs)
        
        rev = _get_rev(self.request.GET.get('branch'), self.request.GET.get('commit'), default_branch_name=None)
        if rev is None:
            rev_name = None
        else:
            _, _, rev_name = rev
        
        context['rev_name'] = rev_name if rev_name else "All"
        context['commits'] = repository.commits(rev_name)
        context['all_branches'] = repository.branches()
        
        return context

class CommitDetailView(TemplateView):
    
    template_name = "gitvcs/commit_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(CommitDetailView, self).get_context_data(**kwargs)
        
        commit_sha = kwargs.get('commit')
        if not commit_sha:
            raise Http404("No commit specified.")
        
        commit = repository.commit(commit_sha)
        
        if not commit:
            raise Http404("A commit with sha "+commit_sha+" doesn't exists.")
        
        context['commit'] = commit
        context['all_branches'] = repository.branches()
        
        return context
    
class DiffListView(TemplateView):
    
    template_name = "gitvcs/diff_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(DiffListView, self).get_context_data(**kwargs)
        
        commit_a, rev_type_a, rev_name_a = _get_rev(self.request.GET.get('branch_a'), self.request.GET.get('commit_a'))
        commit_b, rev_type_b, rev_name_b = _get_rev(self.request.GET.get('branch_b'), self.request.GET.get('commit_b'))
        
        diff_index = commit_a.diff(commit_b)
        
        context['diff_index'] = diff_index
        context['rev_type_a'] = rev_type_a
        context['rev_type_b'] = rev_type_b
        context['rev_name_a'] = rev_name_a
        context['rev_name_b'] = rev_name_b
        context['all_branches'] = repository.branches()
        
        return context
    
    
    