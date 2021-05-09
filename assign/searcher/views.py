from django.shortcuts import render
from .forms import SearchForm
# Create your views here.
from .rank import main


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results, time_taken = main(query=query)
            print(len(set(results)))
            new_dict = {}
            repeat = ""
            for doc in results:
                if doc[1] in new_dict:
                    repeat = doc[1]
                new_dict[doc[1]] = doc[2]
                # print(i[0])
                print(new_dict[doc[1]])
                # print(num)
                # num += 1
            print(len(new_dict))
            print(f"Repeated: {repeat}")
            return render(request, 'searcher/results.html', {'results': new_dict, 'endtime': time_taken})

    else:
        form = SearchForm()
    return render(request, 'searcher/search.html', {'form': form})
