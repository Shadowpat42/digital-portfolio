import json
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, LoginForm

from .models import CustomUser, Post, MethodologicalResource, Reaction, Media


def index(request):
    return render(request, "about.html")


# не используется
@csrf_exempt
def user_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]

            if not CustomUser.is_valid_email(email):
                return HttpResponse(status=HTTPStatus.BAD_REQUEST)

            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            user.save()
            response_data = {
                "user": user.json(),
            }
            return JsonResponse(response_data, status=HTTPStatus.OK)

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON data", status=HTTPStatus.BAD_REQUEST)

    else:
        # todo: Поменять method == GET
        return HttpResponse("<h1>Hello world</h1>")


def get_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "get_post.html", {"post": post})


def event(request):
    posts = Post.objects.all()
    reaction_count_dict = {}
    for post in posts:
        reactions = Reaction.objects.filter(post=post)
        reaction_count_dict[post.id] = {
            "like": reactions.filter(reaction_type=Reaction.LIKE).count(),
            "dislike": reactions.filter(reaction_type=Reaction.DISLIKE).count(),
            "heart": reactions.filter(reaction_type=Reaction.HEART).count(),
            "fire": reactions.filter(reaction_type=Reaction.FIRE).count(),
        }
    return render(
        request,
        "event.html",
        {"posts": posts, "reaction_count_dict": reaction_count_dict},
    )


@csrf_exempt
def methodological_resources(request):
    if request.method == "POST":
        sort_by = request.POST.get("sort_by")
        if sort_by == "date":
            resources = MethodologicalResource.objects.all().order_by("-created_at")
        else:
            resources = MethodologicalResource.objects.all()
    else:
        resources = MethodologicalResource.objects.all()
    return render(
        request,
        "methodological_resources.html",
        {"methodological_resources": resources},
    )


@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            auth_login(request, user)
            return redirect(
                "user", user_id=user.id
            )  # Перенаправление на вашу главную страницу после регистрации
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@csrf_exempt
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(
                    "user", user_id=user.id
                )  # Перенаправление на вашу главную страницу после входа
            else:
                # Обработка неверных данных входа
                pass
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    reactions = Reaction.objects.filter(user=user)
    return render(request, "get_user.html", {"user": user, "reactions": reactions})


@csrf_exempt
def react_to_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        reaction_type = request.POST.get("reaction_type")
        if reaction_type in ["like", "dislike", "heart", "fire"]:
            existing_reaction = Reaction.objects.filter(
                user=request.user, post=post, reaction_type=reaction_type
            ).first()

            if existing_reaction:
                existing_reaction.delete()
                return redirect("event")

            else:
                new_reaction = Reaction.objects.create(
                    user=request.user, post=post, reaction_type=reaction_type
                )
                return redirect("event")
        else:
            return JsonResponse({"error": "Invalid reaction type"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def reward(request):
    return render(request, "reward.html")


def media_list(request):
    media_files = Media.objects.all()
    return render(request, "media.html", {"media_files": media_files})


# не используется
def react_to_media(request, media_id):
    if request.method == "POST":
        media = get_object_or_404(Media, pk=media_id)
        reaction_type = request.POST.get("reaction_type")
        if reaction_type in ["like", "dislike", "heart", "fire"]:
            existing_reaction = Reaction.objects.filter(
                user=request.user, media=media, reaction_type=reaction_type
            ).first()

            if existing_reaction:
                existing_reaction.delete()
                return JsonResponse(
                    {"error": f"{reaction_type.capitalize()} reaction removed"}
                )
            else:
                new_reaction = Reaction.objects.create(
                    user=request.user, media=media, reaction_type=reaction_type
                )
                return redirect("media")
        else:
            return JsonResponse({"error": "Invalid reaction type"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)
