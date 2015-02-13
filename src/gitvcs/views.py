
from django.shortcuts import render

from gitvcs.repository import local_repo


def browse_source(branch='master', commit='last'):
    pass

def get_all_branches():
    pass

def file_contents():
    pass

def diff():
    pass






def test(request):
    response=''
    #shutil.rmtree('repo', ignore_errors=True)
    
    #empty_repo = Repo.init('repo', bare=True)
    #origin = empty_repo.create_remote('origin', "https://e13109:password@puppet.ftn.uns.ac.rs/gitlab/uks2014/tim1.git")
    #assert origin.exists()
    #assert origin == empty_repo.remotes.origin == empty_repo.remotes['origin']
    
    #for fetch_info in origin.fetch():
    #    print("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))
    

    
    

    
    #response = (local_repo().heads[0].commit.tree.blobs[2]).data_stream.read().decode('ascii')
    #response = local_repo().heads[0].commit.parents[1].tree.blobs[2].data_stream.read().decode('ascii')
    for t in local_repo().tree().trees[0].trees:
        for b in t.blobs:
            response += b.data_stream.read().decode('ascii')
        
    
    
    
    
    return render(request,'gitvcs/test.html', {"response":response})

def branches_list(request):
    return render(request,'gitvcs/branches_list.html', {"branches_list":parse_heads()})

def parse_tree(tree):
    resp_list = []
    resp_list.append('dir: '+tree.path+'/'+tree.name)
    for sub_tree in tree.trees:
        resp_list.extend(parse_tree(sub_tree))
    for blob in tree.blobs:
        resp_list.append('______file: '+blob.path+'/'+blob.name)
    return resp_list

def parse_heads():
    resp_list = []
    for head in local_repo().heads:
        resp_list.extend(parse_head(head))
    return resp_list

def parse_head(head):
    resp_list = []
    resp_list.append('branch: '+head.name)
    resp_list.extend(parse_commit(head.commit))
    return resp_list

def parse_commit(commit):
    resp_list = []
    resp_list.append('_____commit: '+commit.message)
    for parent in commit.parents:
        resp_list.extend(parse_commit(parent))
    return resp_list





    
    