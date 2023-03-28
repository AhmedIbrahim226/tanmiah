from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50, help_text=_("The name of this reporting category."))
    description = models.TextField(help_text=_("A short description of this reporting category."))
    show_when_reporting = models.SmallIntegerField(
        choices=[
            (1, 'content'),
            (2, 'members'),
            (3, 'content & members'),
        ],
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def ret_created_at(self):
        return str(naturaltime(self.created_at))




class Report(models.Model):
    reported_discussion = models.ForeignKey(to='forums.Discussion', on_delete=models.CASCADE, null=True, blank=True)
    reported_discussion_comment = models.ForeignKey(to='forums.DiscussionComment', on_delete=models.CASCADE,
                                                    null=True,
                                                    blank=True)
    reported_answer = models.ForeignKey(to='forums.Answer', on_delete=models.CASCADE, null=True, blank=True)
    reported_answer_comment = models.ForeignKey(to='forums.AnswerComment', on_delete=models.CASCADE, null=True,
                                                blank=True)
    reported_to = models.ForeignKey('users.UserAuth', on_delete=models.CASCADE, related_name='user_completed_reports')
    date_reported = models.DateTimeField(auto_now_add=True)

    @cached_property
    def get_reports_num(self):
        return self.report_contents.count()

    @cached_property
    def ret_date_reported(self):
        return str(naturaltime(self.date_reported))

    # @cached_property
    # def get_notice_href(self):
    #     if self.sender_discussion:
    #         lnk = reverse('discussion_detail_view', kwargs={'discussion_id': self.sender_discussion.id})
    #         return f'{HOST}{lnk}'
    #     elif self.sender_discussion_comment:
    #         lnk = reverse('discussion_detail_view',
    #                       kwargs={'discussion_id': self.sender_discussion_comment.discussion.id})
    #         return f'{HOST}{lnk}#discussion-comment-{self.sender_discussion_comment.id}'
    #     elif self.sender_answer:
    #         lnk = reverse('discussion_detail_view', kwargs={'discussion_id': self.sender_answer.discussion.id})
    #         return f'{HOST}{lnk}#answer-{self.sender_answer.id}'
    #     elif self.sender_answer_comment:
    #         lnk = reverse('discussion_detail_view',
    #                       kwargs={'discussion_id': self.sender_answer_comment.answer.discussion.id})
    #         return f'{HOST}{lnk}#answer-comment-{self.sender_answer_comment.id}'

class ReportContent(models.Model):
    report = models.ForeignKey('reports.Report', on_delete=models.CASCADE, related_name='report_contents')
    reported_by = models.ForeignKey('users.UserAuth', on_delete=models.CASCADE, related_name='user_reporters')
    category = models.ForeignKey('reports.Category', on_delete=models.SET_NULL, blank=True, null=True)

    @cached_property
    def get_reports_num(self):
        return self.report.get_reports_num

    @cached_property
    def ret_date_reported(self):
        return self.report.ret_date_reported



