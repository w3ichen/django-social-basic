from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import NewPostForm, NewCommentForm
from django.contrib import messages
from django.http import HttpResponse

@login_required(login_url='register')
def home(request):
	context = {
		'posts':Post.objects.all().order_by('-date_posted'),
		'post_form':NewPostForm(),
		'comment_form':NewCommentForm()
	}
	return render(request, 'blog/home.html', context)

@login_required(login_url='register')
def newPost(request):
    if request.method == 'POST':
      # new post
      form = NewPostForm(request.POST)
      form.instance.user = request.user
      if form.is_valid():
        form.save()
        messages.success(request, f'Posted')
    return redirect('blog-home')

@login_required(login_url='register')
def deletePost(request, id):
	Post.objects.get(id=id).delete()
	return redirect("blog-home")

@login_required(login_url='register')
def editPost(request,id):
	post = Post.objects.get(id=id)
	if request.method == 'POST':
		# if user hits update, then update
		post.content = request.POST['content']
		post.save() # update post
		messages.success(request, f'Successfully updated post')
		return redirect('blog-home')
	# if user is still updating form, then show form with current content
	form = NewPostForm(instance=post)	# empty form with post info
	return render(request, 'blog/update.html', {'form':form,'id':id})

@login_required(login_url='register')
def like(request):
	if request.method == "GET":
		post_id = request.GET['post_id']
		liked_post = get_object_or_404(Post, id=post_id)
		if liked_post.likes.filter(username=request.user.username).count() == 1:
			# user has already liked the post
			liked_post.likes.remove(request.user)
			liked_post.likes_count = liked_post.likes.count()
			liked_post.save()
			return HttpResponse('-1')
		else:
			liked_post.likes.add(request.user)
			liked_post.likes_count = liked_post.likes.count()
			liked_post.save()
			return HttpResponse('1')

	return redirect('blog-home')

@login_required(login_url='register')
def comment(request):
	if request.method == "GET":
		newComment = Comment.objects.create(
			user = request.user,
			text = request.GET.get('text')
		)

		commented_post = Post.objects.get(id=request.GET.get('post_id'))

		commented_post.comments.add(newComment)
		commented_post.comments_count = commented_post.comments.count()
		commented_post.save()
		messages.success(request, f'Comment Added')
	return HttpResponse('Comment Added')

@login_required(login_url='register')
def deleteComment(request, postId, commentId):
	post = Post.objects.get(id=postId)
	comment = post.comments.get(id=commentId).delete()
	post.comments_count = post.comments.count()
	post.save()
	return redirect("blog-home")