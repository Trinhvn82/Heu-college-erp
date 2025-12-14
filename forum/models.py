from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ForumPostImage(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='forum_images/')

    def __str__(self):
        return f"Image for {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Reply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.post.title}"


class ReplyImage(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='forum_reply_images/')

    def __str__(self):
        return f"Image for reply {self.reply.id}"
