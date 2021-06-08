from django.shortcuts import render, redirect
from django.views import View

from app_posts.forms import PostForm, CsvForm
from app_posts.models import Post, Like, update_like, PhotoToPost, CsvModel
from app_posts.views_str_render import PostWithPhotos, TableMiniPosts
from app_users.models import Profile
from app_home.addons_for_views import PageNumsList
from app_posts.read_csv import ProcessUploadCsvPosts


class PostPage(View):
    def get(self, request, id_post):
        obj_post = PostWithPhotos(post_obj=Post.objects.get(id=id_post))
        context = {
            'title': obj_post.obj_model().short_text,
            'obj_post': obj_post,
            'users_like_list': list(Like.objects.filter(post_id=id_post)  # Список всех пользователей поставивших лайк
                                    .values_list('user_profile__user_id', flat=True)),
        }
        return render(request, 'app_posts/full_size/post.html', context)

    def post(self, request, id_post):
        obj_post = Post.objects.get(id=id_post)
        user_profile = Profile.objects.get(user_id=request.user.id)
        users_like_list = list(Like.objects.filter(post_id=id_post).values_list('user_profile__user_id', flat=True))
        if request.POST['action'] == 'add':
            if request.user.id not in users_like_list:
                update_like(obj_post, user_profile)
        elif request.POST['action'] == 'del':
            if request.user.id in users_like_list:
                update_like(obj_post, user_profile, remove_like=True)
        return redirect('post page', id_post)


class CreatePost(View):
    def get(self, request):
        context = {
            'title': 'Создание поста',
            'main_form': PostForm(),
            'csv_form': CsvForm(),
        }
        return render(request, 'app_posts/full_size/create_post.html', context)

    def post(self, request):
        user_profile = Profile.objects.get(id=request.user.id)

        if request.POST['action'] == 'main':
            create_post_form = PostForm(request.POST, request.FILES)
            if create_post_form.is_valid():
                new_post = Post.objects.create(
                    text=create_post_form.cleaned_data.get('text'),
                    author_profile=user_profile
                )
                photos = request.FILES.getlist('photos')
                if photos:
                    for photo in photos:
                        PhotoToPost.objects.create(
                            post=new_post,
                            photo=photo
                        )
                return redirect('home page')
            return redirect('create post')

        elif request.POST['action'] == 'csv':
            csv_form = CsvForm(request.POST, request.FILES)
            if csv_form.is_valid():
                new_csv = CsvModel.objects.create(
                    user_profile=user_profile,
                    csv_file=request.FILES['csv_file']
                )
                csv_file = new_csv.csv_file
                if ProcessUploadCsvPosts(file=csv_file, author_profile=user_profile).update_model():
                    return redirect('home page')
            return redirect('create post')

        return redirect('create post')


class PostsList(View):
    def get(self, request, page_num):
        posts_list = PageNumsList(page_num=page_num, num_objs=8, model_objs=Post.objects.all())
        context = {
            'title': 'Список Постов',
            'page_num': page_num,
            'page_nums_list': posts_list.get_page_num_list(),
            'mini_posts_list': TableMiniPosts(post_objects=posts_list.get_model_objs_list('-publication_date', '-id')
                                              ).get_html_str()
        }
        return render(request, 'app_posts/posts_list.html', context)
