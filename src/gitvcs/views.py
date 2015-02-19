
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.shortcuts import redirect
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
        
        context['file_contents'] = repository.get_blob_contents(commit.tree[file_path])
        context['file_path'] = file_path
        context['rev_name'] = rev_name
        context['rev_type'] = rev_type
        context['all_branches'] = repository.branches()
        
        return context

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
    
class DiffDetailView(TemplateView):
    
    template_name = "gitvcs/diff_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(DiffDetailView, self).get_context_data(**kwargs)
        
        file_path = self.request.GET.get('path')
        if not file_path:
            raise Http404("No file specified.")
        
        commit_a, rev_type_a, rev_name_a = _get_rev(self.request.GET.get('branch_a'), self.request.GET.get('commit_a'))
        commit_b, rev_type_b, rev_name_b = _get_rev(self.request.GET.get('branch_b'), self.request.GET.get('commit_b'))
        
        diff_index = commit_a.diff(commit_b, create_patch=True)
        
        diff_info = repository.get_diff_by_path(diff_index, file_path)
        if not diff_info:
            raise Http404("Diff doesn't exist.")
        
        context['file_path'] = file_path
        context['diff'] = diff_info
        context['file_contents_a'] = repository.get_blob_contents(diff_info.a_blob) if not diff_info.new_file else None
        context['file_contents_b'] = repository.get_blob_contents(diff_info.b_blob) if not diff_info.deleted_file else None
        context['rev_type_a'] = rev_type_a
        context['rev_type_b'] = rev_type_b
        context['rev_name_a'] = rev_name_a
        context['rev_name_b'] = rev_name_b
        context['all_branches'] = repository.branches()
        
        return context
    
class DiffSelectView(TemplateView):
    
    template_name = "gitvcs/diff_select.html"
    
    def dispatch(self, request, *args, **kwargs):  
        ref_type_a = request.GET.get('ref_type_a')
        ref_type_b = request.GET.get('ref_type_b')
        
        if not (ref_type_a or ref_type_b):
            return super(DiffSelectView, self).dispatch(request, *args, **kwargs)
        
        if ref_type_a == 'branch':
            ref_a = request.GET.get('branch_a')
            param_a = 'branch_a='+ref_a
        elif ref_type_a == 'commit':
            ref_a = request.GET.get('commit_a')
            param_a = 'commit_a='+ref_a
        else:
            raise SuspiciousOperation("Unknown ref_type.")
        
        if ref_type_b == 'branch':
            ref_b = request.GET.get('branch_b')
            param_b = 'branch_b='+ref_b
        elif ref_type_b == 'commit':
            ref_b = request.GET.get('commit_b')
            param_b = 'commit_b='+ref_b
        else:
            raise SuspiciousOperation("Unknown ref_type.")
        
        if not ref_a or not ref_b:
            raise Http404("Ref a not specified.")
        
        return redirect(reverse('diff_list')+'?'+param_a+'&'+param_b, permanent=True)
    
    def get_context_data(self, **kwargs):
        context = super(DiffSelectView, self).get_context_data(**kwargs)
        context['all_branches'] = repository.branches()
        return context
    
    