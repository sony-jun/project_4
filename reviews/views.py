from urllib import request
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "reviews/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        reviews_form = ReviewForm(request.POST)
        if reviews_form.is_valid():
            reviews_form.save()
        return redirect("reviews:index")
    else:
        reviews_form = ReviewForm()
    context = {"reviews_form": reviews_form}

    return render(request, "reviews/create.html", context=context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)

    context = {"reviews": review}
    return render(request, "reviews/detail.html", context)


def update(request, pk):
    reviews = Review.objects.get(pk=pk)
    if request.method == "POST":
        reviews_form = ReviewForm(request.POST, instance=reviews)
        if reviews_form.is_valid():
            reviews_form.save()
            return redirect("reviews:index")
    else:
        reviews_form = ReviewForm(instance=reviews)
    context = {"reviews_form": reviews_form}
    return render(request, "reviews/update.html", context)


def delete(request, pk):
    Review.objects.get(id=pk).delete()
    return redirect("reviews:index")


@login_required
def comment_create(request, pk):
    reviews = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.reviews = reviews
        comment.user = request.user
        comment.save()
    return redirect("reviews:detail", reviews.pk)


@login_required
def comments_delete(request, reviews_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("reviews:detail", reviews_pk, comment_pk)
