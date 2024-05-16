from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ExchangeRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    skill_offered = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_requested = models.ForeignKey(Skill, related_name='requested_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')

class Feedback(models.Model):
    sender = models.ForeignKey(User, related_name='sent_feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_feedback', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')

    def __str__(self):
        return self.title


# class User(AbstractUser):
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#
#     def __str__(self):
#         return self.username
#
#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return{
#             'refresh':str(refresh),
#             'access':str(refresh.access_token)
#         }