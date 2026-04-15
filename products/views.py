from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from .service import parent_categories, discount_desc, category_unique_product,new_arrivals, featured_products
from home.service import get_sliders, get_banners, get_brands
from blog.service import get_latest_posts
from django.contrib import messages
from .models import Comment, Saved, Like, RecentlyProduct, ProductView
from django.contrib.auth.decorators import login_required
from .form import CommentForm



class IndexView(View):
    def get(self, request):
        context = {
            'categories': parent_categories(),
            'discount_desc': discount_desc(),
            'category_unique_product': category_unique_product(),
            'new_arrivals': new_arrivals(),
            "featured_products":  featured_products(),
            'sliders': get_sliders(),
            'banners': get_banners(),
            'brands': get_brands(),
            'latest_posts': get_latest_posts(),
        }
        return render(request,"index.html",context=context)


class ProductDetailView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)

        if request.user.is_authenticated:
            RecentlyProduct.objects.get_or_create(
                user=request.user,
                product=product,
            )

        ProductView.objects.create(product=product)

        comments = product_comments(id)
        user_comment = comments.filter(user=request.user).first() if request.user.is_authenticated else None

        context = {
            'product': product,
            'categories': parent_categories(),
            'comments': comments,
            'comment_form': CommentForm(instance=user_comment) if user_comment else CommentForm(),
            'user_comment': user_comment,
            'product_view_count': product.view_product.count(),
            'comment_count': comments.count(),
            'saved_count': product.saved_users.count(),
            'like_count': product.liked_users.count(),
            'is_saved': request.user.is_authenticated and Saved.objects.filter(user=request.user, product=product).exists(),
            'is_liked': request.user.is_authenticated and Like.objects.filter(user=request.user, product=product).exists(),
        }
        return render(request, "product.html", context=context)


@login_required()
def comment_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method != 'POST':
        return redirect('product_detail', id=product.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment, created = Comment.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'text': form.cleaned_data['text'],
                'rate': form.cleaned_data['rate'],
            },
        )
        if created:
            messages.success(request, 'Izohingiz qoldirildi')
        else:
            messages.success(request, 'Izohingiz yangilandi')
        return redirect('product_detail', id=product.id)

    messages.warning(request, 'Izoh ma`lumotlari noto`g`ri kiritildi')
    return redirect('product_detail', id=product.id)
    

@login_required()
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user != request.user:
        messages.warning(request, 'Bu commentni ozgartirolmaysiz')
        return redirect('product_detail', id=comment.product.id)

    if request.method != 'POST':
        return redirect('product_detail', id=comment.product.id)

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Comment ozgartirildi')
    else:
        messages.warning(request, 'Commentni saqlashda xatolik yuz berdi')
    return redirect('product_detail', id=comment.product.id)
        
        
@login_required()
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user:
        product_id = comment.product.id
        comment.delete()
        messages.success(request, 'Comment ochirildi')
        return redirect('product_detail', id=product_id)

    messages.warning(request, 'Bu commentni ochirolmaysiz')
    return redirect('product_detail', id=comment.product.id)
       
@login_required()
def my_comments(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'profile_section_title': 'My comments',
        'profile_mode': 'comments',
        'profile_comments': comments,
    })

        
def product_comments(product_id):
    comments = Comment.objects.filter(product=product_id).select_related('user', 'product')
    return comments


@login_required()
def saved(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    saved, created = Saved.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, 'Mahsulot saqlandi')
    else:
        saved.delete()
        messages.success(request, 'Saved ro`yxatdan olib tashlandi')
    return redirect('product_detail', id=product.id)


@login_required()
def like(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    like_obj, created = Like.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, 'Mahsulot like qilindi')
    else:
        like_obj.delete()
        messages.success(request, 'Like bekor qilindi')
    return redirect('product_detail', id=product.id)
        
        
@login_required()
def user_saveds(request):
    saved_products = request.user.saved_products.all().select_related('product')
    return render(request, 'profile.html', {
        'profile_section_title': 'Saved products',
        'profile_mode': 'products',
        'profile_items': saved_products,
    })


@login_required()
def user_likes(request):
    liked_products = request.user.liked_products.all().select_related('product')
    return render(request, 'profile.html', {
        'profile_section_title': 'Liked products',
        'profile_mode': 'products',
        'profile_items': liked_products,
    })



@login_required()
def user_recently(request):
    recently_products = request.user.recently_products.all().select_related('product')
    return render(request, 'profile.html', {
        'profile_section_title': 'Recently viewed',
        'profile_mode': 'products',
        'profile_items': recently_products,
    })
    
    
        
        
        