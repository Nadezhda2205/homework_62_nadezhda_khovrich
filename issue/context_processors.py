from issue.forms import SearchTaskForm

def get_searchtaskform(requesr):
    searchtaskform = SearchTaskForm()
    context = {
        'searchtaskform': searchtaskform,
        }

    return context
    