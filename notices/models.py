from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from utils.constants import HOST


class ForumNotice(models.Model):
    sender_discussion = models.ForeignKey(to='forums.Discussion', on_delete=models.CASCADE, null=True, blank=True)
    sender_discussion_comment = models.ForeignKey(to='forums.DiscussionComment', on_delete=models.CASCADE, null=True,
                                                  blank=True)
    sender_answer = models.ForeignKey(to='forums.Answer', on_delete=models.CASCADE, null=True, blank=True)
    sender_answer_comment = models.ForeignKey(to='forums.AnswerComment', on_delete=models.CASCADE, null=True,
                                              blank=True)

    recipient = models.ForeignKey(to='users.UserAuth', on_delete=models.CASCADE, related_name='user_forum_notices')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def ret_created_at(self):
        return str(naturaltime(self.created_at))

    @cached_property
    def get_notice_href(self):
        if self.sender_discussion:
            lnk = reverse('discussion_detail_view', kwargs={'discussion_id': self.sender_discussion.id})
            return f'{HOST}{lnk}'
        elif self.sender_discussion_comment:
            lnk = reverse('discussion_detail_view',
                          kwargs={'discussion_id': self.sender_discussion_comment.discussion.id})
            return f'{HOST}{lnk}#discussion-comment-{self.sender_discussion_comment.id}'
        elif self.sender_answer:
            lnk = reverse('discussion_detail_view', kwargs={'discussion_id': self.sender_answer.discussion.id})
            return f'{HOST}{lnk}#answer-{self.sender_answer.id}'
        elif self.sender_answer_comment:
            lnk = reverse('discussion_detail_view',
                          kwargs={'discussion_id': self.sender_answer_comment.answer.discussion.id})
            return f'{HOST}{lnk}#answer-comment-{self.sender_answer_comment.id}'
