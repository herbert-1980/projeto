from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from apps.reviews.models import Review
from apps.reviews.forms import ReviewForm


def add_review(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id=object_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content_type = content_type
            review.object_id = object_id
            review.save()
            return redirect('reviews:list_reviews', content_type_id=content_type.id, object_id=object_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form, 'content_object': content_object})

def list_reviews(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id=object_id)
    reviews = Review.objects.filter(content_type=content_type, object_id=object_id)
    
    return render(request, 'reviews/list_reviews.html', {'reviews': reviews, 'content_object': content_object})
