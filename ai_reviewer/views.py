from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import views
from .models import CodeReview
from .forms import CodeReviewForm
from django.conf import settings
from .forms import CodeSubmissionForm
from .models import CodeSubmission
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from .utils import review_code_with_ai



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
             # 🔥 SESSION CONTROL
            if request.POST.get("remember_me"):
                # Stay logged in for 2 days
                request.session.set_expiry(172800)
            else:
                # Logout when browser closes
                request.session.set_expiry(0)
            return redirect("submit_code")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "register.html")


def home_view(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def submit_code_view(request):
    review_data = None

    if request.method == 'POST':
        form = CodeReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            code = form.cleaned_data['code']
            language = form.cleaned_data['language']

            # 🔥 AI call
            ai_review_json = review_code_with_ai(code, language)

            # ✅ Save to DB (keep this)
            review.json_review = ai_review_json
            review.score = ai_review_json.get('score', 5)
            review.result = str(ai_review_json)
            review.save()

            # ✅ SEND TO TEMPLATE (instead of redirect)
            review_data = {
                "score": review.score,
                "language": language,
                "output": ai_review_json.get("output"),
                "errors": ai_review_json.get("errors", []),
                "improvements": ai_review_json.get("improvements", []),
                "optimized_code": ai_review_json.get("optimized_code"),
            }

    else:
        form = CodeReviewForm()

    return render(request, 'submit_code.html', {
        'form': form,
        'review': review_data
    })
        

@login_required
def dashboard_view(request):
    reviews = CodeReview.objects.filter(user=request.user).order_by("-created_at")[:5]
    total_reviews = CodeReview.objects.filter(user=request.user).count()

    context = {
        "reviews": reviews,
        "total_reviews": total_reviews,
    }
    return render(request, "dashboard.html", context)


@login_required
def profile_view(request):
    reviews = CodeReview.objects.filter(user=request.user)

    total_reviews = reviews.count()
    good_reviews = reviews.filter(score__gte=8).count()
    average_reviews = reviews.filter(score__gte=5, score__lt=8).count()
    poor_reviews = reviews.filter(score__lt=5).count()

    context = {
        "total_reviews": total_reviews,
        "good_reviews": good_reviews,
        "average_reviews": average_reviews,
        "poor_reviews": poor_reviews,
    }
    return render(request, "profile.html", context)

@login_required
def review_result_view(request, review_id):
    review = CodeReview.objects.get(id=review_id, user=request.user)
    return render(request, "review_result.html", {"review": review})

@login_required
def review_history_view(request):
    # Base queryset
    reviews_qs = CodeReview.objects.filter(user=request.user)
    
    # Filtering
    language = request.GET.get('language')
    if language and language != 'all':
        reviews_qs = reviews_qs.filter(language=language)
    
    min_score = request.GET.get('min_score')
    if min_score:
        reviews_qs = reviews_qs.filter(score__gte=int(min_score))
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        reviews_qs = reviews_qs.filter(created_at__date__gte=start_date)
    if end_date:
        reviews_qs = reviews_qs.filter(created_at__date__lte=end_date)
    
    search = request.GET.get('search')
    if search:
        reviews_qs = reviews_qs.filter(code__icontains=search)
    
    # Sorting
    sort = request.GET.get('sort', 'date_desc')
    if sort == 'score_desc':
        reviews_qs = reviews_qs.order_by('-score')
    elif sort == 'language':
        reviews_qs = reviews_qs.order_by('language')
    else:
        reviews_qs = reviews_qs.order_by('-created_at')
    
    # Stats
    stats = reviews_qs.aggregate(
        total=Count('id'),
        avg_score=Avg('score')
    )
    
    # Pagination
    paginator = Paginator(reviews_qs, 10)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    context = {
        'reviews': reviews,
        'stats': stats,
        'filter_params': request.GET.urlencode(),
    }
    return render(request, "review_history.html", context)

