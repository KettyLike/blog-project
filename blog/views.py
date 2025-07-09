from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, ArticleImage
from .forms import ArticleForm, ArticleImageForm
from django.contrib.auth.decorators import login_required
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import os
from dotenv import load_dotenv

def article_list(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        files = request.FILES.getlist('images')
        image_forms = [ArticleImageForm(files={'image': f}) for f in files]

        if form.is_valid() and all(f.is_valid() for f in image_forms):
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            for f in image_forms:
                img = f.save(commit=False)
                img.article = article
                img.save()

            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
        image_forms = []

    return render(request, 'article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save()
            images_to_delete = request.POST.getlist('delete_images')
            for image_id in images_to_delete:
                ArticleImage.objects.filter(id=image_id, article=article).delete()

            for img in request.FILES.getlist('images'):
                ArticleImage.objects.create(article=article, image=img)

            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    images = article.images.all()
    return render(request, 'article_form.html', {'form': form, 'article': article, 'images': images})
@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user:
        article.delete()
    return redirect('article_list')


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@csrf_exempt
@require_POST
def generate_article_text(request):
    prompt = request.POST.get('prompt')
    style = request.POST.get('style', 'standard')

    style_prompt = {
        'standard': '',
        'short_news': ' Напиши коротку новину:',
        'blog_post': ' Напиши як блог-пост з емоціями:',
    }

    full_prompt = prompt + style_prompt.get(style, '')


    if not prompt:
        return JsonResponse({'error': 'Порожній запит'}, status=400)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a Ukrainian journalist writing articles."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        generated_text = response.choices[0].message.content
        return JsonResponse({'text': generated_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)